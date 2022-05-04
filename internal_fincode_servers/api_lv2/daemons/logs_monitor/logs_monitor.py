from logging import exception
import re
import time
import datetime
import json
from eth_typing.encoding import Primitives
import mysql.connector

from web3 import Web3
from web3._utils.events import get_event_data
from web3._utils.filters import construct_event_filter_params

# .env usage
from dotenv import dotenv_values
config = dotenv_values(".env")

try:
    with open(config["ABI_FILE"]) as f:
        info_json = json.load(f)
    abi = info_json["abi"]
except Exception as e:
    print("Cannot load ABI.\nDetails: " + str(e))
    exit()

infuraEndpoint = config["ETH_ENDPOINT"]
contractAddress = config["CONTRACT"]

web3 = Web3(Web3.HTTPProvider(infuraEndpoint))
contract = web3.eth.contract(address=contractAddress, abi=abi)

mydb = mycursor = ""
checkInterval = int(config["CHECKINTERVAL"])

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
        host = config["DB_HOST"],
        port = config["DB_PORT"],
        user = config["DB_USER"],
        password = config["DB_PW"],
        database = config["DB"],
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

#ref -> https://ethereum.stackexchange.com/questions/51637/get-all-the-past-events-of-the-contract/87209
def fetch_events(event, argument_filters = None, from_block = None, to_block = "latest", address = None, topics = None) :
    """Get events using eth_getLogs API.

    This is a stateless method, as opposite to createFilter and works with
    stateless nodes like QuikNode and Infura.

    :param event: Event instance from your contract.events
    :param argument_filters:
    :param from_block: Start block. Use 0 for all history/
    :param to_block: Fetch events until this contract
    :param address:
    :param topics:
    :return:
    """

    if from_block is None :
        raise TypeError("Missing mandatory keyword argument to getLogs: from_Block")

    abi = event._get_event_abi()
    abi_codec = event.web3.codec

    #Set up any indexed event filters if needed
    argument_filters = dict()
    _filters = dict(**argument_filters)
    data_filter_set, event_filter_params = construct_event_filter_params(
        abi,
        abi_codec,
        contract_address = event.address,
        argument_filters = _filters,
        fromBlock = from_block,
        toBlock = to_block,
        address = address,
        topics = topics,
    )

    #Call node over JSON-RPC API
    logs = event.web3.eth.getLogs(event_filter_params)

    #Convert raw binary event data to easily manipulable Python objects
    data=[]
    for entry in logs:
        data = get_event_data(abi_codec, abi, entry)
        yield data
    return data

def getLastBlock(eType) :
    mycursor.execute("SELECT block_number FROM fc_log WHERE event_type='" + eType + "' ORDER BY block_number DESC LIMIT 1")
    res = mycursor.fetchall()

    blockN = 0
    if (len(res) > 0) :
        blockN = res[0][0]

    print("\n" + eType + " - Last 'block_number' -> " + str(blockN))
    return blockN

def getLastSerialNumber() :
    # mycursor.execute(
    #     "SELECT fc1.serial_number FROM fc_token as fc1 WHERE fc1.mint_date = " +
    #     "(SELECT MAX(fc2.mint_date) FROM fc_token as fc2 WHERE fc1.serial_number = fc2.serial_number)" +
    #     " AND fc1.burn_date IS NOT NULL ")
    # res = mycursor.fetchall()

    # if (len(res) != 0) :
    #     return res[0][0]

    mycursor.execute("SELECT DISTINCT MAX(serial_number) FROM fc_token")
    res = mycursor.fetchall()
    
    if (res[0][0] == None) :    
        return 1
    
    return res[0][0] + 1

def getIdTokenByTokenId(tokenID) :
    mycursor.execute("SELECT token_id FROM fc_token WHERE token_id='" + str(tokenID) + "'")
    res = mycursor.fetchall()

    # print(res)
    idToken = res[0][0]
    print("INFO: 'token_id' -> " + str(idToken))
    return idToken

def getUnloggableTxList() :
    mycursor.execute("SELECT txhash, type, token_id FROM requests WHERE (type='setURI' OR type='addExistance' OR type='removeExistance') and status='broadcasted' LIMIT 1")
    res = mycursor.fetchall()

    txHash = None
    type = None
    tokenId = None
    if (len(res) > 0) :
        txHash = res[0][0]
        type = res[0][1]
        tokenId = res[0][2]
        print("Found broadcasted unloggable tx with hash -> " + str(txHash))
    return txHash, type, tokenId

def updateUnlogabbleTxStatus(txHash, type, req_token_id):
    #check if mined locally because setURI has no event logs
    tx_status = web3.eth.get_transaction(txHash)
    if tx_status['blockNumber'] is not None:
        block_timestamp = web3.eth.getBlock(tx_status['blockNumber']).timestamp
        if type == 'setURI':
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
                tx_status['hash'].hex(),
                tx_status['blockHash'].hex(), 
                tx_status['blockNumber'],
                tx_status['from'], 
                tx_status['to'],
                datetime.datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            )
        
        if type == 'addExistance' or type == 'removeExistance':
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
                tx_status['hash'].hex(),
                tx_status['blockHash'].hex(), 
                tx_status['blockNumber'],
                tx_status['from'], 
                tx_status['to'],
                req_token_id,
                datetime.datetime.fromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            )

        mycursor.execute(sql_log, val)
        mydb.commit()

        print("Updating table 'requests'...")
        sql_requests = "UPDATE requests SET status = 'completed' WHERE txhash = '" + tx_status['hash'].hex() + "'"
        mycursor.execute(sql_requests)
        mydb.commit()


def checkForFailedTx():
    mycursor.execute("SELECT txHash FROM requests WHERE status='broadcasted'")
    res = mycursor.fetchall()
    for item in res:
        try:
            #https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.get_transaction_receipt
            #status = 1 -> tx mined -> example -> 0x9e011defee701f591400ecd96a7566c080494c2b4b9cf7e7dff672398942e5f4
            #status = 0 -> tx failed -> example -> 0x2707a50c5e1c3692e7daa81476d0cf3b1d62f56cb4b66d68e2a0b2efe7f1d6f4 | 0x3685f7a182da7a90326ce41f040751bf775644bcc41e43e68bbf729606766e1a
            #If the transaction has not yet been mined throws web3.exceptions.TransactionNotFound.
            txHash = item[0]
            status = web3.eth.get_transaction_receipt(txHash)['status']
            if status == 0:
                #transaction failed -> write status to db
                print("Failed Tx found. Updating table 'requests'...")
                sql_requests = "UPDATE requests SET status = 'failed' WHERE txhash = '" + txHash + "'"
                mycursor.execute(sql_requests)
                mydb.commit()
        except Exception as e:
            #useless
            txHash = ""

def addEventToDB(ev, timestamp) :      
    # AttributeDict({
    #   'args': AttributeDict({
    #       'operator': '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1',
    #       'from': '0x0000000000000000000000000000000000000000', 
    #       'to': '0x10B6F68Ac2aA703Ad1E74BFAbC4414ecCce356dF', 
    #       'id': 1234567890,
    #       'value': 1
    #   }),
    #   'event': 'TransferSingle', 
    #   'logIndex': 0, 'transactionIndex': 1, 
    #   'transactionHash': HexBytes('0x54fb1949f47bfa00164199e068a530c657c6c38168904bb4568c7d24c48b4e22'), 
    #   'address': '0x761e944C30a6c6c2BD12400fc3cE0c8D2C5943e9', 
    #   'blockHash': HexBytes('0x944ca0bc01655fbc1bcb90673b324b337141ae79dde98b5aa00a593756b7989d'), 
    #   'blockNumber': 10404042
    # })

    # AttributeDict({
    #     'args': AttributeDict({
    #         'operator': '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', 
    #         'from': '0x0000000000000000000000000000000000000000', 
    #         'to': '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', 
    #         'ids': [98765, 4321], 
    #         'values': [1, 1]
    #     }), 
    #     'event': 'TransferBatch', 
    #     'logIndex': 50, 
    #     'transactionIndex': 26, 
    #     'transactionHash': HexBytes('0x7027a10d65a2a11b051095bd2e76d6b538ea7c43865df8e2071b5fe480cdba5f'), 
    #     'address': '0x761e944C30a6c6c2BD12400fc3cE0c8D2C5943e9', 
    #     'blockHash': HexBytes('0x53de1a199298fa007e1fa39ecc7711db1fd43c92f68055ba2e20e53654a8603b'), 
    #     'blockNumber': 10492908
    # })

    #Query for table 'fc_token'
    sql_mint = """INSERT INTO fc_token (
        token_id,
        token_value,
        serial_number,
        owner,
        mint_date
    ) VALUES(%s, %s, %s, %s, %s)"""

    sql_token_exist = """SELECT COUNT(token_id)
        FROM fc_token 
        WHERE token_id = '%s'"""

    sql_token_update_date_mint = """UPDATE fc_token SET mint_date = %s , owner = %s WHERE token_id = %s"""

    #Query for table 'fc_token'
    sql_burn = """UPDATE fc_token SET 
        burn_date = %s , 
        owner = %s 
        WHERE token_id = %s"""

    #Query for table 'fc_token'
    sql_transfer = """UPDATE fc_token SET 
        owner = %s 
        WHERE token_id = %s"""

    #Query for table 'fc_log'
    sql_log = """INSERT INTO fc_log (
        tx_hash,
        block_hash,
        block_number,
        token_id,
        token_value,
        amount,
        tx_operator,
        tx_from,
        tx_to,
        tx_timestamp,
        event_type
        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    tx = web3.eth.get_transaction(ev.transactionHash.hex())
    raw_data = contract.decode_function_input(tx.input)
    try:
        # (<Function mint(address,uint256,uint256,bytes)>, {'account': '0x10B6F68Ac2aA703Ad1E74BFAbC4414ecCce356dF', 'id': 1234567890, 'amount': 1, 'data': b'\x00'})
        raw_data_string = raw_data[1]['data'].decode("utf-8")
    except Exception:
        raw_data_string = None


    if (e.event == "TransferSingle") :
        tokenID = [ev.args.id]
        values = [ev.args.value]
        if  raw_data_string is not None:
            token_val = [raw_data_string.split(",")[0]]
        else:
            token_val = ["0"]


    if (e.event == "TransferBatch") :
        tokenID = ev.args.ids
        values = ev.args.values
        if  raw_data_string is not None:
            token_val = raw_data_string.split(",")
        else:
            token_val = ["0"]*len(tokenID)

    for i in range(0, len(tokenID), 1) :
        print("\nSTART - Writing transaction: " + ev.transactionHash.hex())
        
        #Is mint event?
        if (e.args.__getitem__("from") == "0x0000000000000000000000000000000000000000") :
            print("Mint event found. Updating table 'fc_token'...")
            mycursor.execute(sql_token_exist, (tokenID[i], ))
            res = mycursor.fetchall()
            if (res[0][0] == 1) :
                val = (
                    datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    ev.args.to,
                    tokenID[i]
                )
                mycursor.execute(sql_token_update_date_mint, val)
                mydb.commit()
            else :
                try:
                    token_val[i] = int(token_val[i])
                except:
                    token_val[i] = 0
                val = (
                    tokenID[i],
                    token_val[i],
                    getLastSerialNumber(),
                    ev.args.to,
                    datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                )
                mycursor.execute(sql_mint, val)
                mydb.commit()

        #Is burn event?
        if (e.args.__getitem__("to") == "0x0000000000000000000000000000000000000000") :
            print("Burn event found. Updating table 'fc_token'...")
            val = (
                datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                ev.args.to,
                str(tokenID[i]),
            )
            mycursor.execute(sql_burn, val)
            mydb.commit()

        #Is transfer event?
        if (e.args.__getitem__("from") != "0x0000000000000000000000000000000000000000" and e.args.__getitem__("to") != "0x0000000000000000000000000000000000000000") :
            print("Transfer event found. Updating table 'fc_token'...")
            val = (
                ev.args.to,
                str(tokenID[i]),
            )
            mycursor.execute(sql_transfer, val)
            mydb.commit()        

        #Update log table
        print("Updating table 'fc_log'...")
        try:
            token_val[i] = int(token_val[i])
        except:
            token_val[i] = 0
        val = (
            ev.transactionHash.hex(),
            ev.blockHash.hex(), 
            ev.blockNumber,
            tokenID[i],
            token_val[i],
            values[i],
            ev.args.operator,
            e.args.__getitem__("from"), # e.args.from -> not valid -> from is method
            ev.args.to,
            datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            ev.event
        )
        mycursor.execute(sql_log, val)
        mydb.commit()

        print("Updating table 'requests'...")
        sql_requests = "UPDATE requests SET status = 'completed' WHERE txhash = '" + ev.transactionHash.hex() + "'"
        mycursor.execute(sql_requests)
        mydb.commit()

        print("END - Writing transaction")

while(True) :
    try:
        dbConnect()

        #check for failed transactions
        checkForFailedTx()

        #Get last TransferSingle block checked from db
        fromBlock = getLastBlock('TransferSingle') + 1
        print("TransferSingle - Events search from 'block_number': " + str(fromBlock) + "...")
        
        #Get TransferSingle events
        events = list(fetch_events(contract.events.TransferSingle, from_block=fromBlock, to_block="latest"))
        print("TransferSingle - Events found: " + str(len(events)))

        for e in events:
            timestamp = web3.eth.getBlock(e.blockNumber).timestamp
            addEventToDB(e, timestamp)

        #Get last TransferBatch block checked from db
        fromBlock = getLastBlock('TransferBatch') + 1
        print("TransferBatch - Events search from 'block_number': " + str(fromBlock) + "...")
        
        #Get TransferBatch events
        events = list(fetch_events(contract.events.TransferBatch, from_block=fromBlock, to_block="latest"))
        print("TransferBatch - Events found: " + str(len(events)))

        for e in events:
            timestamp = web3.eth.getBlock(e.blockNumber).timestamp
            addEventToDB(e, timestamp)
        
        
        #check if a uloggable tx in broadcasted status exist (setExistance, setURI)
        txHash, type, req_token_id = getUnloggableTxList()
        if txHash != None:
            #found tx to check
            updateUnlogabbleTxStatus(txHash, type, req_token_id)
            
        dbClose()


    except Exception as e:
        print("ERROR: " + str(e))
    
    countdown(checkInterval)