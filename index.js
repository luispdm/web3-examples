const web3 = require('web3');

console.log(web3.eth.accounts.create());

// get web3 account from private key
// let pK = '0x...';
// console.log(web3.eth.accounts.privateKeyToAddress(pK));
