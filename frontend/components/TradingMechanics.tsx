'use client';

import { useState } from 'react';
import { Brain, Target, TrendingUp, BarChart3, Users, Zap, ChevronDown, ChevronUp } from 'lucide-react';

interface TradingMechanicsProps {
  sessionData?: any;
}

export function TradingMechanics({ sessionData }: TradingMechanicsProps) {
  const [activeTab, setActiveTab] = useState<'strategy' | 'fairness' | 'utility' | 'process'>('strategy');

  const tabs = [
    { id: 'strategy', label: 'AI Strategy', icon: Brain },
    { id: 'fairness', label: 'Fairness Metrics', icon: BarChart3 },
    { id: 'utility', label: 'Utility Functions', icon: Target },
    { id: 'process', label: 'Process Flow', icon: Zap }
  ];

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Trading Mechanics & AI Strategy</h3>
      
      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'strategy' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-3 h-3 rounded-full bg-blue-500" />
                  <h4 className="font-semibold text-gray-900">Buyer Agent Strategy</h4>
                </div>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>Goal:</strong> Minimize price while maintaining fairness</li>
                  <li>• <strong>Starting Position:</strong> Target price (usually below market)</li>
                  <li>• <strong>Concession Strategy:</strong> Gradually increase offers</li>
                  <li>• <strong>Fairness Weight:</strong> {sessionData?.fairness_weight || 0.5} (how much fairness matters)</li>
                  <li>• <strong>Aggressiveness:</strong> {sessionData?.aggressiveness || 0.5} (concession speed)</li>
                </ul>
              </div>

              <div className="bg-green-50 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <h4 className="font-semibold text-gray-900">Seller Agent Strategy</h4>
                </div>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>Goal:</strong> Maximize price while maintaining fairness</li>
                  <li>• <strong>Starting Position:</strong> Maximum acceptable price</li>
                  <li>• <strong>Concession Strategy:</strong> Gradually decrease offers</li>
                  <li>• <strong>Fairness Weight:</strong> {sessionData?.fairness_weight || 0.5} (how much fairness matters)</li>
                  <li>• <strong>Aggressiveness:</strong> {sessionData?.aggressiveness || 0.5} (concession speed)</li>
                </ul>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Negotiation Parameters</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-gray-600">Max Rounds</div>
                  <div className="font-semibold">{sessionData?.max_rounds || 8}</div>
                </div>
                <div>
                  <div className="text-gray-600">Concession Rate</div>
                  <div className="font-semibold">{((sessionData?.concession_rate || 0.05) * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-gray-600">Fairness Weight</div>
                  <div className="font-semibold">{((sessionData?.fairness_weight || 0.5) * 100).toFixed(0)}%</div>
                </div>
                <div>
                  <div className="text-gray-600">Aggressiveness</div>
                  <div className="font-semibold">{((sessionData?.aggressiveness || 0.5) * 100).toFixed(0)}%</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'fairness' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-yellow-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Simple Fairness</h4>
                <div className="space-y-3 text-sm">
                  <div className="bg-white rounded p-3 font-mono text-xs">
                    fairness = 1 - |buyer_utility - seller_utility|
                  </div>
                  <ul className="space-y-1 text-gray-700">
                    <li>• Measures how close the utilities are</li>
                    <li>• Range: 0 to 1 (1 = perfectly fair)</li>
                    <li>• Easy to understand and compute</li>
                    <li>• Penalizes large utility differences</li>
                  </ul>
                </div>
              </div>

              <div className="bg-purple-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Proportional Fairness</h4>
                <div className="space-y-3 text-sm">
                  <div className="bg-white rounded p-3 font-mono text-xs">
                    prop_fairness = log(buyer_utility) + log(seller_utility)
                  </div>
                  <ul className="space-y-1 text-gray-700">
                    <li>• Nash product approach</li>
                    <li>• Maximizes product of utilities</li>
                    <li>• Better for economic efficiency</li>
                    <li>• Handles edge cases better</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Fairness Interpretation</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="bg-green-100 border border-green-200 rounded p-3">
                  <div className="font-semibold text-green-800">High Fairness (80%+)</div>
                  <div className="text-green-700 mt-1">Both parties get similar value. Deal is balanced and mutually beneficial.</div>
                </div>
                <div className="bg-yellow-100 border border-yellow-200 rounded p-3">
                  <div className="font-semibold text-yellow-800">Medium Fairness (60-80%)</div>
                  <div className="text-yellow-700 mt-1">Moderate imbalance. One party benefits more, but still acceptable.</div>
                </div>
                <div className="bg-red-100 border border-red-200 rounded p-3">
                  <div className="font-semibold text-red-800">Low Fairness (&lt;60%)</div>
                  <div className="text-red-700 mt-1">Significant imbalance. One party is getting a much better deal.</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'utility' && (
          <div className="space-y-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Utility Function Calculation</h4>
              <div className="space-y-4 text-sm">
                <div className="bg-white rounded p-3">
                  <div className="font-semibold mb-2">For Buyer:</div>
                  <div className="font-mono text-xs mb-2">utility = (max_price - offer_price) / (max_price - min_price)</div>
                  <div className="text-gray-700">Higher utility when price is lower (closer to min_price)</div>
                </div>
                <div className="bg-white rounded p-3">
                  <div className="font-semibold mb-2">For Seller:</div>
                  <div className="font-mono text-xs mb-2">utility = (offer_price - min_price) / (max_price - min_price)</div>
                  <div className="text-gray-700">Higher utility when price is higher (closer to max_price)</div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Utility Ranges</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-green-600 font-medium">0.7 - 1.0:</span>
                    <span>Excellent deal</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-yellow-600 font-medium">0.4 - 0.7:</span>
                    <span>Acceptable deal</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-red-600 font-medium">0.0 - 0.4:</span>
                    <span>Poor deal</span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Session Price Range</h4>
                {sessionData && (
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Min Price:</span>
                      <span className="font-semibold">${sessionData.min_price}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Target Price:</span>
                      <span className="font-semibold">${sessionData.target_price}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Max Price:</span>
                      <span className="font-semibold">${sessionData.max_price}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Range:</span>
                      <span className="font-semibold">${sessionData.max_price - sessionData.min_price}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'process' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-6">
              <h4 className="font-semibold text-gray-900 mb-4">Negotiation Process Flow</h4>
              <div className="space-y-4">
                {[
                  {
                    step: 1,
                    title: "Initialization",
                    description: "Both agents start with their preferred prices (buyer: target, seller: max)",
                    color: "bg-blue-500"
                  },
                  {
                    step: 2,
                    title: "Offer Exchange",
                    description: "Agents make simultaneous offers based on their strategy and opponent's last offer",
                    color: "bg-purple-500"
                  },
                  {
                    step: 3,
                    title: "Utility Calculation",
                    description: "Each agent calculates their utility and fairness metrics for the current round",
                    color: "bg-yellow-500"
                  },
                  {
                    step: 4,
                    title: "Strategy Adjustment",
                    description: "Agents adjust their next offer using concession rate, fairness weight, and aggressiveness",
                    color: "bg-orange-500"
                  },
                  {
                    step: 5,
                    title: "Convergence Check",
                    description: "Check if offers are close enough or max rounds reached. If not, repeat from step 2",
                    color: "bg-green-500"
                  }
                ].map((item) => (
                  <div key={item.step} className="flex items-start space-x-4">
                    <div className={`w-8 h-8 ${item.color} rounded-full flex items-center justify-center text-white text-sm font-semibold`}>
                      {item.step}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">{item.title}</div>
                      <div className="text-sm text-gray-700">{item.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Convergence Criteria</h4>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>Price Gap:</strong> Offers within $1.00 of each other</li>
                  <li>• <strong>Max Rounds:</strong> {sessionData?.max_rounds || 8} rounds completed</li>
                  <li>• <strong>Utility Threshold:</strong> Both agents above 0.3 utility</li>
                  <li>• <strong>Fairness Target:</strong> Simple fairness above 60%</li>
                </ul>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">AI Decision Factors</h4>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>Own Utility:</strong> How good the price is for the agent</li>
                  <li>• <strong>Opponent Behavior:</strong> Pattern recognition in opponent offers</li>
                  <li>• <strong>Fairness Balance:</strong> Maintaining mutual benefit</li>
                  <li>• <strong>Market Context:</strong> Real market prices when available</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}