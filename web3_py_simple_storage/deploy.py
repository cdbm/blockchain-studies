from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os

install_solc("0.6.0")

with open("../contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

complied_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(complied_sol, file)

bytecode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/96ba97eb48b1453f8791f32032deca48")
)
chainId = 4
my_address = "0x7D3cd7c54f37b22B5edfC3F742aFe373bb4B69e7"
private_key = os.getenv("METAMASK_RINKEBY_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainId, "from": my_address, "nonce": nonce}
)

print("Deploying contract...")

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!!")

# WORKING WITH THE CONTRACT
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())

print("Updating Contract")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chainId, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=send_store_tx)

print("Updated!!")
print(simple_storage.functions.retrieve().call())
