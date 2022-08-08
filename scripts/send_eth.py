from scripts.utils import get_account, get_contract
from brownie import config, accounts
from brownie import send_ETH
import brownie.network as network
from decimal import Decimal
from web3 import Web3

"""
Only run this after the contract is deployed!
To run this type the following in shell-

brownie run scripts/send_eth.py --network rinkeby
"""

def send_eth(
    sender: str,
    reciever: str,
    value: float
    )-> int:

    account = accounts.add(sender)
    account1 = accounts.at(reciever, force=True)
    send = send_ETH[-1] #uses latest deployed contract if multiple contracts deployed with same account

    #we send a little more wei for gas purposes
    value = Web3.toWei(Decimal(value), 'ether') + 350000000

    if value < send.get_min_txn():
        return 0

    print("Before")
    print(f"Balance of sender: {account.balance()}")
    print(f"Balance of reciever: {account1.balance()}")

    tx = send.send_ether(account1, {"from": account, "value": value}) #this sends the actual ether to the account
    tx.wait(1)
    print("done!")
    print("After")
    print(f"Balance of sender: {account.balance()}")
    print(f"Balance of reciever: {account1.balance()}")

    return 1

def main():
    send_eth()