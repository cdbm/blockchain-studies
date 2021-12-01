from brownie import network, accounts, MockV3Aggregator
from brownie.network.web3 import Web3
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
FORK_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local-2"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORK_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.load("freecodecamp-account")


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed")
