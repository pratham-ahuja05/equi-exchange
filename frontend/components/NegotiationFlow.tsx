'use client';

import { useState, useEffect } from 'react';
import { api, Offer } from '@/lib/api';
import { formatAddress } from '@/lib/utils';
import { ArrowLeft, Play, RefreshCw, CheckCircle, MessageCircle } from 'lucide-react';

import { MarketContext } from './MarketContext';
import { NegotiationTimeline } from './NegotiationTimeline';
import { TradingMechanics } from './TradingMechanics';
import { NegotiationResults } from './NegotiationResults';

interface NegotiationFlowProps {
  sessionId: number;
  address: string;
  onAgreementReached?: (agreement: any) => void;
  onNewNegotiation: () => void;
}

export function NegotiationFlow({ sessionId, address, onAgreementReached, onNewNegotiation }: NegotiationFlowProps) {
  const [timeline, setTimeline] = useState<any[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [agreement, setAgreement] = useState<any>(null);
  const [sessionData, setSessionData] = useState<any>(null);
  const [marketPrice, setMarketPrice] = useState<number | null>(null);
  const [marketSymbol, setMarketSymbol] = useState<string | null>(null);
  const [marketAssetType, setMarketAssetType] = useState<string | null>(null);


  const runNegotiation = async () => {
    setIsRunning(true);
    setIsLoading(true);
    
    try {
      const result = await api.runAutoNegotiation(sessionId);
      setAgreement(result.agreement);
      setTimeline(result.timeline || []);
      
      // Store market data from negotiation result
      if (result.market_price) setMarketPrice(result.market_price);
      if (result.market_symbol) setMarketSymbol(result.market_symbol);
      if (result.market_asset_type) setMarketAssetType(result.market_asset_type);
      
      // Finalize the agreement if one was reached
      if (result.agreement) {
        const finalizedAgreement = await api.finalizeAgreement(sessionId);
        setAgreement(finalizedAgreement);
      }
    } catch (error) {
      console.error('Error running negotiation:', error);
    } finally {
      setIsLoading(false);
      setIsRunning(false);
    }
  };

  const loadTimeline = async () => {
    try {
      const result = await api.getTimeline(sessionId);
      setTimeline(result.timeline || []);
    } catch (error) {
      console.error('Error loading timeline:', error);
      setTimeline([]);
    }
  };

  useEffect(() => {
    loadTimeline();
    loadSessionData();
  }, [sessionId]);

  const loadSessionData = async () => {
    try {
      const sessions = await api.getSessions();
      const session = sessions.sessions?.find((s: any) => s.id === sessionId);
      if (session) setSessionData(session);
    } catch (error) {
      console.error('Error loading session data:', error);
    }
  };



  // If agreement is reached, show results page
  if (agreement) {
    return (
      <NegotiationResults
        sessionId={sessionId}
        agreement={agreement}
        timeline={timeline}
        address={address}
        onNewNegotiation={onNewNegotiation}
        marketPrice={marketPrice || undefined}
        marketSymbol={marketSymbol || undefined}
        marketAssetType={marketAssetType || undefined}
      />
    );
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
        
        <div className="text-sm text-gray-600">
          Session ID: {sessionId}
        </div>
      </div>

      {/* Market Context */}
      <MarketContext
        symbol={sessionData?.market_symbol}
        assetType={sessionData?.market_asset_type}
        marketPrice={sessionData?.market_price}
      />

      <div className="space-y-6">
        {/* Control Panel */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Negotiation Control
          </h3>
          
          <div className="flex flex-wrap gap-4">
            <button
              onClick={runNegotiation}
              disabled={isLoading || isRunning}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Run Auto-Negotiation</span>
                </>
              )}
            </button>
            
            <button
              onClick={loadTimeline}
              disabled={isLoading}
              className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Refresh Timeline</span>
            </button>
          </div>
        </div>

        {/* Trading Mechanics */}
        <TradingMechanics sessionData={sessionData} />

        {/* Timeline */}
        <NegotiationTimeline timeline={timeline} sessionData={sessionData} />
      </div>
    </div>
  );
}
