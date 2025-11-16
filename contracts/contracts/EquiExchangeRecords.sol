// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract EquiExchangeRecords {
    struct Agreement {
        bytes32 agreementHash;
        address partyA;
        address partyB;
        uint256 price;
        uint256 quantity;
        uint256 timestamp;
    }
 
    mapping(bytes32 => Agreement) public agreements;

    event AgreementRecorded(
        bytes32 indexed agreementHash,
        address indexed partyA,
        address indexed partyB,
        uint256 price,
        uint256 quantity,
        uint256 timestamp
    );

    function recordAgreement(
        bytes32 _agreementHash,
        address _partyA,
        address _partyB,
        uint256 _price,
        uint256 _quantity
    ) public {
        require(agreements[_agreementHash].timestamp == 0, "Agreement already exists");

        agreements[_agreementHash] = Agreement({
            agreementHash: _agreementHash,
            partyA: _partyA,
            partyB: _partyB,
            price: _price,
            quantity: _quantity,
            timestamp: block.timestamp
        });

        emit AgreementRecorded(
            _agreementHash,
            _partyA,
            _partyB,
            _price,
            _quantity,
            block.timestamp
        );
    }

    function getAgreement(bytes32 _agreementHash) public view returns (Agreement memory) {
        return agreements[_agreementHash];
    }
}
