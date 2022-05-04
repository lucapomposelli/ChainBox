# DOCS https://flask-restful.readthedocs.io/en/latest/
# this file handle all api lv2 requests from app and website.
# fill the request table of daemons
# read the db and answer requests

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import time
import datetime
import json
import mysql.connector
from web3 import Web3
from web3.gas_strategies.time_based import fast_gas_price_strategy
from threading import Timer, Thread
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
# .env usage
from dotenv import dotenv_values
config = dotenv_values(".env")

from hashlib import sha256

from werkzeug.sansio.response import Response


app = Flask(__name__)
api = Api(app)

try:
    with open(config["ABI_FILE"]) as f:
        info_json = json.load(f)
    abi = info_json["abi"]
except Exception as e:
    print("Cannot load ABI.\nDetails: " + str(e))
    exit()

infuraEndpoint = config["ETH_ENDPOINT"]
chainId = config["CHAINID"]
contractAddress = config["CONTRACT"]

xDaiEndPoint = config["XDAI_ENDPOINT"]
xDaiChainId = config["XDAI_CHAINID"]
web3 = Web3(Web3.HTTPProvider(infuraEndpoint))
contract = web3.eth.contract(address=contractAddress, abi=abi)
web3.eth.set_gas_price_strategy(fast_gas_price_strategy)
sc_admin = config["SC_ADMIN"]

#start xDai web3
xDai_web3 = Web3(Web3.HTTPProvider(xDaiEndPoint))
xDai_web3.eth.set_gas_price_strategy(fast_gas_price_strategy)

mydb = mycursor = ""
broadcastTxSourceAllowedIp = json.loads(config["ALLOWED_IPS"])

PASSPHRASE: Optional[str] = None  # "meherett"

# Initialize Ethereum mainnet BIP44HDWallet
bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
#FinCode database connection
def dbConnect(local = False):
    local_mydb = ""
    local_mycursor = ""
    if not local:
        print("\nWaiting for FinCode database connection...")
    local_mydb = mysql.connector.connect(
        host = config["DB_HOST"],
        port = config["DB_PORT"],
        user = config["DB_USER"],
        password = config["DB_PW"],
        database = config["DB"],
    )
    #Only this particular cursor will buffer results
    local_mycursor = local_mydb.cursor(buffered = True, dictionary = True)
    if not local:
        global mydb
        global mycursor
        mydb = local_mydb
        mycursor = local_mycursor
        print("INFO: Database connected!")
    return local_mydb, local_mycursor

#FinCode database disconnection
def dbClose(local_mydb = None, local_mycursor = None) :
    if local_mydb is not None or local_mycursor is not None:
        local_mycursor.close()
        local_mydb.close()
    else:
        print("\nWaiting for FinCode database disconnection...")
        global mydb
        global mycursor
        mycursor.close()
        mydb.close()
        print("INFO: Database disconnected!\n")


def updateRequest(id, status, description = None, txhash = None, table = "requests"):
    sql = 'UPDATE ' + table + ' SET status = "' + status + '"'
    
    if description is not None:
        sql = sql +  ', description = "' + description + '"'

    if txhash is not None:
        sql = sql +  ', txhash = "' + txhash + '"'
    
    sql = sql + ' WHERE id = "' + str(id) + '"'

    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    print("\nTx with id = " + str(id) + " updated.")
    return True


def checkAuth(body, authKey, hash):
    hash_salt = config["HASH_SALT"]
    authKey_local = config["AUTH_KEY"]
    #calculate hash (sha256 body+salt)
    text = body + hash_salt
    h=sha256()
    h.update(text.encode())
    hash_calc=h.hexdigest()
    if hash_calc == hash and authKey_local == authKey:
        return True
    else:
        abort(403, message="unathorized!")

def checkMasterAuth(body):
    try:
        if len(body['master_auth_key']) == 0:
            abort(403, message="unathorized!")
        else:
            if not(body['master_auth_key'] == config["MASTER_KEY"]):
                abort(403, message="unathorized!")
                return False
            return True
    except:
        abort(403, message="unathorized!")

def checkProcessorAuth(body):
    try:
        if len(body['request_processor_auth_key']) == 0:
            abort(403, message="unathorized!")
        else:
            if not(body['request_processor_auth_key'] == config["TX_PROCESSORKEY"]):
                abort(403, message="unathorized!")
                return False
            return True
    except:
        abort(403, message="unathorized!")
        

def checkParams(body):
    try:
        if len(body['params']) == 0:
            abort(400, message="params cannot be empty!")
        else:
            return body['params']
    except:
        abort(400, message="other parameters needed!")


def isValidAddress(address):
    try:
        if web3.isAddress(address):
            return address
        else:
            abort(400, message="invalid address (" + address + ") supplied!")
    except:
        abort(400, message="invalid address (" + address + ") supplied!")


def getBalanceOf(params):
    status = ""
    description = ""
    results = ""
    #addresses check
    addresses = list(map(lambda par : isValidAddress(par["address"]), params))
    try:
        balancesList = []
        if len(params) == 1:
            #use balanceOf
            address = addresses[0]
            balance = contract.functions.balanceOf(address, params[0]['tokenId']).call()
            resp = {
                "address" : address,
                "tokenId" : params[0]['tokenId'],
                "balance" : balance
            }
            balancesList.append(resp)
        else:
            #use balanceOfBatch
            tokensIds = list(map(lambda par : par["tokenId"], params))
            balances = contract.functions.balanceOfBatch(addresses, tokensIds).call()

            #build output array
            for i in range (0, len(balances), 1):
                resp = {
                    "address" : addresses[i],
                    "tokenId" : tokensIds[i],
                    "balance" : balances[i]
                }
                balancesList.append(resp)

        status = "OK"
        description = ""
        results = balancesList
        code = 200
    except Exception as e:
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code

def checkExistance(params):
    status = ""
    description = ""
    results = ""
    existances =[]
    try:
        tokensIds = params[0]['tokensIds']
        if len(tokensIds) == 0:
            status = "Error"
            description = "Missing tokens IDs"
            result = []
            code = 400
        else:
            for tk_id in tokensIds:       
                exist = contract.functions.checkExistance(tk_id).call()
                resp = {
                    "tokenId" : tk_id,
                    "existance" : exist==1
                }
                existances.append(resp)
        status = "OK"
        description = ""
        results = existances
        code = 200
    except Exception as e:
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def owner(params):
    status = ""
    description = ""
    results = ""
    owner =[]
    try:
        tokensIds = params[0]['tokensIds']
        if len(tokensIds) == 0:
            status = "Error"
            description = "Missing tokens IDs"
            result = []
            code = 400
        else:
            dbConnect()
            for tk_id in tokensIds:       
                sql = "SELECT owner FROM fc_token WHERE token_id = '" + str(tk_id) + "'"
                mycursor.execute(sql)
                res = mycursor.fetchall()
                ow = None
                if len(res)!=0:
                    ow = res[0]['owner']
                resp = {
                    "tokenId" : tk_id,
                    "owner" : ow
                }
                owner.append(resp)
            dbClose()
        status = "OK"
        description = ""
        results = owner
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def tokensOfAddress(params):
    status = ""
    description = ""
    results = ""
    tokensIDs =[]
    try:
        addresses = params[0]['addresses']
        if len(addresses) == 0:
            status = "Error"
            description = "Missing addresses"
            result = []
            code = 400
        else:
            dbConnect()
            for addr in addresses:       
                sql = "SELECT token_id, token_value FROM fc_token WHERE owner = '" + str(addr) + "' and burn_date IS NULL"
                mycursor.execute(sql)
                res = mycursor.fetchall()
                tk_list = []
                tk_val = []
                tk_total_value = 0
                for id in res:
                    tk_list.append(int(id['token_id']))
                    tk_val.append(int(id['token_value']))
                    tk_total_value += int(id['token_value'])
                resp = {
                    "address" : addr,
                    "tokensIds" : tk_list,
                    "tokensValues" : tk_val,
                    "tokensTotalValue" : tk_total_value
                }
                tokensIDs.append(resp)
            dbClose()
        status = "OK"
        description = ""
        results = tokensIDs
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def tokensHistory(params):
    status = ""
    description = ""
    results = ""
    history =[]
    try:
        tokensIds = params[0]['tokensIds']
        if len(tokensIds) == 0:
            status = "Error"
            description = "Missing tokens IDs"
            result = []
            code = 400
        else:
            dbConnect()
            for tk_id in tokensIds:   
                mint = []
                transfer = []
                burn = []    
                sql = "SELECT * FROM fc_log WHERE token_id = '" + str(tk_id) + "'"
                mycursor.execute(sql)
                res = mycursor.fetchall()
                for r in res:
                    if r['tx_from'] == '0x0000000000000000000000000000000000000000':
                        #mint
                        mint.append({
                            "timestamp" : str(r['tx_timestamp']),
                            "txHash" : r['tx_hash']
                        })

                    if r['tx_from'] != '0x0000000000000000000000000000000000000000' and r['tx_to'] != '0x0000000000000000000000000000000000000000':
                        #transfer
                        transfer.append({
                            "from" : r['tx_from'],
                            "to" : r['tx_to'],
                            "timestamp" : str(r['tx_timestamp']),
                            "txHash" : r['tx_hash']
                        })

                    if r['tx_to'] == '0x0000000000000000000000000000000000000000':
                        #burn
                        burn.append({
                            "timestamp" : str(r['tx_timestamp']),
                            "txHash" : r['tx_hash']
                        })
                history.append({
                    "tokenId" : tk_id,
                    "mint" : mint,
                    "transfers" : transfer,
                    "burn" : burn
                })            

            dbClose()
            status = "OK"
            description = ""
            results = history
            code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def getBaseURI(params):
    status = ""
    description = ""
    results = ""
    URIs = []
    try:
        tokensIds = params[0]['tokensIds']
        if len(tokensIds) == 0:
            status = "Error"
            description = "Missing tokens IDs"
            result = []
            code = 400
        else:
            baseURI = contract.functions.uri(0).call()
            for tk_id in tokensIds:       
                resp = {
                    "tokenId" : tk_id,
                    "URI" : baseURI.replace("{id}", str(tk_id))
                }
                URIs.append(resp)
            status = "OK"
            description = ""
            results = URIs
            code = 200
    except Exception as e:
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code

def getTokensList(params):
    status = ""
    description = ""
    results = ""
    try:
        type = params[0]['type']
        dbConnect()
        tokensIds = []
        if type == "minted":
            sql = "SELECT DISTINCT token_id FROM fc_token ORDER BY token_id"
        if type == "existing":
            sql = "SELECT DISTINCT token_id FROM fc_token WHERE burn_date IS NULL ORDER BY token_id"
        if type == "burned":
            sql = "SELECT DISTINCT token_id FROM fc_token WHERE burn_date IS NOT NULL ORDER BY token_id"
        if type != "minted" and type != "existing" and type != "burned":
            status = "Error"
            description = "Wrong filter parameter"
            result = []
            code = 400
        else:
            mycursor.execute(sql)
            res = mycursor.fetchall()
            dbClose()
            tokensIds.append({"tokensIds" : list(map(lambda par : int(par['token_id']), res))})
            status = "OK"
            description = ""
            results = tokensIds
            code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def broadcastTx(params):
    status = ""
    description = ""
    results = ""
    id = params[0]['id']
    txHex = params[0]['txHex']
    try:
        #'0xf9012a678502540a5ee0830f4240944ee72d96768f9aa2e1047f07a74d14991cec1bce80b8c4731133e9000000000000000000000000c679d778b948dc9e605f55438e3017f55bfbbcd10000000000000000000000000000000000000000000000000000001c38ce307c000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000003307830000000000000000000000000000000000000000000000000000000000029a0381a0d609f9311f64ec611e0103dc4149843336d26e48f2a309c5c6081b9901da00e7060ea74812d7b6d7980613e47a56b01b0cc943c3190824a3adde82d8e1f79'
        txHash = web3.eth.send_raw_transaction(txHex).hex()
        dbConnect()
        updateRequest(id, status = "broadcasted", txhash = txHash)
        dbClose()
        status = "OK"
        description = ""
        results = [{ "txHash" : str(txHash) }]
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def getAuxTxData(params):
    status = ""
    description = ""
    results = ""
    address = isValidAddress(params[0]['address'])
    gasPrice = params[0]['gasPrice'] #bool
    txCount = params[0]['txCount'] #bool
    type = params[0]['method']
    fromAddress = params[0]['fromAddress']
    toAddress = params[0]['toAddress']
    tokensIds = params[0]['tokensIds']
    qty = params[0]['qty']
    if params[0]['data'] is not None:
        data_string = ",".join(list(map(lambda intvalue : str(intvalue), params[0]['data'])))
    else:
        data_string = ""
    description = params[0]['aux_string']
    try:
        if gasPrice:
            print("Acquiring gasPrice...")
            try:
                #EIP 1559 from 2021_08_03 London HF 
                gasPrice = int(web3.eth.getBlock("latest").baseFeePerGas, base=16) #get last block fee and convert to decimal value
                gasPrice = gasPrice + web3.toWei(1, "gwei")
            except Exception:
                #Legacy
                gasPrice = web3.eth.generate_gas_price()
            print("Gas price -> " + str(web3.fromWei(gasPrice, "gwei")) + " gwei")
            
        else:
            gasPrice = 0

        if txCount: 
            print("Acquiring nonce...")
            txCount = web3.eth.get_transaction_count(address)
            print("Nonce -> " + str(txCount))
        else:
            txCount = 0
            
        print("Calculating gasLimit...")

        data = b'0x0'
        #prepare data to be write for mint function
        if type=="mint" or type=="mintBatch":
            data = web3.toHex(bytes(data_string, 'utf-8'))
            
        if type=="mint":
            tx_obj= contract.functions.mint(
                toAddress,
                tokensIds[0],
                qty[0],
                data
            )

        if type=="mintBatch":
            tx_obj = contract.functions.mintBatch(
                toAddress,
                tokensIds,
                qty,
                data
            )
        

        if type=="burn":
            tx_obj= contract.functions.burn(
                toAddress,
                tokensIds[0],
                qty[0]
            )
            
        if type=="burnBatch":
            tx_obj = contract.functions.burnBatch(
                toAddress,
                tokensIds,
                qty
            )


        if type=="safeTransferFrom":
            tx_obj= contract.functions.safeTransferFrom(
                fromAddress,
                toAddress,
                tokensIds[0],
                qty[0],
                b'0x0'
            )
            
        if type=="safeBatchTransferFrom":
            tx_obj = contract.functions.safeBatchTransferFrom(
                fromAddress,
                toAddress,
                tokensIds,
                qty,
                b'0x0'
            )

        if type=="setURI":
            tx_obj = contract.functions.setURI(
                description
            )

        if type=="addExistance":
            tx_obj = contract.functions.addExistance(
                tokensIds[0] #single
            )

        if type=="removeExistance":
            tx_obj = contract.functions.removeExistance(
                tokensIds[0] #single
            )

        gasLimit =  tx_obj.estimateGas({"from" : sc_admin}) #from field is mandatory
        print("Gas limit -> " + str(gasLimit) + " gwei")

        status = "OK"
        description = ""
        results = [{ "gasPrice" : gasPrice,  "txCount" : txCount, "gasLimit" : gasLimit}]
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def requestMintBurnTransfer(type, params):
    status = ""
    description = ""
    results = []
    #addresses check
    addresses_to = list(map(lambda par : isValidAddress(par["to"]), params))
    if type == "safeTransferFrom":
        addresses_to = list(map(lambda par : isValidAddress(par["from"]), params))
    try:
        burned = []
        minted = []
        toTransfer = []
        for par in params:
            if len(par["tokensIds"]) == 1:
                #request mint / burn / transfer
                if type == "mint":
                    tokensIds = str(par["tokensIds"][0]["id"])
                    values = str(par["tokensIds"][0]["value"])
                else:
                    tokensIds = str(par["tokensIds"][0])
                    values = "0"
                funcType = type
                qty=1
            else:
                #request mintBatch / burnBatch / transferBatch
                if type == "mint":
                    tokensIds = ",".join(list(map(lambda par : str(par["id"]), par["tokensIds"])))
                    values = ",".join(list(map(lambda par : str(par["value"]), par["tokensIds"])))
                else:
                    tokensIds = ",".join(list(map(lambda par : str(par), par["tokensIds"])))
                    values = ",".join(["0"]*len(par["tokensIds"]))
                if type == "safeTransferFrom":
                    funcType = "safeBatchTransferFrom"
                else:
                    funcType = type + "Batch"
                qty=",".join(["1"]*len(par["tokensIds"]))
            #Add request to db
            if type == "safeTransferFrom":
                tx_from = par["from"]
            else:
                tx_from = None
            sql = 'INSERT INTO requests (type, tx_from, tx_to, token_id, token_value, amount, status) VALUES(%s,%s,%s,%s,%s,%s,%s)'
            val = (funcType, tx_from, par["to"], tokensIds, values, qty, "queued")
            dbConnect()
            mycursor.execute(sql, val)
            mydb.commit()
            last_id =  mycursor.lastrowid
            dbClose()
            for tk_id in par["tokensIds"]:
                if type == "burn":
                    singleBurn = {
                        "tokenId" : tk_id,
                        "requestId" : last_id
                    }
                    burned.append(singleBurn)

                if type == "mint":
                    singleMint = {
                        "tokenId" : tk_id["id"],
                        "value" : tk_id["value"],
                        "requestId" : last_id
                    }
                    minted.append(singleMint)

                if type == "safeTransferFrom":
                    singleTransfer = {
                        "tokenId" : tk_id,
                        "requestId" : last_id
                    }
                    toTransfer.append(singleTransfer)

            if type == "burn":
                results.append({"burned" : burned})
            if type == "mint":
                results.append({"minted" : minted})
            if type == "safeTransferFrom":
                results.append({"toTransfer" : toTransfer})

        status = "OK"
        description = type + " operation enqueued"
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def mintBurnTransferStatus(type, params):
    status = ""
    description = ""
    results = []
    try:
        dbConnect()
        burned = []
        minted = []
        transferred = []
        for par in params:
            for reqId in par["requestsIds"]:
                mycursor.execute("SELECT type, tx_from, tx_to, token_id, token_value, amount, status, description, txhash FROM requests WHERE id = " +  str(reqId))
                res = mycursor.fetchall()
                if len(res) == 0:
                    req_status = ""
                    req_token_id = []
                    req_token_value = []
                    req_type = ""
                    tx_from = ""
                    tx_to = ""
                    txhash = ""
                else:
                    req_status = res[0]['status']
                    req_token_id = list(map(lambda tk_id : int(tk_id), res[0]['token_id'].split(",")))
                    req_token_value = list(map(lambda tk_id : int(tk_id), res[0]['token_value'].split(","))) if res[0]['token_value'] != None else "0"
                    req_type = res[0]['type']
                    tx_from = res[0]['tx_from']
                    tx_to = res[0]['tx_to']
                    txhash = ""  if res[0]['txhash'] == None else res[0]['txhash']
                #possibile status: queued - requested - signed - broadcasted - completed - failed
                timestamp = ""
                if req_status == "completed":
                    mycursor.execute("SELECT r.txhash, log.tx_timestamp FROM requests as r JOIN fc_log as log on r.txhash = log.tx_hash WHERE r.id = " +  str(reqId))
                    log_res = mycursor.fetchall()
                    if len(log_res) != 0:
                        timestamp = str(log_res[0]['tx_timestamp'])

                
                if type == "burnStatus" and (req_type == "burn" or req_type == "burnBatch"):
                    singleBurn = {
                        "status" : req_status,
                        "requestId" : reqId,
                        "tokensIds" : req_token_id,
                        "timestamp" : timestamp,
                        "txhash" : txhash
                    }
                    burned.append(singleBurn)

                if type == "mintStatus" and (req_type == "mint" or req_type == "mintBatch"):
                    token_ids_value_obj = list(map(lambda id, val : {"id" : id, "value" : val}, req_token_id, req_token_value))
                    singleMint = {
                        "status" : req_status,
                        "requestId" : reqId,
                        "to" : tx_to,
                        "tokensIds" : token_ids_value_obj,
                        "timestamp" : timestamp,
                        "txhash" : txhash
                    }
                    minted.append(singleMint)

                if type == "safeTransferFromStatus" and (req_type == "safeTransferFrom" or req_type == "safeBatchTransferFrom"):
                    singleTransf = {
                        "status" : req_status,
                        "requestId" : reqId,
                        "from" : tx_from,
                        "to" : tx_to,
                        "tokensIds" : req_token_id,
                        "timestamp" : timestamp,
                        "txhash" : txhash
                    }
                    transferred.append(singleTransf)

            if type == "burnStatus":
                results.append({"burned" : burned})
            if type == "mintStatus":
                results.append({"minted" : minted})
            if type == "safeTransferFromStatus":
                results.append({"transferred" : transferred})
        dbClose()
        status = "OK"
        description = ""
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }    
    
    return ret, code



def requestEditExistance(params):
    status = ""
    description = ""
    results = []
    try:
        added = []
        removed = []
        for par in params:
            try:
                tokenIds_add = par['add']
            except Exception:
                tokenIds_add = []

            try:
                tokenIds_remove = par['remove']
            except Exception:
                tokenIds_remove = []

            if len(tokenIds_add) == 0 and len(tokenIds_remove) == 0:
                status = "Error"
                description = "Missing token IDs"
                results = []
                code = 400
            else:
                dbConnect()
                for add in tokenIds_add:
                    #Add request to db
                    sql = 'INSERT INTO requests (type, token_id, status) VALUES(%s,%s,%s)'
                    val = ("addExistance", add, "queued")
                    mycursor.execute(sql, val)
                    mydb.commit()
                    last_id =  mycursor.lastrowid
                    singleAdd = {
                        "tokenId" : add,
                        "requestId" : last_id
                    }
                    added.append(singleAdd)

                for remove in tokenIds_remove:
                    #Add request to db
                    sql = 'INSERT INTO requests (type, token_id, status) VALUES(%s,%s,%s)'
                    val = ("removeExistance", remove, "queued")
                    mycursor.execute(sql, val)
                    mydb.commit()
                    last_id =  mycursor.lastrowid
                    singleRemove = {
                        "tokenId" : remove,
                        "requestId" : last_id
                    }
                    removed.append(singleRemove)
                
                dbClose()

                results.append({"added" : added})
                results.append({"removed" : removed})

        status = "OK"
        description = "editExistance operation enqueued"
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def editExistanceStatus(params):
    status = ""
    description = ""
    results = []
    try:
        added = []
        removed = []
        dbConnect()
        requestsIds = params[0]['requestsIds']
        if len(requestsIds) == 0:
            status = "Error"
            description = "Missing request IDs"
            results = []
            code = 400
        else:
            for reqId in requestsIds:
                mycursor.execute("SELECT type, status, token_id, txhash FROM requests WHERE id = " +  str(reqId))
                res = mycursor.fetchall()
                if len(res) == 0:
                    req_status = ""
                    req_token_id = ""
                    req_type = ""
                    txhash = ""
                else:
                    req_status = res[0]['status']
                    req_token_id = int(res[0]['token_id'])
                    req_type = res[0]['type']
                    txhash = ""  if res[0]['txhash'] == None else res[0]['txhash']
                    #possibile status: queued - requested - signed - broadcasted - completed - failed
                    timestamp = ""

                    if txhash != None and txhash != "":
                        #check if mined locally because setURI has no event logs
                        editExistance_status = web3.eth.get_transaction(txhash)
                        if editExistance_status['blockNumber'] is not None:
                            block_timestamp = web3.eth.getBlock(editExistance_status['blockNumber']).timestamp
                            #Query for table 'fc_log'
                            sql_log = """INSERT INTO fc_log (
                                tx_hash,
                                block_hash,
                                block_number,
                                tx_from,
                                tx_to,
                                token_id,
                                tx_timestamp
                                ) VALUES(%s, %s, %s, %s, %s, %s, %s)"""

                            print("Updating table 'fc_log'...")
                            val = (
                                editExistance_status['hash'].hex(),
                                editExistance_status['blockHash'].hex(), 
                                editExistance_status['blockNumber'],
                                editExistance_status['from'], 
                                editExistance_status['to'],
                                req_token_id,
                                datetime.datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                            )
                            mycursor.execute(sql_log, val)
                            mydb.commit()

                            print("Updating table 'requests'...")
                            sql_requests = "UPDATE requests SET status = 'completed' WHERE txhash = '" + editExistance_status['hash'].hex() + "'"
                            print(sql_requests)
                            mycursor.execute(sql_requests)
                            mydb.commit()
                            req_status = "completed"

                            if req_status == "completed":
                                mycursor.execute("SELECT r.txhash, log.tx_timestamp FROM requests as r JOIN fc_log as log on r.txhash = log.tx_hash WHERE r.id = " +  str(reqId))
                                log_res = mycursor.fetchall()
                                if len(log_res) != 0:
                                    timestamp = str(log_res[0]['tx_timestamp'])

                    if req_type == "addExistance":
                        added.append({
                            "status" : req_status,
                            "requestId" : reqId,
                            "tokenId" : req_token_id,
                            "timestamp" : timestamp,
                            "txhash" : txhash
                    })
                    
                    if req_type == "removeExistance":
                        removed.append({
                            "status" : req_status,
                            "requestId" : reqId,
                            "tokenId" : req_token_id,
                            "timestamp" : timestamp,
                            "txhash" : txhash
                    })

            results.append({"added" : added})
            results.append({"removed" : removed})
                
        dbClose()
        status = "OK"
        description = ""
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }    
    
    return ret, code



def requestSetBaseURI(params):
    status = ""
    description = ""
    results = []
    try:
        newURI = params[0]['newURI']
        if newURI == None or newURI == "" :
            status = "Error"
            description = "Wrong or no URI passed."
            code = 400
        else:
            #Add request to db
            sql = 'INSERT INTO requests (type, description, status) VALUES(%s,%s,%s)'
            val = ("setURI", newURI, "queued")
            dbConnect()
            mycursor.execute(sql, val)
            mydb.commit()
            last_id =  mycursor.lastrowid
            dbClose()
            results.append({
                    "requestId" : last_id
                })
        status = "OK"
        description = "setURI operation enqueued"
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def setBaseURIStatus(params):
    status = ""
    description = ""
    results = []
    try:
        dbConnect()
        requestsIds = params[0]['requestsIds']
        if len(requestsIds) == 0:
            status = "Error"
            description = "Missing request ID"
            results = []
            code = 400
        else:
            reqId = requestsIds[0]
            mycursor.execute("SELECT type, status, description, txhash FROM requests WHERE id = " +  str(reqId))
            res = mycursor.fetchall()
            if len(res) == 0:
                req_status = ""
                newURI = ""
                req_type = ""
                txhash = ""
            else:
                req_status = res[0]['status']
                newURI = res[0]['description']
                req_type = res[0]['type']
                txhash = ""  if res[0]['txhash'] == None else res[0]['txhash']
                #possibile status: queued - requested - signed - broadcasted - completed - failed
                timestamp = ""

                if txhash != None and txhash != "":
                    #check if mined locally because setURI has no event logs
                    setURI_status = web3.eth.get_transaction(txhash)
                    if setURI_status['blockNumber'] is not None:
                        block_timestamp = web3.eth.getBlock(setURI_status['blockNumber']).timestamp
                        #Query for table 'fc_log'
                        sql_log = """INSERT INTO fc_log (
                            tx_hash,
                            block_hash,
                            block_number,
                            tx_from,
                            tx_to,
                            tx_timestamp
                            ) VALUES(%s, %s, %s, %s, %s, %s)"""

                        print("Updating table 'fc_log'...")
                        val = (
                            setURI_status['hash'].hex(),
                            setURI_status['blockHash'].hex(), 
                            setURI_status['blockNumber'],
                            setURI_status['from'], 
                            setURI_status['to'],
                            datetime.datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        )
                        mycursor.execute(sql_log, val)
                        mydb.commit()

                        print("Updating table 'requests'...")
                        sql_requests = "UPDATE requests SET status = 'completed' WHERE txhash = '" + setURI_status['hash'].hex() + "'"
                        print(sql_requests)
                        mycursor.execute(sql_requests)
                        mydb.commit()
                        req_status = "completed"

            if req_status == "completed":
                mycursor.execute("SELECT r.txhash, log.tx_timestamp FROM requests as r JOIN fc_log as log on r.txhash = log.tx_hash WHERE r.id = " +  str(reqId))
                log_res = mycursor.fetchall()
                if len(log_res) != 0:
                    timestamp = str(log_res[0]['tx_timestamp'])

            if req_type == "setURI":
                results.append({
                    "status" : req_status,
                    "requestId" : reqId,
                    "newURI" : newURI,
                    "timestamp" : timestamp,
                    "txhash" : txhash
                })
                
        dbClose()
        status = "OK"
        description = ""
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }    
    
    return ret, code


def sendPayReceipt(params):
    status = ""
    description = ""
    results = []
    #addresses check
    addresses_to = list(map(lambda par : isValidAddress(par["payReceipts"][0]["to"]), params))
    try:
        toSend = []
        for par in params:
            for pr in par["payReceipts"]:
                #request send receipt
                tx_to = str(pr["to"])
                data = str(pr["data"])
                #Add request to db
                sql = 'INSERT INTO pay_receipts (tx_to, data, status) VALUES(%s,%s,%s)'
                val = (tx_to, data, "queued")
                dbConnect()
                mycursor.execute(sql, val)
                mydb.commit()
                last_id =  mycursor.lastrowid
                dbClose()
                singleSend = {
                    "to" : tx_to,
                    "data" : data,
                    "requestId" : last_id
                }
                toSend.append(singleSend)
        results.append({"toSend" : toSend})

        status = "OK"
        description = "Send pay receipt operation enqueued"
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code



def sendPayReceiptStatus(params):
    status = ""
    description = ""
    results = []
    try:
        dbConnect()
        sent = []
        for par in params:
            for reqId in par["requestsIds"]:
                mycursor.execute("SELECT tx_to, data, status, description, txhash FROM pay_receipts WHERE id = " +  str(reqId))
                res = mycursor.fetchall()
                if len(res) == 0:
                    req_status = ""
                    tx_to = ""
                    data = ""
                    txhash = ""
                else:
                    req_status = res[0]['status']
                    tx_to = res[0]['tx_to']
                    data = res[0]['data']
                    txhash = ""  if res[0]['txhash'] == None else res[0]['txhash']
                #possibile status: queued - requested - signed - broadcasted - completed - failed
                timestamp = ""
                if req_status == "completed":
                    mycursor.execute("SELECT txhash, tx_timestamp FROM pay_receipts WHERE id = " +  str(reqId))
                    log_res = mycursor.fetchall()
                    if len(log_res) != 0:
                        timestamp = str(log_res[0]['tx_timestamp'])

                singleSend = {
                    "status" : req_status,
                    "requestId" : reqId,
                    "to" : tx_to,
                    "data" : data,
                    "timestamp" : timestamp,
                    "txhash" : txhash
                }
                sent.append(singleSend)

            results.append({"receiptsSent" : sent})

        dbClose()
        status = "OK"
        description = ""
        code = 200

    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }    
    
    return ret, code

def getAuxReceiptTxData(params):
    status = ""
    description = ""
    results = ""
    gasPrice = params[0]['gasPrice'] #bool
    txCount = params[0]['txCount'] #bool
    fromAddress = params[0]['fromAddress']
    toAddress = params[0]['toAddress']
    data = params[0]['data']
    if params[0]['data'] is not None:
        data_string = params[0]['data']
    description = params[0]['aux_string']
    try:
        if gasPrice:
            print("Acquiring xDai gasPrice...")
            try:
                #EIP 1559 from 2021_08_03 London HF 
                gasPrice = int(xDai_web3.eth.getBlock("latest").baseFeePerGas, base=16) #get last block fee and convert to decimal value
                gasPrice = gasPrice + xDai_web3.toWei(1, "gwei")
            except Exception:
                #Legacy
                gasPrice = xDai_web3.eth.generate_gas_price()
            print("Gas price -> " + str(xDai_web3.fromWei(gasPrice, "gwei")) + " gwei")
            
        else:
            gasPrice = 0

        if txCount: 
            print("Acquiring nonce...")
            txCount = xDai_web3.eth.get_transaction_count(fromAddress)
            print("Nonce -> " + str(txCount))
        else:
            txCount = 0
            
        print("Calculating gasLimit...")

        data = xDai_web3.toHex(bytes(data_string, 'utf-8'))
            
        tx_obj = {
            'to': toAddress,
            'value' : 0,
            'gasPrice': gasPrice,
            'nonce' : txCount,
            'data' : xDai_web3.toHex(bytes(data, 'utf-8'))
        }

        gasLimit =  xDai_web3.eth.estimateGas(tx_obj)
        print("Gas limit -> " + str(gasLimit) + " gwei")

        status = "OK"
        description = ""
        results = [{ "gasPrice" : gasPrice,  "txCount" : txCount, "gasLimit" : gasLimit}]
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code


def broadcastReceiptTx(params):
    status = ""
    description = ""
    results = ""
    id = params[0]['id']
    txHex = params[0]['txHex']
    try:
        txHash = xDai_web3.eth.send_raw_transaction(txHex).hex()
        dbConnect()
        updateRequest(id, status = "broadcasted", txhash = txHash, table = "pay_receipts")
        dbClose()
        status = "OK"
        description = ""
        results = [{ "txHash" : str(txHash) }]
        code = 200
    except Exception as e:
        dbClose()
        status = "Error"
        description = str(e)
        results = []
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "description" : description,
        "results" : results
    }
        
    return ret, code

def getPendingReceiptsTxList() :
    mydb, mycursor = dbConnect(True)
    mycursor.execute("SELECT txhash FROM pay_receipts WHERE status='broadcasted' LIMIT 1")
    res = mycursor.fetchall()
    txHash = None
    if (len(res) > 0) :
        txHash = res[0]['txhash']
        print("Found broadcasted receipt tx with hash -> " + str(txHash))
    dbClose(mydb, mycursor)
    return txHash


def updateReceiptsTxStatus(txHash):
    #check if mined locally because setURI has no event logs
    try:
        tx_status = xDai_web3.eth.get_transaction(txHash)
    except:
        tx_status = None
    if tx_status is not None:    
        if tx_status['blockNumber'] is not None:
            mydb, mycursor = dbConnect(True)
            block_timestamp = xDai_web3.eth.getBlock(tx_status['blockNumber']).timestamp
            print("Updating table 'pay_receipts'...")
            sql_receipt = """UPDATE pay_receipts SET 
                status = 'completed',
                block_hash = %s,
                block_number = %s,
                tx_timestamp = %s
                WHERE txhash = %s"""
            val = (
                tx_status['blockHash'].hex(), 
                tx_status['blockNumber'],
                datetime.datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                tx_status['hash'].hex()
            )
        mycursor.execute(sql_receipt, val)
        mydb.commit()
        dbClose(mydb, mycursor)


def checkReceiptTxStatus():
    interval = int(config['RECEIPTS_TX_CHECK_INTERVAL'])
    txHash = ""
    while(True):
        try:
            print("Starting receipt tx checking...")
            checkForFailedTx()
            txHash = getPendingReceiptsTxList()
            if txHash is not None:
                updateReceiptsTxStatus(txHash)
            print("Completed, waiting next...")
            time.sleep(interval)
        except Exception as e:
            print("Error while checking receipt tx.\nDetails: " + str(e))
            time.sleep(interval)
            
def createWalletSFP():
    status = ""
    wallet = ""
    try:
        bip44_hdwallet.from_mnemonic(mnemonic=config['TEST_SEED'], language="english", passphrase=PASSPHRASE)
        bip44_hdwallet.clean_derivation()
        wallet = bip44_hdwallet.address()
        status = "OK"
        code = 200
    except Exception as e:
        status = "Error"
        code = 500
        print("ERROR: " + str(e))   

    ret = {
        "status" : status,
        "wallet" : wallet
    }
    return ret, code
# readonly request processing (only GET)
class readOnly(Resource):
    def get(self):
        method = request.headers.environ['REQUEST_URI'][1:]
        auth_key = request.headers.environ['HTTP_AUTHKEY']
        hash = request.headers.environ['HTTP_HASH']
        body_string = request.get_data().decode()
        #checkAuth(body_string, auth_key, hash)
        body = request.get_json(force=True)
        params = checkParams(body)
        if (method == "balanceOf"):
            return getBalanceOf(params)
        if (method == "tokensList"):
            return getTokensList(params)
        if (method == "baseURI"):
            return getBaseURI(params)
        if (method == "checkExistance"):
            return checkExistance(params)
        if (method == "tokensHistory"):
            return tokensHistory(params)
        if (method == "owner"):
            return owner(params)
        if (method == "tokensOfAddress"):
            return tokensOfAddress(params)


# writeOp request processing (only POST and correlated GET)
class writeOp(Resource):
    def get(self):
        method = request.headers.environ['REQUEST_URI'][1:]
        auth_key = request.headers.environ['HTTP_AUTHKEY']
        hash = request.headers.environ['HTTP_HASH']
        body_string = request.get_data().decode()
        #checkAuth(body_string, auth_key, hash)
        body = request.get_json(force=True)
        params = checkParams(body)
        if (checkMasterAuth(body)):
            if (method == "mintStatus" or method == "burnStatus" or method == "safeTransferFromStatus"):
                return mintBurnTransferStatus(method, params)
            if (method == "setBaseURIStatus"):
                return setBaseURIStatus(params)
            if (method == "editExistanceStatus"):
                return editExistanceStatus(params)
            if (method == "sendPayReceiptStatus"):
                return sendPayReceiptStatus(params)


    def post(self):
        method = request.headers.environ['REQUEST_URI'][1:]
        auth_key = request.headers.environ['HTTP_AUTHKEY']
        hash = request.headers.environ['HTTP_HASH']
        body_string = request.get_data().decode()
        #checkAuth(body_string, auth_key, hash)
        body = request.get_json(force=True)
        params = checkParams(body)
        if (checkMasterAuth(body)):
            if (method == "mint" or method == "burn" or method == "safeTransferFrom"):
                return requestMintBurnTransfer(method, params)
            if (method == "createWalletSFP"):
                return createWalletSFP()
            if (method == "setBaseURI"):
                return requestSetBaseURI(params)
            if (method == "editExistance"):
                return requestEditExistance(params)
            if (method == "sendPayReceipt"):
                return sendPayReceipt(params)




# writeOp request processing
class restricted(Resource):
    def post(self):
        if not (request.remote_addr in broadcastTxSourceAllowedIp):
            # if ip not in allowed list, response is 404
            abort(404)
        method = request.headers.environ['REQUEST_URI'][1:]
        auth_key = request.headers.environ['HTTP_AUTHKEY']
        hash = request.headers.environ['HTTP_HASH']
        body_string = request.get_data().decode()
        #checkAuth(body_string, auth_key, hash)
        body = request.get_json(force=True)
        if (checkProcessorAuth(body)):
            if (method == "broadcastTx"):
                params = checkParams(body)
                return broadcastTx(params)
            if (method == "broadcastReceiptTx"):
                params = checkParams(body)
                return broadcastReceiptTx(params)


    def get(self):
        if not (request.remote_addr in broadcastTxSourceAllowedIp):
            # if ip not in allowed list, response is 404
            abort(404)
        method = request.headers.environ['REQUEST_URI'][1:]
        auth_key = request.headers.environ['HTTP_AUTHKEY']
        hash = request.headers.environ['HTTP_HASH']
        body_string = request.get_data().decode()
        #checkAuth(body_string, auth_key, hash)
        body = request.get_json(force=True)
        if (checkProcessorAuth(body)):
            if (method == "auxTxData"):
                params = checkParams(body)
                return getAuxTxData(params)
            if (method == "auxReceiptTxData"):
                params = checkParams(body)
                return getAuxReceiptTxData(params)




# Actually setup the Api resource routing here
# Requests redirected to readonly class
api.add_resource(readOnly, '/balanceOf' ,'/checkExistance', '/tokensHistory', '/tokensList', '/baseURI', '/owner', '/tokensOfAddress')
api.add_resource(writeOp, '/editExistance' ,'/burn', '/mint', '/safeTransferFrom', '/setBaseURI', '/burnStatus', '/mintStatus', '/safeTransferFromStatus', '/setBaseURIStatus', '/editExistanceStatus','/sendPayReceipt','/sendPayReceiptStatus', '/createWalletSFP')
api.add_resource(restricted, '/auxTxData', '/broadcastTx', '/auxReceiptTxData', '/broadcastReceiptTx')


def checkForFailedTx():
    mydb, mycursor = dbConnect(True)
    mycursor.execute("SELECT txHash FROM pay_receipts WHERE status='broadcasted'")
    res = mycursor.fetchall()
    for item in res:
        try:
            #https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.get_transaction_receipt
            #status = 1 -> tx mined -> example -> 0x9e011defee701f591400ecd96a7566c080494c2b4b9cf7e7dff672398942e5f4
            #status = 0 -> tx failed -> example -> 0x2707a50c5e1c3692e7daa81476d0cf3b1d62f56cb4b66d68e2a0b2efe7f1d6f4 | 0x3685f7a182da7a90326ce41f040751bf775644bcc41e43e68bbf729606766e1a
            #If the transaction has not yet been mined throws web3.exceptions.TransactionNotFound.
            txHash = item['txHash']
            status = xDai_web3.eth.get_transaction_receipt(txHash)['status']
            if status == 0:
                #transaction failed -> write status to db
                print("Failed Tx found. Updating table 'pay_receipts'...")
                sql_requests = "UPDATE pay_receipts SET status = 'failed' WHERE txhash = '" + txHash + "'"
                mycursor.execute(sql_requests)
                mydb.commit()
        except Exception as e:
            #useless
            txHash = ""   
    dbClose(mydb, mycursor)




if __name__ == '__main__':
    print("Starting receipt tx checking thread..")
    thr = Thread(target = checkReceiptTxStatus)
    thr.start()
    print("Started.")

    app.run(debug=False, host='0.0.0.0', port=5555)
    