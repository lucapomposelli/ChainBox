//load web3
var Web3 = require('web3')

//define infura endpoint
var infura_end = "";
//connect to endpoint
var web3 = new Web3(new Web3.providers.HttpProvider(infura_end));

//load abi from file
var fs = require('fs');
var jsonFile = "../build/contracts/wizard.json";
var parsed= JSON.parse(fs.readFileSync(jsonFile));
var abi = parsed.abi;
var address = "0x761e944C30a6c6c2BD12400fc3cE0c8D2C5943e9"

//contract instance
var wizard= new web3.eth.Contract(abi, address);

//request past events
(async () => {
    events = await wizard.getPastEvents(
        'TransferSingle',
        {
            fromBlock: 0,
            toBlock: 'latest'
        }
    );
    console.log(events); 
} )()

