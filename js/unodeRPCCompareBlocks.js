const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

// nodes URLs
const unodeURL = process.env.UNODE_URL;
const rpcURL = process.env.RPC_URL;

// JSON-RPC request body
const requestBody = {
    jsonrpc: '2.0',
    method: 'eth_blockNumber',
    params: [],
    id: 1
};

// Function to make a JSON-RPC request to an Ethereum node
const getBlockNumber = async (nodeUrl) => {
    try {
        const response = await axios.post(nodeUrl, requestBody);
        const blockNumberHex = response.data.result;
        const blockNumberDecimal = parseInt(blockNumberHex, 16);
        return blockNumberDecimal;
    } catch (error) {
        console.error(`Error getting block number from ${nodeUrl}:`, error);
        throw error;
    }
};

// Function to get block numbers from both nodes and log the results
const getAndCompareBlockNumbers = async () => {
    try {
        const blockNumber1 = await getBlockNumber(unodeURL);
        const blockNumber2 = await getBlockNumber(rpcURL);
        const time = new Date();
        console.log(`Block number from UNode: ${blockNumber1}  / Block number from RPC: ${blockNumber2} / Difference: ${blockNumber2 - blockNumber1} time: ${time}`);
    } catch (error) {
        console.error('Error getting block numbers:', error);
    }
};

getAndCompareBlockNumbers();