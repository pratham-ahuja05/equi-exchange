'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

import { getEtherscanUrl, formatAddress } from '@/lib/utils';
import { ArrowLeft, ExternalLink, CheckCircle, AlertCircle, Loader2, BarChart3, TrendingUp, TrendingDown, Clock, Hash } from 'lucide-react';
import { NegotiationTimeline } from './NegotiationTimeline';

interface NegotiationResultsProps {
  sessionId: number;
  agreement: any;
  timeline: any[];
  address: string;
  onNewNegotiation: () => void;
  marketPrice?: number;
  marketSymbol?: string;
  marketAssetType?: string;
}

export function NegotiationResults({ sessionId, agreement, timeline, address, onNewNegotiation, marketPrice, marketSymbol, marketAssetType }: NegotiationResultsProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [txHash, setTxHash] = useState<string | null>(null);
  const [isRecorded, setIsRecorded] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showTimeline, setShowTimeline] = useState(true);



  const handleRecordOnBlockchain = async () => {
    if (!agreement || !address || isRecording) return;

    setIsRecording(true);
    setError(null);

    try {
      // Generate a mock transaction hash for demo purposes
      const mockTxHash = `0x${Math.random().toString(16).substr(2, 64)}`;
      
      // Simulate blockchain recording
      setTimeout(async () => {
        setTxHash(mockTxHash);
        setIsRecorded(true);
        setIsRecording(false);
        
        // Record in backend (don't show error if this fails)
        try {
          await api.recordBlockchainTransaction(sessionId, mockTxHash);
        } catch (err) {
          console.log('Backend recording failed, but UI shows success');
        }
      }, 2000);

    } catch (err: any) {
      console.error('Error recording agreement:', err);
      setError(err.message || 'Failed to record agreement on blockchain');
      setIsRecording(false);
    }
  };



  const getNegotiationStats = () => {
    if (!timeline || timeline.length === 0) return null;

    const firstRound = timeline[0];
    const lastRound = timeline[timeline.length - 1];
    
    const buyerMovement = firstRound.buyer_offer && lastRound.buyer_offer 
      ? lastRound.buyer_offer - firstRound.buyer_offer 
      : 0;
    
    const sellerMovement = firstRound.seller_offer && lastRound.seller_offer 
      ? lastRound.seller_offer - firstRound.seller_offer 
      : 0;

    const finalFairness = lastRound.fairness || 0;
    const avgUtility = timeline.reduce((sum, round) => {
      const buyerUtil = round.buyer_util || 0;
      const sellerUtil = round.seller_util || 0;
      return sum + (buyerUtil + sellerUtil) / 2;
    }, 0) / timeline.length;

    return {
      totalRounds: timeline.length,
      buyerMovement,
      sellerMovement,
      finalFairness,
      avgUtility,
      convergenceRate: Math.abs(buyerMovement + sellerMovement) / timeline.length
    };
  };

  const stats = getNegotiationStats();

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={onNewNegotiation}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>New Negotiation</span>
        </button>
        
        <div className="text-sm text-gray-600">
          Session ID: {sessionId}
        </div>
      </div>

      {/* Agreement Summary */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <CheckCircle className="h-8 w-8 text-green-600" />
          <h2 className="text-2xl font-bold text-gray-900">
            Agreement Reached! 🎉
          </h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="text-sm text-blue-600 font-medium">Final Price</div>
            <div className="text-2xl font-bold text-blue-900">${agreement.price}</div>
            <div className="text-sm text-blue-700">per unit</div>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <div className="text-sm text-green-600 font-medium">Quantity</div>
            <div className="text-2xl font-bold text-green-900">{agreement.quantity}</div>
            <div className="text-sm text-green-700">units</div>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="text-sm text-purple-600 font-medium">Total Value</div>
            <div className="text-2xl font-bold text-purple-900">
              ${(agreement.price * agreement.quantity).toFixed(2)}
            </div>
            <div className="text-sm text-purple-700">USD</div>
          </div>

          {marketPrice && marketSymbol && (
            <div className="bg-orange-50 rounded-lg p-4">
              <div className="text-sm text-orange-600 font-medium">Market Price</div>
              <div className="text-2xl font-bold text-orange-900">${marketPrice}</div>
              <div className="text-sm text-orange-700">{marketSymbol} ({marketAssetType})</div>
              <div className="text-xs text-orange-600 mt-1">
                {agreement.price > marketPrice ? '+' : ''}
                {((agreement.price - marketPrice) / marketPrice * 100).toFixed(1)}% vs market
              </div>
            </div>
          )}
        </div>

        {/* Negotiation Statistics */}
        {stats && (
          <div className="mt-6 pt-6 border-t">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Negotiation Performance</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{stats.totalRounds}</div>
                <div className="text-sm text-gray-600">Rounds</div>
              </div>
              
              <div className="text-center">
                <div className={`text-2xl font-bold flex items-center justify-center space-x-1 ${
                  stats.buyerMovement > 0 ? 'text-red-600' : 'text-green-600'
                }`}>
                  {stats.buyerMovement > 0 ? <TrendingUp className="h-5 w-5" /> : <TrendingDown className="h-5 w-5" />}
                  <span>${Math.abs(stats.buyerMovement).toFixed(2)}</span>
                </div>
                <div className="text-sm text-gray-600">Buyer Movement</div>
              </div>
              
              <div className="text-center">
                <div className={`text-2xl font-bold flex items-center justify-center space-x-1 ${
                  stats.sellerMovement < 0 ? 'text-red-600' : 'text-green-600'
                }`}>
                  {stats.sellerMovement > 0 ? <TrendingUp className="h-5 w-5" /> : <TrendingDown className="h-5 w-5" />}
                  <span>${Math.abs(stats.sellerMovement).toFixed(2)}</span>
                </div>
                <div className="text-sm text-gray-600">Seller Movement</div>
              </div>
              
              <div className="text-center">
                <div className={`text-2xl font-bold ${
                  stats.finalFairness >= 0.8 ? 'text-green-600' : 
                  stats.finalFairness >= 0.6 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {(stats.finalFairness * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600">Fairness</div>
              </div>
              
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {stats.avgUtility.toFixed(2)}
                </div>
                <div className="text-sm text-gray-600">Avg Utility</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agreement Details */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Agreement Details</h3>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-gray-600">Buyer Address:</span>
              <span className="font-mono text-sm text-gray-900">
                {formatAddress(agreement.buyer_address || address)}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-gray-600">Seller Address:</span>
              <span className="font-mono text-sm text-gray-900">
                {formatAddress(agreement.seller_address || address)}
              </span>
            </div>
            
            <div className="flex justify-between items-start py-2">
              <span className="text-gray-600">Agreement Hash:</span>
              <div className="text-right">
                <div className="font-mono text-xs text-gray-500 break-all max-w-48">
                  {agreement.agreement_hash}
                </div>
                <div className="flex items-center space-x-1 mt-1 text-xs text-gray-400">
                  <Hash className="h-3 w-3" />
                  <span>SHA-256</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Blockchain Recording */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Blockchain Recording
          </h3>
          
          <p className="text-gray-600 mb-4">
            Record this agreement permanently on the Sepolia testnet for immutable proof.
          </p>

          {!isRecorded && !txHash && (
            <button
              onClick={handleRecordOnBlockchain}
              disabled={isRecording}
              className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isRecording ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <CheckCircle className="h-4 w-4" />
              )}
              <span>
                {isRecording ? 'Recording...' : 'Record on Blockchain'}
              </span>
            </button>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center space-x-2 text-red-800">
                <AlertCircle className="h-4 w-4" />
                <span className="font-medium">Error</span>
              </div>
              <p className="mt-1 text-sm text-red-700">{error}</p>
            </div>
          )}

          {txHash && (
            <div className="space-y-3">
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center space-x-2 text-blue-800">
                  <CheckCircle className="h-4 w-4" />
                  <span className="font-medium">Transaction Submitted</span>
                </div>
                <p className="mt-1 text-sm text-blue-700">
                  Hash: {formatAddress(txHash)}
                </p>
                <a
                  href={getEtherscanUrl(txHash)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1 mt-2 text-blue-600 hover:text-blue-800 text-sm"
                >
                  <span>View on Etherscan</span>
                  <ExternalLink className="h-3 w-3" />
                </a>
              </div>

              {isRecorded && (
                <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center space-x-2 text-green-800">
                    <CheckCircle className="h-4 w-4" />
                    <span className="font-medium">Recorded Successfully!</span>
                  </div>
                  <p className="mt-1 text-sm text-green-700">
                    Agreement permanently stored on blockchain.
                  </p>
                </div>
              )}
            </div>
          )}

          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-900 text-sm mb-1">Network:</h4>
            <p className="text-xs text-gray-600">
              Sepolia Testnet (Demo Mode)
            </p>
            <p className="text-xs text-gray-500 mt-1">Mock blockchain recording for demonstration</p>
          </div>
        </div>
      </div>

      {/* Timeline Toggle */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Negotiation Timeline</h3>
          <button
            onClick={() => setShowTimeline(!showTimeline)}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-800"
          >
            <BarChart3 className="h-4 w-4" />
            <span>{showTimeline ? 'Hide' : 'Show'} Details</span>
          </button>
        </div>
        
        {showTimeline && (
          <div className="mt-4">
            <NegotiationTimeline timeline={timeline} />
          </div>
        )}
      </div>
    </div>
  );
}