const web3 = require('web3');

const ownerAddress = '0x399e18eE7168B06B37bdA87Faa9a8A4147CD4e13';  // replace with your contract address
const methodSignature = web3.eth.abi.encodeFunctionSignature('balanceOf(address)');
const encodedAddress = web3.eth.abi.encodeParameter('address', ownerAddress);
const encodedFunctionCall = methodSignature + encodedAddress.slice(2);

// const tokenId = '27317269254130722282651374643077502699886158991487809237418337964212284949309';
// const methodSignature = web3.eth.abi.encodeFunctionSignature('tokenURI(uint256)');
// const encodedTokenId = web3.eth.abi.encodeParameter('uint256', tokenId);
// const encodedFunctionCall = methodSignature + encodedTokenId.slice(2);

console.log(encodedFunctionCall);