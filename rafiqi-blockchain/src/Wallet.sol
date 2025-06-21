// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Wallet Assistant Contract for ETH Transfer Utility
/// @author Goenawan 
/// @notice Kontrak pembantu untuk mentransfer ETH ke alamat lain.
/// @dev Fungsi sederhana untuk demonstrasi transfer ETH.

contract WalletAssistant {
    /// @notice Mentransfer ETH ke alamat tujuan.
    /// @param to Alamat tujuan yang menerima ETH.
    /// @dev Fungsi ini harus dipanggil dengan mengirimkan ETH bersama transaksi.
    function transferETH(address payable to) external payable {
        require(msg.value > 0, "No ETH sent");
        to.transfer(msg.value);
    }
}
