// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Reputation Scoring Contract
/// @author Goenawan 
/// @notice Kontrak ini menyimpan dan mengelola skor reputasi pengguna.
/// @dev Hanya admin yang dapat menambah skor reputasi.

contract Reputation {
    /// @notice Menyimpan skor reputasi untuk tiap alamat.
    mapping(address => uint256) public reputationScore;

    /// @notice Alamat admin yang berhak mengubah skor reputasi.
    address public admin;

    /// @notice Constructor untuk menetapkan admin.
    constructor() {
        admin = msg.sender;
    }

    /// @notice Menambahkan skor reputasi ke pengguna tertentu.
    /// @param user Alamat pengguna.
    /// @param score Jumlah skor reputasi yang ingin ditambahkan.
    function increaseReputation(address user, uint256 score) external {
        require(msg.sender == admin, "Only admin");
        reputationScore[user] += score;
    }

    /// @notice Mengambil nilai reputasi pengguna.
    /// @param user Alamat pengguna.
    /// @return Nilai reputasi pengguna tersebut.
    function getReputation(address user) external view returns (uint256) {
        return reputationScore[user];
    }
}
