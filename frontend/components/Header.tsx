'use client';

import { ConnectButton } from '@rainbow-me/rainbowkit';
import { ShoppingCart, Users } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              <ShoppingCart className="h-8 w-8 text-primary-600" />
              <Users className="h-6 w-6 text-primary-500" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">
              EquiExchange
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              Sepolia Testnet
            </span>
            <ConnectButton />
          </div>
        </div>
      </div>
    </header>
  );
}
