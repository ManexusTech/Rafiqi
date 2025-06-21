// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Subscription Contract
/// @author Goenawan
/// @notice Kontrak ini digunakan untuk sistem langganan berbasis durasi harian.
/// @dev Menggunakan pembayaran ETH untuk memperpanjang masa langganan.

import "./SubscriptionPassNFT.sol";

contract Subscription {
    /// @notice Menyimpan waktu berakhir langganan tiap pengguna.
    mapping(address => uint256) public subscriptionExpiry;

    /// @notice Harga per hari langganan dalam ETH.
    uint256 public pricePerDay = 0.001 ether;

    /// @notice Melakukan langganan dengan membayar ETH sesuai jumlah hari.
    /// @param daysToSubscribe Jumlah hari langganan yang ingin dibeli.
    /// @dev Jika user belum berlangganan, dihitung dari sekarang; jika masih aktif, ditambah durasi.
    function subscribe(uint256 daysToSubscribe) external payable {
        require(msg.value >= pricePerDay * daysToSubscribe, "Insufficient payment");
        if (block.timestamp > subscriptionExpiry[msg.sender]) {
            subscriptionExpiry[msg.sender] = block.timestamp + daysToSubscribe * 1 days;
        } else {
            subscriptionExpiry[msg.sender] += daysToSubscribe * 1 days;
        }
    }

    /// @notice Mengecek apakah pengguna masih dalam masa langganan aktif.
    /// @param user Alamat pengguna yang ingin dicek.
    /// @return Boolean true jika langganan masih aktif.
    function isSubscribed(address user) external view returns (bool) {
        return subscriptionExpiry[user] > block.timestamp;
    }
}
