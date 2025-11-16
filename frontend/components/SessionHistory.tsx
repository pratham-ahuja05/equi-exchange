'use client';

import { useState, useEffect } from 'react';
import { api, Session } from '@/lib/api';
import { History, Clock, CheckCircle, XCircle, ExternalLink, Hash } from 'lucide-react';
import { formatAddress, getEtherscanUrl } from '@/lib/utils';

interface SessionHistoryProps {
  onSessionSelect: (sessionId: number) => void;
}

interface ExtendedSession extends Session {
  blockchain_tx_hash?: string;
  blockchain_block_number?: number;
}

export function SessionHistory({ onSessionSelect }: SessionHistoryProps) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<string>('');

  useEffect(() => {
    loadSessions();
  }, [filter]);

  const loadSessions = async () => {
    setIsLoading(true);
    try {
      const data = await api.getSessions(filter || undefined);
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            <History className="h-5 w-5 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-900">Session History</h2>
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="input-field"
          >
            <option value="">All Sessions</option>
            <option value="open">Open</option>
            <option value="finalized">Finalized</option>
            <option value="recorded">Recorded on Blockchain</option>
          </select>
        </div>

        {isLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          </div>
        ) : sessions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No sessions found.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition"
                onClick={() => onSessionSelect(session.id!)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="font-semibold text-gray-900">
                        Session #{session.id}
                      </span>
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium ${
                          session.status === 'recorded'
                            ? 'bg-purple-100 text-purple-800'
                            : session.status === 'finalized'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {session.status === 'recorded' ? 'On Blockchain' : session.status}
                      </span>
                      {session.status === 'recorded' ? (
                        <Hash className="h-4 w-4 text-purple-600" />
                      ) : session.status === 'finalized' ? (
                        <CheckCircle className="h-4 w-4 text-green-600" />
                      ) : (
                        <XCircle className="h-4 w-4 text-yellow-600" />
                      )}
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                      <div>
                        <span className="font-medium">Role:</span> {session.role}
                      </div>
                      <div>
                        <span className="font-medium">Price Range:</span>{' '}
                        ${session.min_price} - ${session.max_price}
                      </div>
                      <div>
                        <span className="font-medium">Quantity:</span> {session.quantity}
                      </div>
                      <div>
                        <span className="font-medium">Max Rounds:</span> {session.max_rounds}
                      </div>
                    </div>
                    <div className="mt-2 space-y-1">
                      {session.buyer_address && (
                        <div className="text-xs text-gray-500">
                          Buyer: {formatAddress(session.buyer_address)}
                        </div>
                      )}
                      {(session as any).blockchain_tx_hash && (
                        <div className="flex items-center space-x-2 text-xs">
                          <Hash className="h-3 w-3 text-purple-600" />
                          <span className="text-gray-500">TX:</span>
                          <span className="font-mono text-purple-600">
                            {formatAddress((session as any).blockchain_tx_hash)}
                          </span>
                          <a
                            href={getEtherscanUrl((session as any).blockchain_tx_hash)}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-purple-600 hover:text-purple-800"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <ExternalLink className="h-3 w-3" />
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <Clock className="h-4 w-4" />
                    <span>{formatDate(session.created_at || '')}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

