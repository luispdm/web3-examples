const ethers = require('ethers');
const contractABI = require('./ERC721Enumerable.json');

// This script allows sending web3 requests via the ethers library: https://www.npmjs.com/package/ethers
// The uses the contract calls "supportsInterface" and "balanceOf"

const providerURL = 'https://rpc-mumbai.maticvigil.com';
const contractAddress = '0x4A81A22ad1e0434732d9d925598246762e87154F';
const accountAddress = '0x399e18eE7168B06B37bdA87Faa9a8A4147CD4e13';

// The interface ID you want to check. Replace with your actual value.
const interfaceId = '0x780e9d63';
const provider = new ethers.JsonRpcProvider(providerURL, 80001, {
  // staticNetwork: ethers.Network.from(80001),
  // batchMaxSize: 1,
});

provider.on('debug', (info) => {
  if (info.action === 'sendRpcPayload') console.log(info.payload);
});
const contract = new ethers.Contract(contractAddress, contractABI, provider);

async function checkSupportsInterface() {
  try {
      const result = await contract.supportsInterface(interfaceId);
      console.log(`The contract supports the interface: ${result}`);
      return result;
  } catch (error) {
      console.error('Error:', error);
  }
}

async function checkBalanceOf() {
  try {
      const balance = await contract.balanceOf(accountAddress);
      console.log(`Balance of the address is: ${balance.toString()}`);
      return balance;
  } catch (error) {
      console.error('Error:', error);
  }
}

(async () => {
  const res = await checkSupportsInterface();
  const b = await checkBalanceOf();
  console.log(res);
  console.log(b);
  console.log('Done');
})();