from dotenv import load_dotenv
import os
from web3 import Web3, HTTPProvider
import random

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


def make_rpc_call(node_rpc, private_key, contract_address, abi, method_name, *args):
    # Initialize a Web3 instance
    w3 = Web3(HTTPProvider(node_rpc))

    # For networks like Binance Smart Chain, you might need the following middleware
    # w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Ensure connection to node is successful
    print("Checking if connection to node is successful...")
    assert w3.is_connected() , "Failed to connect to the Ethereum node"
    print("Connection to node successful!")

    # Set up the account from the private key
    account = w3.eth.account.from_key(private_key)

    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Construct the transaction
    print("Setting up transaction...")
    transaction = contract.functions[method_name](*args).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        # Additional transaction parameters may be needed, like 'gas' and 'gasPrice'
    })

    # Sign the transaction
    print("Signing transaction...")
    # Sign the transaction
    signed_txn = account.sign_transaction(transaction)

    print("Transcation signed")
    # Send the signed transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Raw transaction sent, starting waiting for receipt...")

    # Wait for the transaction to be mined
    transaction_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print("Transaction receipt")

    # Extract token ID from the transaction receipt if necessary
    # This assumes the Minted event is the first log in the receipt logs
    # You'll need to adjust the index and decoding if it's not
    return transaction_receipt, w3



def main():
    print("Loading env variables...")
    public_key, private_key, laos_collection_contract, laos_rpc, token_uri = get_env_variables()
    _to = public_key  # The destination address

    print("Env variables loaded!")
    print("Generating random number...")
    _slot = random.randint(0, 2**96 - 1)  # This generates a random uint96
    _tokenURI = token_uri 
    print(f"Random number generated: {_slot}")

    print("Making RPC call...")
    transaction_receipt, w3 = make_rpc_call(
        laos_rpc,
        private_key,
        laos_collection_contract,
        abi,
        'mintWithExternalURI',
        _to,
        _slot,
        _tokenURI
    )

    # Extract token ID from the transaction receipt if necessary
    # The token ID is the return value of the mintWithExternalURI function
    # Decode the returned value from the transaction receipt
    # Decode the returned value from the transaction receipt
    print("Extracting token ID from the transaction receipt...")
    contract_instance = w3.eth.contract(abi=abi, address=laos_collection_contract)
    # If the event `MintedWithExternalURI` is not triggered, this will cause an error
    token_id_event = contract_instance.events.MintedWithExternalURI().process_receipt(transaction_receipt)
    print("TokenID extracted from receipt")

    if token_id_event:
        token_id = token_id_event[0]['args']['_tokenId']
        print(f"Minted token ID: {token_id}")
    else:
        print("No MintedWithExternalURI event found in the transaction receipt.")


if __name__ == "__main__":
    main()
