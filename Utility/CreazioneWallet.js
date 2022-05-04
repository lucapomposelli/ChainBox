const Web3API = require('web3');
    const main = () => {
    const web3 = new Web3API(new Web3API.providers.HttpProvider('https://ropsten.infura.io'));
    let account = web33.eth.accounts.create(web33.utils.randomHex(32));
    let wallet = web33.eth.accounts.wallet.add(account);
    let keystore = wallet.encrypt(web33.utils.randomHex(32));
    console.log({
        account: account,
        wallet: wallet,
        keystore: keystore
    });
};
main();