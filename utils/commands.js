const truffleConfig = require("./truffle-config")

let wizard = await wizard.deployed()
//erc1155 haven't name and symbol

//standard interfaces
//https://docs.openzeppelin.com/contracts/3.x/api/token/erc1155#core

//as default truffle console operate only with accounts[0], then alla transaction will send from this account
//to use another account, add extra argument  {from: accounts[1]}  to the function call, to set from field
await wizard.safeTransferFrom(accounts[1],accounts[0],111,1,0x0, {from: accounts[1]}) //send 1x 111 token from account 1 to account 0

//mint single -> non-fungible token -> ERC721
//mint(address, tokenID, qty, data->set to 0x0)
await wizard.mint(accounts[0], 1234567890, 1, 0x0) //only contract deployer can mint

//mint multiple with same id -> fungible token -> ERC20
//mint(address, tokenID, qty, data->set to 0x0)
await wizard.mint(accounts[0], 987654321, 1000, 0x0)

//check balance of a specific address related to a specific token
//balanceOf(address, tokenID)
balance = await wizard.balanceOf(accounts[0], 1234567890)
balance.toNumber()

//check balance of multiple addresses for multiple or same token
//balanceOfBatch([address array], [token array])
balances = await wizard.balanceOfBatch([accounts[0],accounts[1]],[1234567890,987654321])
//can be used to detect all balance of all token from a single user
balances = await wizard.balanceOfBatch([accounts[0],accounts[0]],[1234567890,987654321])
//can be used to detect all balance of all user from a single token
balances = await wizard.balanceOfBatch([accounts[0],accounts[1]],[1234567890,1234567890])
//is useful to avoid implementation of a specific tracking function that will cost a lot of gas for each call
//https://ethereum.stackexchange.com/questions/92275/how-can-i-get-a-list-of-all-owners-of-an-erc1155-nft-by-using-a-web3-call
balances[0].toNumber()

//trasfer single
//safeTrasferFrom(addressFrom, addressTo, tokenID, qty, data->set to 0x0)
await wizard.safeTransferFrom(accounts[0],accounts[2],1234567890,1,0x0)

//transfer batch
await wizard.safeBatchTransferFrom(accounts[1],accounts[0],[1234567890,987654321],[1,1],0x0)

//get past events
// getPastEvents(eventName, blockinterval in json)
await wizard.getPastEvents("TransferBatch", {fromBlock: 0, toBlock: "latest"})

//getlist of minted token. getAllMintedTokens() not exist in the standard. workaround and opensae method decribed here
//https://ethereum.stackexchange.com/questions/94716/get-a-list-of-all-token-types-for-erc1155
//1) list all TransferSingle events -> 
let transferEvents = await wizard.getPastEvents('TransferSingle', { fromBlock: 0, toBlock: 'latest' });
//2) get the returnValues property and filter on the id field
transferEvents.returnValues
    Result {
        '0': '0x0d301CEfBe049FB32FA10239ab4D90027aA82d68',
        '1': '0x0000000000000000000000000000000000000000',
        '2': '0x0d301CEfBe049FB32FA10239ab4D90027aA82d68',
        '3': '1234567890',
        '4': '1',
        operator: '0x0d301CEfBe049FB32FA10239ab4D90027aA82d68', //who execute mint function
        from: '0x0000000000000000000000000000000000000000', //address that generate the token (0x0 is the base network address)
        to: '0x0d301CEfBe049FB32FA10239ab4D90027aA82d68', //destination address for the minted token
        id: '1234567890', //token id
        value: '1' //amount of generated token
    }

//get the basetoken uri
//uri(tokenID)
// https://docs.openzeppelin.com/contracts/3.x/api/token/erc1155#ERC1155-_setURI-string-
// https://eips.ethereum.org/EIPS/eip-1155#metadata
await wizard.uri(1234567890)

//set uri
//setURI("uri address") -> use {id}.json to follow the standard
//client have only to replay {id} with token id to get the files
await wizard.setURI("http://127.0.0.1:9000/json/{id}.json")

//approve
//approve methos allow an address defined as operator, to spend funds of another address, useful with thirdy part tool like opensea
//https://docs.openzeppelin.com/contracts/3.x/api/token/erc1155#IERC1155-setApprovalForAll-address-bool-
//wizard.setApprovalForAll(addressToAllow, bool(true or false))
await wizard.setApprovalForAll(accounts[2], true) //allow accounts[2] to spend funds of the caller account // addressToAllow cannot be the caller.
//check approval
//isApprovedForAll(account, addressToCheck) //return bool and say if addressToCheck can spend funds of account
await wizard.isApprovedForAll(accounts[0], accounts[2])
//if true, accounts[2] can spend accounts[0] funds






//to flattener contract
//npm install truffle-flattener
//.\node_modules\.bin\truffle-flattener .\contracts\wizard.sol > .\contracts\wizard_full.sol
//gives errors when loaded on remix

//fortunately remix can handle all openzeppelin libraries then we not have to flatter a contract
//simply copy wizard.sol content in remix and can deploy from there