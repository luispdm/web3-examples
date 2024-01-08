from dotenv import load_dotenv
import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import random

# Define the number of assets to create
number_of_assets = 500  # Change this to create more or fewer assets


# Load the environment variables from .env file
load_dotenv()
abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_to", "type": "address"},
            {"internalType": "uint96", "name": "_slot", "type": "uint96"},
            {"internalType": "string", "name": "_tokenURI", "type": "string"}
        ],
        "name": "mintWithExternalURI",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "_to", "type": "address"},
            {"indexed": False, "internalType": "uint96", "name": "_slot", "type": "uint96"},
            {"indexed": False, "internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "_tokenURI", "type": "string"}
        ],
        "name": "MintedWithExternalURI",
        "type": "event"
    }
]


# Access the environment variables
def get_env_variables():
    public_key = os.getenv('PUBLIC_KEY')
    private_key = os.getenv('PRIVATE_KEY')
    laos_collection_contract = os.getenv('LAOS_COLLECTION_CONTRACT')
    laos_rpc = os.getenv('LAOS_RPC')
    token_uri = os.getenv('TOKEN_URI')
    return public_key, private_key, laos_collection_contract, laos_rpc, token_uri


def make_rpc_call(nonce, node_rpc, private_key, contract_address, abi, method_name, *args):
    # Initialize a Web3 instance
    w3 = Web3(HTTPProvider(node_rpc))

    # Ensure connection to node is successful
    print("Checking if connection to node is successful...")
    assert w3.is_connected(), "Failed to connect to the Ethereum node"
    print("Connection to node successful!")

    # Set up the account from the private key
    account = w3.eth.account.from_key(private_key)

    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Construct the transaction
    print("Setting up transaction...")
    transaction = contract.functions[method_name](*args).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 50000,
        'gasPrice': w3.to_wei(1, 'gwei'),
    })

    # Sign the transaction
    print("Signing transaction...")
    # Sign the transaction
    signed_txn = account.signTransaction(transaction)
    print("Transcation signed")

    # Send the signed transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Convert transaction hash to hexadecimal string
    txn_hash_hex = txn_hash.hex()

    print("Returning txn_hash_hex: ", txn_hash_hex)
    return txn_hash_hex, w3



def main():
    # Load environment variables
    print("Loading env variables...")
    public_key, private_key, laos_collection_contract, laos_rpc, token_uri = get_env_variables()
    print("Env variables loaded!")

    # Initialize Web3 instance outside the loop to use the same instance for all calls
    w3 = Web3(HTTPProvider(laos_rpc))
    assert w3.is_connected(), "Failed to connect to the Ethereum node"

    # Set up the account from the private key
    account = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)

    # Loop to create assets
    for i in range(number_of_assets):
        print(f"Creating asset {i+1}/{number_of_assets}")

        # Generate a random uint96 value for the slot
        _slot = random.randint(0, 2**96 - 1)
        print(f"Random slot generated: {_slot}")

        print("Stargint with nonce: ",nonce)
        _tokenURI = f"{token_uri}_{i}"

        # Make the RPC call to mint the asset
        print("Making RPC call...")
        transaction_hex, w3 = make_rpc_call(nonce,
            laos_rpc,
            private_key,
            laos_collection_contract,
            abi,
            'mintWithExternalURI',
            public_key,  # The destination address
            _slot,
            _tokenURI
        )
        nonce = nonce +1
        # time.sleep(1)

if __name__ == "__main__":
    main()
