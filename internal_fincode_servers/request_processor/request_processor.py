#this daemon process requests and sign txs
import time
import datetime
import json
import mysql.connector
import requests
from hashlib import sha256

from web3 import Web3
from web3.types import SignedTx

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"MINTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"URI_SETTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"burnBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"checkExistance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"addExistance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"removeExistance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newuri","type":"string"}],"name":"setURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true}]')

contractAddress = "0x465bE4152Bdd8E97cB9c312Ed3fe03Bec339DBD4"

web3 = Web3()
contract = web3.eth.contract(address=contractAddress, abi=abi)
chainId = 100 #ropsten

mydb = mycursor = ""
checkInterval = 10 #seconds

sc_admin = "0xc679D778B948dC9e605F55438e3017f55Bfbbcd1"

pkeys = {
    "0xc679D778B948dC9e605F55438e3017f55Bfbbcd1" : "aa4600e77c4f70cf0df8858753aed0165ec8f880b673d0607234dcd304c639f1"
}

hash_salt = "test_salt"
authKey = "test_key"
request_processor_auth_key = "tx_key"
broadcastTxApiUrl = "http://127.0.0.1:5000/broadcastTx"
auxTxdataApiUrl = "http://127.0.0.1:5000/auxTxData"

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Next check in " + timer, end="\r")
        time.sleep(1)
        t -= 1

#FinCode database connection
def dbConnect() :
    global mydb
    global mycursor
    print("\nWaiting for FinCode database connection...")
    mydb = mysql.connector.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        password = "local_pass",
        database = "fincode_internal"
    )
    #Only this particular cursor will buffer results
    mycursor = mydb.cursor(buffered = True)
    print("INFO: Database connected!")

#FinCode database disconnection
def dbClose() :
    print("\nWaiting for FinCode database disconnection...")
    mycursor.close()
    mydb.close()
    print("INFO: Database disconnected!\n")


def getScrequests() :
    mycursor.execute("SELECT * from requests WHERE (txhash IS NULL or txhash='') AND status = 'requested' ORDER BY id ASC")
    res = mycursor.fetchall()
    print("\nFound " + str(len(res)) + " new requests.")
    return res


def updateRequest(id, status, description = None, aux_details = None):
    sql = 'UPDATE requests SET status = "' + status + '"'
    
    if description is not None:
        sql = sql +  ', description = "' + description + '"'

    if aux_details is not None:
        sql = sql +  ', aux_details = "' + aux_details + '"'
            
    sql = sql + ' WHERE id = "' + str(id) + '"'

    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    print("\nTx with id = " + str(id) + " updated.")
    return True


def process(type, fromAddress, toAddress, tokensIds, tokenValues, qty, description):
    global chainId
    #get nonce of sc_admin
    print("Acquiring nonce, gas price and calculating gasLimit...")
    gasPrice, nonce, gasLimit, status, mex = getAuxTxdata(sc_admin, type, fromAddress, toAddress, tokensIds, qty, tokenValues, description)

    if status:
        #aux data acquired correctly
        print("Nonce -> " + str(nonce))
        print("Gas price -> " + str(web3.fromWei(gasPrice, "gwei")) + " gwei")
        print("Gas limit -> " + str(gasLimit) + " gwei")

        data = b'0x0'
        #prepare data to be write for mint function
        if type=="mint" or type=="mintBatch":
            data_string = ",".join(list(map(lambda intvalue : str(intvalue), tokenValues)))
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

        #https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.send_transaction
        #https://blog.infura.io/london-fork/
        #https://github.com/ethereum/web3.py/issues/2054
        txn = tx_obj.buildTransaction({
            'chainId': chainId,
            'gas': gasLimit,
            'nonce': nonce,

            #LEGACY
            'gasPrice': gasPrice, 

            #EIP 1559 from 2021_08_03 London HF Require connection
            # 'maxFeePerGas': web3.toWei(100, 'gwei'),
            # 'maxPriorityFeePerGas': web3.toWei(5, 'gwei'),
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=pkeys[sc_admin])
        print("Transaction build complete.")
        return signed_txn, ""
    else:
        #error while acquiring aux data
        return "", mex



def sendBroadcastTxRequest(id, signed_tx):
    #build request packet
    data = {
        "params" : [
            {
                "id" : id,
                "txHex" : signed_tx
            }
        ],
        "request_processor_auth_key" : request_processor_auth_key
    }
    data_json = json.dumps(data)
    #calculate hash of data (sha256)
    h=sha256()
    h.update((data_json + hash_salt).encode())
    hash=h.hexdigest()
    headers = {
        "Content-Type" : "application/json",
        "authKey" : authKey,
        "hash" : hash
    }
    print("Calling broadcast api...")
    try:
        r = requests.post(broadcastTxApiUrl, data_json, headers=headers)
        result = r.json()
        print(result)
        if result['status'] == "OK":
            return True
        else:
            return False
    except Exception as e:
        print("ERROR: " + str(e))


def getAuxTxdata(address, method, fromAddress, toAddress, tokensIds, qty, aux_data, aux_string):
    #build request packet
    data = {
        "params" : [
            {
                "address" : address,
                "gasPrice" : True,
                "txCount" : True,
                "method" : method,
                "fromAddress" : fromAddress,
                "toAddress" : toAddress,
                "tokensIds" : tokensIds,
                "qty" : qty,
                "data" : aux_data,
                "aux_string" : aux_string
            }
        ],
        "request_processor_auth_key" : request_processor_auth_key
    }
    data_json = json.dumps(data)
    #calculate hash of data (sha256)
    h=sha256()
    h.update((data_json + hash_salt).encode())
    hash=h.hexdigest()
    headers = {
        "Content-Type" : "application/json",
        "authKey" : authKey,
        "hash" : hash
    }
    print("Calling getAuxData api...")
    try:
        r = requests.get(auxTxdataApiUrl, data = data_json, headers=headers)
        result = r.json()
        print(result)
        if result['status'] == "OK":
            gasPrice = result['results'][0]['gasPrice']
            txCount = result['results'][0]['txCount']
            gasLimit = result['results'][0]['gasLimit']
            
            return gasPrice, txCount, gasLimit, True, ""
        else:
            return 0, 0, 0, False, result['description'].replace("'", "''").replace('\\', '\\\\').replace('"', '""')
    except Exception as e:
        error = "ERROR: " + str(e)
        print(error)
        return 0, 0, 0, False, error



def getBroadcastedTxList():
    mycursor.execute("SELECT COUNT(txhash) FROM requests WHERE status='broadcasted'")
    res = mycursor.fetchall()
    txNum = 0
    if (len(res) > 0) :
        txNum = res[0][0]
        print("Found " + str(txNum) + " broadcasted tx. Wait...")
    return txNum

def setTxAsRequested():
    mycursor.execute("UPDATE requests SET status='requested' WHERE status='queued' ORDER BY ID ASC LIMIT 1")


while(True) :
    try:
        dbConnect()

        #check for enqueued and broadcasted tx. 
        txNum = getBroadcastedTxList()
        if txNum == 0:
            #If no broadcasted status tx found set the first enqueued as 'Requested'
            setTxAsRequested()

        #Get unprocessed requests from db
        scRequests = getScrequests()

        for req in scRequests:
            #validate field
            id, op, tx_operator_address, tx_operator_id, fromAddress, toAddress, tokensIds, tokenValues, qtys, status, description, txhash, aux_details = req

            if fromAddress is not None:
                fromAddress = web3.toChecksumAddress(fromAddress)

            if toAddress is not None:
                toAddress = web3.toChecksumAddress(toAddress)
            
            #get tokens id in int array format
            if tokensIds is not None:
                tokensIds = list(map(lambda tokenId : int(tokenId), tokensIds.split(",")))
            if tokenValues is not None:
                tokenValues = list(map(lambda tokenValue : int(tokenValue), tokenValues.split(",")))
            if qtys is not None:
                qtys = list(map(lambda qty : int(qty), qtys.split(",")))
            
            signed_tx, error = process(op, fromAddress, toAddress, tokensIds, tokenValues, qtys, description)

            if signed_tx != "":
                #signed process ok
                tx_json=json.dumps(signed_tx.rawTransaction.hex())
                #web3.eth.send_raw_transaction(signed_tx.rawTransaction) 
                print(tx_json)
                updateRequest(id, "signed")
                sendBroadcastTxRequest(id, signed_tx.rawTransaction.hex())
            else:
                #error in signing process
                #set request as failed
                updateRequest(id, "failed", aux_details = error)


        dbClose()
    except Exception as e:
        print("ERROR: " + str(e))
    
    countdown(checkInterval)
    #time.sleep(checkInterval)