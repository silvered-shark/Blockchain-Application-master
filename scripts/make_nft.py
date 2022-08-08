from scripts.utils import get_account, OPENSEA_URL, uploadImg_IPFS
from brownie import send_NFT, accounts

"""
Only run this after the contract is deployed!
To run this type the following in shell-

brownie run scripts/make_nft.py --network rinkeby 
"""

def mintNFT(path_name, nft_title, nft_desc, nft_auth):
    title = nft_title  #takes location of file with extension
    desc = nft_desc #a short description on the file
    account = accounts.add(nft_auth)
    location = path_name
    
    print()
    print("File is getting uploaded!")
    token_uri = uploadImg_IPFS(title, desc, location)
    # this function uploads the file to IPFS and produces a hash which is then passed internally 
    # to upload_metadata which uploads the metadata to IPFS and finally returns the IPFS hash of 
    # the metadata


    print(token_uri)
    print("File uploaded successfully!")
    print()
    send_nft = send_NFT[-1]
    print("File now minting!")
    #tokenURI obtained from uploadImg_IPFS is passed to the contract
    tx = send_nft.makeToken(token_uri, {"from": account})
    tx.wait(1)
    print(f"You can view your NFT at {OPENSEA_URL.format(send_nft.address, send_nft._tokenIds() - 1)}") #address to view the nft after it executes
    return f"{OPENSEA_URL.format(send_nft.address, send_nft._tokenIds() - 1)}", send_nft._tokenIds() - 1

def main():
    mintNFT()