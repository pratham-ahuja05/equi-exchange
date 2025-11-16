'use client';

import { useState } from 'react';
import { useAccount, useContractWrite, useWaitForTransaction } from 'wagmi';
import { getContractWithSigner, CONTRACT_ADDRESS } from '@/lib/contract';
import { getEtherscanUrl, formatAddress } from '@/lib/utils';
import { ArrowLeft, ExternalLink, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface AgreementDisplayProps {
  agreement: any;
  address: string;
  onNewNegotiation: () => void;
}

export function AgreementDisplay({ agreement, address, onNewNegotiation }: AgreementDisplayProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [txHash, setTxHash] = useState<string | null>(null);
  const [isRecorded, setIsRecorded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { write, data: hash, isLoading: isPending, error: writeError } = useContractWrite({
    address: CONTRACT_ADDRESS as `0x${string}`,
    abi: [
      {
        "inputs": [
          { "internalType": "bytes32", "name": "_agreementHash", "type": "bytes32" },
          { "internalType": "address", "name": "_partyA", "type": "address" },
          { "internalType": "address", "name": "_partyB", "type": "address" },
          { "internalType": "uint256", "name": "_price", "type": "uint256" },
          { "internalType": "uint256", "name": "_quantity", "type": "uint256" }
        ],
        "name": "recordAgreement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      }
    ],
    functionName: 'recordAgreement',
  });
  
  const { isLoading: isConfirming, isSuccess: isConfirmed } = useWaitForTransaction({
    hash,
  });

  const handleRecordOnBlockchain = async () => {
    if (!agreement || !address) return;

    setIsRecording(true);
    setError(null);

    try {
      // Convert agreement hash to bytes32
      const agreementHash = `0x${agreement.agreement_hash}`;
      
      // Ensure we have both addresses
      const buyerAddress = agreement.buyer_address || address;
      const sellerAddress = agreement.seller_address || address;

      write({
        args: [
          agreementHash as `0x${string}`,
          buyerAddress as `0x${string}`,
          sellerAddress as `0x${string}`,
          BigInt(Math.floor(agreement.price * 100)), // Convert to wei-like units
          BigInt(agreement.quantity)
        ],
      });

      if (hash) {
        setTxHash(hash);
      }
    } catch (err: any) {
      console.error('Error recording agreement:', err);
      setError(err.message || 'Failed to record agreement on blockchain');
    } finally {
      setIsRecording(false);
    }
  };

  // Update state when transaction is confirmed
  if (isConfirmed && !isRecorded) {
    setIsRecorded(true);
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={onNewNegotiation}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>New Negotiation</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agreement Details */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Agreement Reached! 🎉
          </h2>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600">Price per unit:</span>
              <span className="text-xl font-semibold text-gray-900">
                ${agreement.price}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600">Quantity:</span>
              <span className="text-xl font-semibold text-gray-900">
                {agreement.quantity}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600">Total Value:</span>
              <span className="text-xl font-semibold text-gray-900">
                ${(agreement.price * agreement.quantity).toFixed(2)}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600">Buyer:</span>
              <span className="font-mono text-sm">
                {formatAddress(agreement.buyer_address || address)}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600">Seller:</span>
              <span className="font-mono text-sm">
                {formatAddress(agreement.seller_address || address)}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-600">Agreement Hash:</span>
              <span className="font-mono text-xs text-gray-500 break-all">
                {agreement.agreement_hash}
              </span>
            </div>
          </div>
        </div>

        {/* Blockchain Recording */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Record on Blockchain
          </h3>
          
          <p className="text-gray-600 mb-6">
            Record this agreement on the Sepolia testnet for permanent, immutable storage.
          </p>

          {!isRecorded && !txHash && (
            <button
              onClick={handleRecordOnBlockchain}
              disabled={isRecording || isPending}
              className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isRecording || isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <CheckCircle className="h-4 w-4" />
              )}
              <span>
                {isRecording || isPending ? 'Recording...' : 'Record on Blockchain'}
              </span>
            </button>
          )}

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center space-x-2 text-red-800">
                <AlertCircle className="h-5 w-5" />
                <span className="font-medium">Error</span>
              </div>
              <p className="mt-2 text-sm text-red-700">{error}</p>
            </div>
          )}

          {txHash && (
            <div className="mt-4 space-y-4">
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center space-x-2 text-blue-800">
                  <CheckCircle className="h-5 w-5" />
                  <span className="font-medium">Transaction Submitted</span>
                </div>
                <p className="mt-2 text-sm text-blue-700">
                  Transaction Hash: {formatAddress(txHash)}
                </p>
                <a
                  href={getEtherscanUrl(txHash)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1 mt-2 text-blue-600 hover:text-blue-800"
                >
                  <span>View on Etherscan</span>
                  <ExternalLink className="h-3 w-3" />
                </a>
              </div>

              {isConfirming && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-center space-x-2 text-yellow-800">
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span className="font-medium">Confirming Transaction...</span>
                  </div>
                  <p className="mt-2 text-sm text-yellow-700">
                    Please wait while the transaction is confirmed on the blockchain.
                  </p>
                </div>
              )}

              {isConfirmed && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center space-x-2 text-green-800">
                    <CheckCircle className="h-5 w-5" />
                    <span className="font-medium">Agreement Recorded!</span>
                  </div>
                  <p className="mt-2 text-sm text-green-700">
                    Your agreement has been permanently recorded on the blockchain.
                  </p>
                </div>
              )}
            </div>
          )}

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">Contract Address:</h4>
            <p className="font-mono text-sm text-gray-600 break-all">
              {CONTRACT_ADDRESS || 'Not configured'}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Sepolia Testnet
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
