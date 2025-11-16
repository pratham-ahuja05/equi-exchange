'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

interface MarketContextProps {
  symbol?: string;
  assetType?: string;
  marketPrice?: number;
}

// Generate dummy price based on symbol for consistency
const getDummyPrice = (symbol: string) => {
  const hash = symbol.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  return Math.abs(hash % 200) + 50; // Price between $50-$250
};

export function MarketContext({ symbol, assetType, marketPrice: initialPrice }: MarketContextProps) {
  // Always show with dummy data
  const displaySymbol = symbol || 'AAPL';
  const displayAssetType = assetType || 'stock';
  const displayPrice = initialPrice || getDummyPrice(displaySymbol);

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <DollarSign className="h-5 w-5 text-blue-600" />
          <div>
            <h3 className="font-semibold text-gray-900">Market Context</h3>
            <p className="text-sm text-gray-600">
              {displaySymbol.toUpperCase()} ({displayAssetType})
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center space-x-1">
            <span className="text-2xl font-bold text-gray-900">
              ${displayPrice.toFixed(2)}
            </span>
            <span className="text-xs text-gray-500">(Demo)</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Market reference price</p>
        </div>
      </div>
    </div>
  );
}

