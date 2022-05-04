#this daemon process pay_receipts and sign tx
import time
import datetime
import json
import mysql.connector
import requests
from hashlib import sha256

from web3 import Web3
from web3.types import SignedTx

web3 = Web3()
chainId = 100 #xDai mainnet

mydb = mycursor = ""
checkInterval = 10 #seconds

sc_admin = "0xc679D778B948dC9e605F55438e3017f55Bfbbcd1"

pkeys = {
    "0xc679D778B948dC9e605F55438e3017f55Bfbbcd1" : "aa4600e77c4f70cf0df8858753aed0165ec8f880b673d0607234dcd304c639f1"
}

hash_salt = "test_salt"
authKey = "test_key"
request_processor_auth_key = "tx_key"
broadcastTxApiUrl = "http://127.0.0.1:5000/broadcastReceiptTx"
auxTxdataApiUrl = "http://127.0.0.1:5000/auxReceiptTxData"

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


def getReceiptRequests() :
    mycursor.execute("SELECT id, tx_to, data, status, description, aux_details, txhash, block_hash, block_number FROM pay_receipts WHERE (txhash IS NULL or txhash='') AND status = 'requested' ORDER BY id ASC")
    res = mycursor.fetchall()
    print("\nFound " + str(len(res)) + " new requests.")
    return res


def updateRequest(id, status, description = None, aux_details = None):
    sql = 'UPDATE pay_receipts SET status = "' + status + '"'
    
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


def process(toAddress, data, description):
    global chainId
    #get nonce of sc_admin
    print("Acquiring nonce, gas price and calculating gasLimit...")
    gasPrice, nonce, gasLimit, status, mex = getReceiptAuxTxdata(sc_admin, toAddress, data, description)

    if status:
        #aux data acquired correctly
        print("Nonce -> " + str(nonce))
        print("Gas price -> " + str(web3.fromWei(gasPrice, "gwei")) + " gwei")
        print("Gas limit -> " + str(gasLimit) + " gwei")

        tx_obj = {
            'to': toAddress,
            'value' : 0,
            'gasPrice': gasPrice,
            'gas' : gasLimit,
            'nonce' : nonce,
            'data' : web3.toHex(bytes(data, 'utf-8'))
        }
      
        signed_txn = web3.eth.account.signTransaction(tx_obj, pkeys[sc_admin])

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


def getReceiptAuxTxdata(fromAddress, toAddress, data, aux_string = ""):
    #build request packet
    data = {
        "params" : [
            {
                "gasPrice" : True,
                "txCount" : True,
                "fromAddress" : fromAddress,
                "toAddress" : toAddress,
                "data" : data,
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
    mycursor.execute("SELECT COUNT(txhash) FROM pay_receipts WHERE status='broadcasted'")
    res = mycursor.fetchall()
    txNum = 0
    if (len(res) > 0) :
        txNum = res[0][0]
        print("Found " + str(txNum) + " broadcasted tx. Wait...")
    return txNum

def setTxAsRequested():
    mycursor.execute("UPDATE pay_receipts SET status='requested' WHERE status='queued' ORDER BY ID ASC LIMIT 1")


while(True) :
    try:
        dbConnect()

        #check for enqueued and broadcasted tx. 
        txNum = getBroadcastedTxList()
        if txNum == 0:
            #If no broadcasted status tx found set the first enqueued as 'Requested'
            setTxAsRequested()

        #Get unprocessed requests from db
        receiptRequests = getReceiptRequests()

        for req in receiptRequests:
            #validate field
            id, tx_to, data, status, description, aux_details, txhash, block_hash, block_number = req


            if tx_to is not None:
                tx_to = web3.toChecksumAddress(tx_to)
            
            signed_tx, error = process(tx_to, data, description)

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