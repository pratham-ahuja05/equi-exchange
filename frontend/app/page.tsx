'use client';

import { useState, useEffect } from 'react';
import { useAccount } from 'wagmi';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { Header } from '@/components/Header';
import { NegotiationForm } from '@/components/NegotiationForm';
import { NegotiationFlow } from '@/components/NegotiationFlow';
import { AgreementDisplay } from '@/components/AgreementDisplay';
import { SessionHistory } from '@/components/SessionHistory';

export default function Home() {
  const { isConnected, address } = useAccount();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [currentStep, setCurrentStep] = useState<'form' | 'negotiation' | 'history'>('form');
  const [mounted, setMounted] = useState(false);

  // Prevent hydration mismatch by only rendering after mount
  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSessionCreated = (session: any) => {
    setSessionId(session.session_id);
    setCurrentStep('negotiation');
  };

  const handleNewNegotiation = () => {
    setSessionId(null);
    setCurrentStep('form');
  };

  const handleSessionSelect = (selectedSessionId: number) => {
    setSessionId(selectedSessionId);
    setCurrentStep('negotiation');
  };

  // Prevent hydration mismatch - show loading state during SSR
  if (!mounted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-md mx-auto text-center">
            <div className="card">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                Welcome to EquiExchange
              </h1>
              <p className="text-gray-600 mb-6">
                Loading...
              </p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!isConnected ? (
          <div className="max-w-md mx-auto text-center">
            <div className="card">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                Welcome to EquiExchange
              </h1>
              <p className="text-gray-600 mb-6">
                Connect your wallet to start trading on the decentralized exchange
              </p>
              <ConnectButton />
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto">
            {/* Navigation Tabs */}
            <div className="flex space-x-4 mb-6">
              <button
                onClick={() => setCurrentStep('form')}
                className={`px-4 py-2 rounded-lg ${
                  currentStep === 'form'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                New Negotiation
              </button>
              <button
                onClick={() => setCurrentStep('history')}
                className={`px-4 py-2 rounded-lg ${
                  currentStep === 'history'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                History
              </button>
            </div>

            {currentStep === 'form' && (
              <NegotiationForm 
                address={address!}
                onSessionCreated={handleSessionCreated}
              />
            )}
            
            {currentStep === 'history' && (
              <SessionHistory onSessionSelect={handleSessionSelect} />
            )}
            
            {currentStep === 'negotiation' && sessionId && (
              <NegotiationFlow 
                sessionId={sessionId}
                address={address!}
                onNewNegotiation={handleNewNegotiation}
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}
