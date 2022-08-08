from brownie import accounts, config, MockV3Aggregator, Contract
import brownie.network as network
import requests, json

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index= None, id= None):
    """
    This function returns an account based on which network we are on.
    If network is a development network then it returns an account on 
    our local machine which is not persistent.
    If network is testnet then it returns a pre-created account with 
    custom settings.
    """
    if index:
        return accounts[index]
    if id:
            return accounts.load(id)        
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract,
    and return that mock contract.
        Args:
            contract_name(string)
        
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            #if we dont have a previosly used mock then this will deploy a new one
            deploy_mocks()
        #this reuses the previously used mock 
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    
    return contract

DECIMALS=8
INITIAL_VALUE = 200000000000

def deploy_mocks(decimals= DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(
        decimals,
        initial_value, 
        {"from":account}
        )
    print("Deployed!!")


def uploadImg_IPFS(name, desc, location):
    """
    Takes image, name and description as input and uploads it to IPFS 
    and then passes the returned hash to function uploadMetadata which creates the metadata
    and returns the hash of the metadata.
    """
    data = open(location,"rb").read()
    endpoint = 'https://api.nft.storage/upload'
    headers = {
    "Authorization": "Bearer **authorization bearer key here**" #make a new authorization key by logging in to nft.storage
    }
    resp = requests.post(endpoint, headers=headers, data=data) #stores the value in the filecoin distributed storage service and returns a hash
    formt = resp.json()
    cid_val = "https://ipfs.io/ipfs/" + str(formt["value"]["cid"]) 
    met = {}
    met["name"] = name
    met["description"] = desc
    met["image"] = cid_val
    metadata_location = ''.join(location.split('.')[0:-1])+'-metadata.json'
    with open(metadata_location,"w") as outfile:
        json.dump(met, outfile)
    
    return upload_metadata(open(metadata_location,"r").read())

def upload_metadata(data):
    endpoint = 'https://api.nft.storage/upload'
    headers = {
    "Authorization": "Bearer **authorization bearer key here**" #make a new authorization key by logging in to nft.storage
    }
    resp = requests.post(endpoint, headers=headers, data=data)
    formt = resp.json()
    cid_val = "https://ipfs.io/ipfs/" + str(formt["value"]["cid"])
    return cid_val