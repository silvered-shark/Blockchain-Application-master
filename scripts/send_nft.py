from scripts.utils import OPENSEA_URL
from brownie import send_NFT, accounts

"""
Only run this after the contract is deployed!
To run this type the following in shell-

brownie run scripts/send_nft.py --network rinkeby
"""

def send_token(det1, det2, det3):
    account_sender = accounts.add(det1) #sender private key is required
    account_reciever = accounts.at(det2, force=True) #receivers public key is required
    _tokenID = det3 #the tokenID is printed in console and in the GUI after an nft is minted
    send_nft = send_NFT[-1]
    print("Transferring token!")
    tx = send_nft.sendToken(account_reciever, _tokenID, {"from": account_sender})
    tx.wait(1)
    print(f"Done! You can view your NFT at {OPENSEA_URL.format(send_nft.address, _tokenID)}")
    return f"{OPENSEA_URL.format(send_nft.address, _tokenID)}"

def main():
    send_token()