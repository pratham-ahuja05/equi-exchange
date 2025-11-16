import { ethers } from 'ethers';

export const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || '';
export const SEPOLIA_RPC_URL = process.env.NEXT_PUBLIC_SEPOLIA_RPC_URL || 'https://sepolia.infura.io/v3/your-project-id';

// Contract ABI for EquiExchangeRecords
export const CONTRACT_ABI = [
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "_agreementHash",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "_partyA",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_partyB",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_price",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_quantity",
        "type": "uint256"
      }
    ],
    "name": "recordAgreement",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "_agreementHash",
        "type": "bytes32"
      }
    ],
    "name": "getAgreement",
    "outputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "agreementHash",
            "type": "bytes32"
          },
          {
            "internalType": "address",
            "name": "partyA",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "partyB",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "price",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "quantity",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct EquiExchangeRecords.Agreement",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "agreementHash",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "partyA",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "partyB",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "price",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "quantity",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      }
    ],
    "name": "AgreementRecorded",
    "type": "event"
  }
];

export const getContract = (provider: ethers.Provider) => {
  return new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
};

export const getContractWithSigner = (signer: ethers.Signer) => {
  return new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);
};
