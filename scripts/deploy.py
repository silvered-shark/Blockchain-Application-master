from scripts.utils import get_account, get_contract, OPENSEA_URL, uploadImg_IPFS
from brownie import accounts, config, send_ETH, send_NFT
import brownie.network as network

"""
To deploy a contract, you will need an account from which to deploy.
This can be done using brownie. After creating an account run the following script in shell-

brownie run scripts/deploy.py --network rinkeby

We are using the rinkeby test network provided by Infura.io. 

***DO NOT RUN ANY BROWNIE SCIPTS THROUGH PYTHON AS IT WILL NOT RECOGNIZE THE SYNTAX.***
"""

def deploy():
    account = get_account(id="your_account_name")
    send_nft = send_NFT.deploy(
        {"from": account}
    )
    send_eth = send_ETH.deploy(
        get_contract("eth_usd_price_feed").address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print("Deployed Successfully!!")

def main():
    deploy()