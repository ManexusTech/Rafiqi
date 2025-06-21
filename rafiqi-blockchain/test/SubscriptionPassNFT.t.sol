// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/SubscriptionPassNFT.sol";

contract SubscriptionPassNFTTest is Test {
    SubscriptionPassNFT public nft;
    address public owner = address(this);
    address public user = address(0x1234);

    function setUp() public {
        nft = new SubscriptionPassNFT(owner);
    }

    function testMintNFT() public {
        uint256 tokenId = nft.mint(user);
        assertEq(nft.ownerOf(tokenId), user);
        assertEq(nft.balanceOf(user), 1);
        assertEq(nft.addressToTokenId(user), tokenId);
    }

    function testOnlyOwnerCanMint() public {
          vm.expectRevert(
            abi.encodeWithSelector(Ownable.OwnableUnauthorizedAccount.selector, address(0x1))
        );
        vm.prank(address(0x1));
        nft.mint(user);
    }

    function testCannotMintTwice() public {
        nft.mint(user);
        vm.expectRevert("Already owns pass");
        nft.mint(user);
    }

    function testCannotTransferNFT() public {
        uint256 tokenId = nft.mint(user);

        vm.startPrank(user);
        vm.expectRevert("Soulbound: non-transferable");
        nft.transferFrom(user, address(0x2), tokenId);
        vm.stopPrank();
    }

    function testBurnNFT() public {
        uint256 tokenId = nft.mint(user);
        vm.startPrank(user);
        vm.expectRevert("Soulbound: non-transferable");
        nft.transferFrom(user, address(0x2), tokenId); // Coba transfer -> gagal
        vm.stopPrank();
    }
}