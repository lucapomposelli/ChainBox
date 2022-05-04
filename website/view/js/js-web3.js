/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */

//Global vars
const abi = JSON.parse('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"URI_SETTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"addExistance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"burnBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"checkExistance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"removeExistance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newuri","type":"string"}],"name":"setURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]');
const deployAddress = '0x63dE49a06B24a81bC314f62016ACC7f628983437';
account = '';

web3 = new Web3(Web3.givenProvider || 'https://ropsten.infura.io/v3/6efe4dc6516a44e89b3d38dd9e55141');
const ethEnabled = async () => {
    if (window.ethereum) {
        await window.ethereum.send('eth_requestAccounts');
        window.web3 = new Web3(window.ethereum);
        return true;
    }
    return false;
}

//https://docs.metamask.io/guide/getting-started.html
//https://medium.com/valist/how-to-connect-web3-js-to-metamask-in-2020-fee2b2edf58a
if (typeof window.ethereum !== 'undefined') {
    $('#btn_mmsk_connect').show();
} else {
    $('#btn_mmsk_install').show();
}
//Show nav buttons
$('.block__nav button').show();

$('#btn_mmsk_connect').click( function() {
    //Will start the MetaMask extension
    W3_getAccount();
});

window.ethereum.on('accountsChanged', function (account) {
    W3_refreshMmsk(account[0]);
});

async function W3_getAccount() {
    //Get MetaMask accounts
    const accounts = await ethereum.request({
        method: 'eth_requestAccounts'
    });
    account = accounts[0];

    W3_refreshMmsk(account);
}

function W3_refreshMmsk(account) {
    web3.eth.getBalance(account, function(err, result) {
        if (err) {
            console.log(err);
        } else {
            balance = (web3.utils.fromWei(result, 'ether')).substr(0, 8);
            $('#mmsk_balance').text(balance);
        }
    });

    shortWallet = jQuery.trim(account).substr(0, 10) + ' ... ' + account.substr(account.length - 10);
    $('#btn_mmsk_connect').attr('data-wallet', account).text(shortWallet);
    $('#alerts').html('');
}

wizard = new web3.eth.Contract(abi, deployAddress);

//https://web3js.readthedocs.io/en/v1.3.4/web3-eth-contract.html#methods-mymethod-send
async function W3_mint(pdf) {
    const whoMint = (cData2 === '') ? cData1 : cData2;

    wizard.methods.mint(
        whoMint.public_key, //Customer PK
        pdf[0], //PDFs hash
        1, //Quantity
        0x0, //Metadata
    ).send({
        from: account
    });
    
};

async function W3_mint_batch(pdfs, nTokens) {
    const whoMint = (cData2 === '') ? cData1 : cData2;

    wizard.methods.mintBatch(
        whoMint.public_key, //Customer PK
        pdfs, //PDFs hash
        nTokens, //Quantity
        0x0, //Metadata
    ).send({
        from: account
    });
};

async function W3_burn(id) {
    wizard.methods.burn(
        cData1.public_key, //Sender PK
        id[0], //Token id
        1, //Quantity
    ).send({
        from: account
    });
};

async function W3_burn_batch(ids, nTokens) {
    wizard.methods.burnBatch(
        cData1.public_key, //Customer PK
        ids, //PDFs hash
        nTokens, //Quantity
    ).send({
        from: account
    });
};

async function W3_transfer(id) {
    wizard.methods.safeTransferFrom(
        cData1.public_key, //Sender PK
        cData2.public_key, //Receiver PK
        id[0], //Token id
        1, //Quantity
        0x0, //Metadata
    ).send({
        from: account
    });
};

async function W3_transfer_batch(ids, nTokens) {
    wizard.methods.safeBatchTransferFrom(
        cData1.public_key, //Sender PK
        cData2.public_key, //Receiver PK
        ids, //Tokens ids
        nTokens, //Quantity
        0x0, //Metadata
    ).send({
        from: account
    })
};

//@TODO: Integrare prima di effettuare il mint per verificare disponibilità fondi
/*async function getBalance() {
    console.log(reqTokenID.value);
    
    //Contract call
    wizard.methods.balanceOf(reqAddress.value,reqTokenID.value).call(function (err, res) {
        console.log(res);
        if (err) {
            resp_span.innerHTML = "An error occured" + err;
            return
        }
        resp_span.innerHTML = "The balance is: " + res;
      })
}*/

/*
async function transferBatchToCustomer(sender,receiver,id_tokens,amounts) {

    //contract call
    let hash_transaction = "";
    let confirm_transaction = "";
    let transf_response = "";
    let transf_error = "";
    wizard.methods.safeBatchTransferFrom(
        sender,
        receiver,
        id_tokens,
        amounts, //qty
        0x0, //metadata
        ).send({
            from: "0xc679D778B948dC9e605F55438e3017f55Bfbbcd1"
        }).on('transactionHash', function(hash){
            hash_transaction=hash;
        }).on('confirmation', function(confirmationNumber, receipt){
            confirm_transaction=confirmationNumber;
        }).on('receipt', function(receipt){
            gReceipt = receipt;
            transf_response=JSON.stringify(receipt, undefined, 4);
        }).on('error', function(error, receipt){
            transf_error=error;
            gReceipt = receipt;
            transf_response=JSON.stringify(receipt, undefined, 4);
        })
};*/


// // using the event emitter
// myContract.methods.myMethod(123).send({from: '0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe'})
// .on('transactionHash', function(hash){
//     ...
// })
// .on('confirmation', function(confirmationNumber, receipt){
//     ...
// })
// .on('receipt', function(receipt){
//     // receipt example
//     console.log(receipt);
//     > {
//         "transactionHash": "0x9fc76417374aa880d4449a1f7f31ec597f00b1f6f3dd2d66f4c9c6c445836d8b",
//         "transactionIndex": 0,
//         "blockHash": "0xef95f2f1ed3ca60b048b4bf67cde2195961e0bba6f70bcbea9a2c4e133e34b46",
//         "blockNumber": 3,
//         "deployAddress": "0x11f4d0A3c12e86B4b5F39B213F7E19D048276DAe",
//         "cumulativeGasUsed": 314159,
//         "gasUsed": 30234,
//         "events": {
//             "MyEvent": {
//                 returnValues: {
//                     myIndexedParam: 20,
//                     myOtherIndexedParam: '0x123456789...',
//                     myNonIndexParam: 'My String'
//                 },
//                 raw: {
//                     data: '0x7f9fade1c0d57a7af66ab4ead79fade1c0d57a7af66ab4ead7c2c2eb7b11a91385',
//                     topics: ['0xfd43ade1c09fade1c0d57a7af66ab4ead7c2c2eb7b11a91ffdd57a7af66ab4ead7', '0x7f9fade1c0d57a7af66ab4ead79fade1c0d57a7af66ab4ead7c2c2eb7b11a91385']
//                 },
//                 event: 'MyEvent',
//                 signature: '0xfd43ade1c09fade1c0d57a7af66ab4ead7c2c2eb7b11a91ffdd57a7af66ab4ead7',
//                 logIndex: 0,
//                 transactionIndex: 0,
//                 transactionHash: '0x7f9fade1c0d57a7af66ab4ead79fade1c0d57a7af66ab4ead7c2c2eb7b11a91385',
//                 blockHash: '0xfd43ade1c09fade1c0d57a7af66ab4ead7c2c2eb7b11a91ffdd57a7af66ab4ead7',
//                 blockNumber: 1234,
//                 address: '0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe'
//             },
//             "MyOtherEvent": {
//                 ...
//             },
//             "MyMultipleEvent":[{...}, {...}] // If there are multiple of the same event, they will be in an array
//         }
//     }
// })
// .on('error', function(error, receipt) { // If the transaction was rejected by the network with a receipt, the second parameter will be the receipt.
//     ...
// });