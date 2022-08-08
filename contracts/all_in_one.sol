// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract send_ETH {
    //usd_min_txn has the minimum amount of dollars one has to send
    uint256 public usd_min_txn; 
    AggregatorV3Interface internal eth_usd_conv;

    constructor(
        address _priceFeedAddress
        ) public{
        usd_min_txn = 10 * (10 ** 18);
        eth_usd_conv = AggregatorV3Interface(_priceFeedAddress);
    }

    function send_ether(
        address payable recipient
        ) public payable{
        //this require statement checks if the amount we are sending 
        //is actually greater than the minimum amount required by us!
        require(msg.value >= get_min_txn(), "You need to send atleast $10 worth of ETH");
        recipient.transfer(msg.value);
    }

    function get_min_txn() public view returns (uint256) {
        (,
        int price
        ,,,
        ) = eth_usd_conv.latestRoundData();
        uint256 new_price = uint256(price) * 10 ** 10;
        uint256 min_to_send = (usd_min_txn * 10 ** 18) / new_price;
        return min_to_send;
    }
}

contract send_NFT is ERC721URIStorage {
   using Counters for Counters.Counter;
    Counters.Counter public _tokenIds;

    constructor() ERC721("CustomNFT", "CNFT") {}

    function makeToken(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newItemId = _tokenIds.current();
        _safeMint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);
        
        _tokenIds.increment();

        return newItemId;
    }

    function sendToken(address to, uint256 _tokenId) public returns (uint256){
        require(msg.sender == ownerOf(_tokenId), "Not owner of this token!");
        safeTransferFrom(msg.sender, to, _tokenId);

        return _tokenId;
    }
}