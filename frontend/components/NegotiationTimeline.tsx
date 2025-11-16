'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp, TrendingUp, TrendingDown, BarChart3, Info } from 'lucide-react';

interface TimelineRound {
  round: number;
  buyer_offer?: number;
  seller_offer?: number;
  buyer_util?: number;
  seller_util?: number;
  fairness?: number;
  proportional_fairness?: number;
  buyer_explanation?: string;
  seller_explanation?: string;
  market_price?: number;
}

interface NegotiationTimelineProps {
  timeline: TimelineRound[];
  sessionData?: any;
}

export function NegotiationTimeline({ timeline, sessionData }: NegotiationTimelineProps) {
  const [expandedRounds, setExpandedRounds] = useState<Set<number>>(new Set());
  const [showMechanics, setShowMechanics] = useState(false);

  const toggleRound = (round: number) => {
    const newExpanded = new Set(expandedRounds);
    if (newExpanded.has(round)) {
      newExpanded.delete(round);
    } else {
      newExpanded.add(round);
    }
    setExpandedRounds(newExpanded);
  };

  const getPriceMovement = (currentPrice: number, previousPrice?: number) => {
    if (!previousPrice) return null;
    const change = currentPrice - previousPrice;
    const isUp = change > 0;
    return {
      change: Math.abs(change),
      direction: isUp ? 'up' : 'down',
      percentage: Math.abs((change / previousPrice) * 100)
    };
  };

  const getFairnessColor = (fairness: number) => {
    if (fairness >= 0.8) return 'text-green-600 bg-green-100';
    if (fairness >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getUtilityColor = (utility: number) => {
    if (utility >= 0.7) return 'text-green-600';
    if (utility >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (!timeline || timeline.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Negotiation Timeline</h3>
        <div className="text-center py-8 text-gray-500">
          <BarChart3 className="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p>No negotiation rounds yet.</p>
          <p className="text-sm mt-2">Start a negotiation to see the timeline here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* How It Works Section */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">How Negotiation Works</h3>
          <button
            onClick={() => setShowMechanics(!showMechanics)}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-800"
          >
            <Info className="h-4 w-4" />
            <span>{showMechanics ? 'Hide' : 'Show'} Mechanics</span>
            {showMechanics ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </button>
        </div>

        {showMechanics && (
          <div className="bg-gray-50 rounded-lg p-4 space-y-3 text-sm">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">AI Agent Strategy</h4>
                <ul className="space-y-1 text-gray-700">
                  <li>• <strong>Utility:</strong> How good the price is for each agent (0-1)</li>
                  <li>• <strong>Fairness:</strong> How balanced the deal is for both parties</li>
                  <li>• <strong>Concession:</strong> Agents gradually move toward opponent's price</li>
                  <li>• <strong>Aggressiveness:</strong> How quickly agents make concessions</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Fairness Metrics</h4>
                <ul className="space-y-1 text-gray-700">
                  <li>• <strong>Simple Fairness:</strong> 1 - |buyer_util - seller_util|</li>
                  <li>• <strong>Proportional:</strong> Log-sum of utilities (Nash product)</li>
                  <li>• <strong>Green (80%+):</strong> Very fair deal</li>
                  <li>• <strong>Yellow (60-80%):</strong> Moderately fair</li>
                  <li>• <strong>Red (&lt;60%):</strong> Unfair, needs adjustment</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Timeline */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Negotiation Rounds</h3>
          <div className="text-sm text-gray-600">
            {timeline.length} round{timeline.length !== 1 ? 's' : ''} completed
          </div>
        </div>

        <div className="space-y-4">
          {timeline.map((round, index) => {
            const isExpanded = expandedRounds.has(round.round);
            const previousRound = index > 0 ? timeline[index - 1] : null;
            const buyerMovement = round.buyer_offer && previousRound?.buyer_offer 
              ? getPriceMovement(round.buyer_offer, previousRound.buyer_offer) 
              : null;
            const sellerMovement = round.seller_offer && previousRound?.seller_offer 
              ? getPriceMovement(round.seller_offer, previousRound.seller_offer) 
              : null;

            return (
              <div key={round.round} className="border rounded-lg overflow-hidden">
                {/* Round Header */}
                <div 
                  className="bg-gray-50 p-4 cursor-pointer hover:bg-gray-100 transition-colors"
                  onClick={() => toggleRound(round.round)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-gray-900">Round {round.round}</span>
                        {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                      </div>
                      
                      {/* Quick Price Display */}
                      <div className="flex items-center space-x-4 text-sm">
                        {round.buyer_offer && (
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 rounded-full bg-blue-500" />
                            <span className="text-gray-700">Buyer: ${round.buyer_offer.toFixed(2)}</span>
                            {buyerMovement && (
                              <div className={`flex items-center space-x-1 ${buyerMovement.direction === 'up' ? 'text-red-600' : 'text-green-600'}`}>
                                {buyerMovement.direction === 'up' ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                                <span className="text-xs">${buyerMovement.change.toFixed(2)}</span>
                              </div>
                            )}
                          </div>
                        )}
                        
                        {round.seller_offer && (
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 rounded-full bg-green-500" />
                            <span className="text-gray-700">Seller: ${round.seller_offer.toFixed(2)}</span>
                            {sellerMovement && (
                              <div className={`flex items-center space-x-1 ${sellerMovement.direction === 'up' ? 'text-red-600' : 'text-green-600'}`}>
                                {sellerMovement.direction === 'up' ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                                <span className="text-xs">${sellerMovement.change.toFixed(2)}</span>
                              </div>
                            )}
                          </div>
                        )}
                        
                        {round.market_price && (
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 rounded-full bg-orange-500" />
                            <span className="text-gray-700">Market: ${round.market_price.toFixed(2)}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Fairness Badge */}
                    {round.fairness !== undefined && (
                      <div className={`px-2 py-1 rounded-full text-xs font-medium ${getFairnessColor(round.fairness)}`}>
                        {(round.fairness * 100).toFixed(1)}% Fair
                      </div>
                    )}
                  </div>
                </div>

                {/* Expanded Content */}
                {isExpanded && (
                  <div className="p-4 bg-white border-t">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Buyer Details */}
                      {round.buyer_offer && (
                        <div className="space-y-3">
                          <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full bg-blue-500" />
                            <h4 className="font-semibold text-gray-900">Buyer Agent</h4>
                          </div>
                          
                          <div className="bg-blue-50 rounded-lg p-3 space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-sm text-gray-600">Offer Price</span>
                              <span className="font-semibold text-lg">${round.buyer_offer.toFixed(2)}</span>
                            </div>
                            
                            {round.buyer_util !== undefined && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">Utility Score</span>
                                <span className={`font-medium ${getUtilityColor(round.buyer_util)}`}>
                                  {round.buyer_util.toFixed(3)}
                                </span>
                              </div>
                            )}
                            
                            {buyerMovement && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">Price Movement</span>
                                <div className={`flex items-center space-x-1 ${buyerMovement.direction === 'up' ? 'text-red-600' : 'text-green-600'}`}>
                                  {buyerMovement.direction === 'up' ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                                  <span className="font-medium">
                                    ${buyerMovement.change.toFixed(2)} ({buyerMovement.percentage.toFixed(1)}%)
                                  </span>
                                </div>
                              </div>
                            )}
                            
                            {round.market_price && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">vs Market</span>
                                <div className={`font-medium ${
                                  round.buyer_offer < round.market_price ? 'text-green-600' : 'text-red-600'
                                }`}>
                                  {round.buyer_offer < round.market_price ? '-' : '+'}
                                  ${Math.abs(round.buyer_offer - round.market_price).toFixed(2)}
                                  ({Math.abs((round.buyer_offer - round.market_price) / round.market_price * 100).toFixed(1)}%)
                                </div>
                              </div>
                            )}
                          </div>
                          
                          {round.buyer_explanation && (
                            <div className="bg-gray-50 rounded-lg p-3">
                              <h5 className="text-sm font-medium text-gray-900 mb-1">Reasoning</h5>
                              <p className="text-sm text-gray-700 italic">"{round.buyer_explanation}"</p>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Seller Details */}
                      {round.seller_offer && (
                        <div className="space-y-3">
                          <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full bg-green-500" />
                            <h4 className="font-semibold text-gray-900">Seller Agent</h4>
                          </div>
                          
                          <div className="bg-green-50 rounded-lg p-3 space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-sm text-gray-600">Offer Price</span>
                              <span className="font-semibold text-lg">${round.seller_offer.toFixed(2)}</span>
                            </div>
                            
                            {round.seller_util !== undefined && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">Utility Score</span>
                                <span className={`font-medium ${getUtilityColor(round.seller_util)}`}>
                                  {round.seller_util.toFixed(3)}
                                </span>
                              </div>
                            )}
                            
                            {sellerMovement && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">Price Movement</span>
                                <div className={`flex items-center space-x-1 ${sellerMovement.direction === 'up' ? 'text-red-600' : 'text-green-600'}`}>
                                  {sellerMovement.direction === 'up' ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                                  <span className="font-medium">
                                    ${sellerMovement.change.toFixed(2)} ({sellerMovement.percentage.toFixed(1)}%)
                                  </span>
                                </div>
                              </div>
                            )}
                            
                            {round.market_price && (
                              <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-600">vs Market</span>
                                <div className={`font-medium ${
                                  round.seller_offer > round.market_price ? 'text-green-600' : 'text-red-600'
                                }`}>
                                  {round.seller_offer > round.market_price ? '+' : '-'}
                                  ${Math.abs(round.seller_offer - round.market_price).toFixed(2)}
                                  ({Math.abs((round.seller_offer - round.market_price) / round.market_price * 100).toFixed(1)}%)
                                </div>
                              </div>
                            )}
                          </div>
                          
                          {round.seller_explanation && (
                            <div className="bg-gray-50 rounded-lg p-3">
                              <h5 className="text-sm font-medium text-gray-900 mb-1">Reasoning</h5>
                              <p className="text-sm text-gray-700 italic">"{round.seller_explanation}"</p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Round Metrics */}
                    {(round.fairness !== undefined || round.proportional_fairness !== undefined) && (
                      <div className="mt-4 pt-4 border-t">
                        <h5 className="text-sm font-medium text-gray-900 mb-2">Round Metrics</h5>
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                          {round.fairness !== undefined && (
                            <div className="text-center">
                              <div className="text-gray-600">Simple Fairness</div>
                              <div className={`font-semibold ${getFairnessColor(round.fairness).split(' ')[0]}`}>
                                {(round.fairness * 100).toFixed(1)}%
                              </div>
                            </div>
                          )}
                          
                          {round.proportional_fairness !== undefined && (
                            <div className="text-center">
                              <div className="text-gray-600">Proportional</div>
                              <div className="font-semibold text-gray-900">
                                {round.proportional_fairness.toFixed(3)}
                              </div>
                            </div>
                          )}
                          
                          {round.buyer_offer && round.seller_offer && (
                            <>
                              <div className="text-center">
                                <div className="text-gray-600">Price Gap</div>
                                <div className="font-semibold text-gray-900">
                                  ${Math.abs(round.buyer_offer - round.seller_offer).toFixed(2)}
                                </div>
                              </div>
                              
                              <div className="text-center">
                                <div className="text-gray-600">Midpoint</div>
                                <div className="font-semibold text-gray-900">
                                  ${((round.buyer_offer + round.seller_offer) / 2).toFixed(2)}
                                </div>
                              </div>
                            </>
                          )}
                          
                          {round.market_price && (
                            <div className="text-center">
                              <div className="text-gray-600">Market Price</div>
                              <div className="font-semibold text-orange-600">
                                ${round.market_price.toFixed(2)}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Summary */}
        {timeline.length > 0 && (
          <div className="mt-6 pt-6 border-t">
            <h4 className="font-semibold text-gray-900 mb-3">Negotiation Summary</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="text-center">
                <div className="text-gray-600">Total Rounds</div>
                <div className="font-semibold text-lg text-gray-900">{timeline.length}</div>
              </div>
              
              {timeline[0]?.buyer_offer && timeline[timeline.length - 1]?.buyer_offer && (
                <div className="text-center">
                  <div className="text-gray-600">Buyer Movement</div>
                  <div className="font-semibold text-lg text-blue-600">
                    ${(timeline[timeline.length - 1].buyer_offer! - timeline[0].buyer_offer!).toFixed(2)}
                  </div>
                </div>
              )}
              
              {timeline[0]?.seller_offer && timeline[timeline.length - 1]?.seller_offer && (
                <div className="text-center">
                  <div className="text-gray-600">Seller Movement</div>
                  <div className="font-semibold text-lg text-green-600">
                    ${(timeline[timeline.length - 1].seller_offer! - timeline[0].seller_offer!).toFixed(2)}
                  </div>
                </div>
              )}
              
              {timeline[timeline.length - 1]?.fairness !== undefined && (
                <div className="text-center">
                  <div className="text-gray-600">Final Fairness</div>
                  <div className={`font-semibold text-lg ${getFairnessColor(timeline[timeline.length - 1].fairness!).split(' ')[0]}`}>
                    {(timeline[timeline.length - 1].fairness! * 100).toFixed(1)}%
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}