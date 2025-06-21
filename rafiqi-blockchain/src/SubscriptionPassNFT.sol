// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SubscriptionPassNFT is ERC721, Ownable {
    uint256 private _tokenIds;
    mapping(address => uint256) public addressToTokenId;

    // Berikan initialOwner ke Ownable
    constructor(address initialOwner)
        ERC721("Rafiqi Subscription Pass", "RSP")
        Ownable(initialOwner)
    {}

    function mint(address to) external onlyOwner returns (uint256) {
        require(balanceOf(to) == 0, "Already owns pass");

        _tokenIds++;
        uint256 newTokenId = _tokenIds;

        addressToTokenId[to] = newTokenId;
        _mint(to, newTokenId);

        return newTokenId;
    }

    function _update(
        address to,
        uint256 tokenId,
        address auth
    ) internal override returns (address from) {
        from = super._update(to, tokenId, auth);

        // Hanya izinkan minting (from == address(0)) atau burning (to == address(0))
        if (from != address(0) && to != address(0)) {
            revert("Soulbound: non-transferable");
        }
    }
}