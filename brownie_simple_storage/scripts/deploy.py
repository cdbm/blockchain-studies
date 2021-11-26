from brownie import accounts, SimpleStorage, network
from dotenv import load_dotenv

load_dotenv()


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.load("freecodecamp-account")


def main():
    deploy_simple_storage()
    print("Hello World!")
