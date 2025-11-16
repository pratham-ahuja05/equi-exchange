import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SessionData {
  role: 'buyer' | 'seller';
  buyer_address?: string;
  seller_address?: string;
  target_price?: number;
  min_price?: number;
  max_price?: number;
  quantity?: number;
  fairness_weight?: number;
  max_rounds?: number;
  concession_rate?: number;
  aggressiveness?: number;
  market_symbol?: string;
  market_asset_type?: 'stock' | 'crypto' | 'forex';
}

export interface Session {
  id: number;
  role: string;
  buyer_address?: string;
  seller_address?: string;
  target_price?: number;
  min_price?: number;
  max_price?: number;
  quantity?: number;
  fairness_weight?: number;
  max_rounds?: number;
  status: string;
}

export interface Offer {
  id: number;
  session_id: number;
  round: number;
  made_by: string;
  price: number;
  quantity: number;
  fairness: number;
  proportional_fairness?: number;
  utility: number;
  explanation?: string;
  tom_insights?: string;
  payload: string;
}

export interface Agreement {
  id: number;
  session_id: number;
  price: number;
  quantity: number;
  agreement_hash: string;
}

export interface FinalizedAgreement {
  agreement_hash: string;
  price: number;
  quantity: number;
  buyer_address?: string;
  seller_address?: string;
}

export const api = {
  // Create a new negotiation session
  createSession: async (data: SessionData) => {
    const response = await axios.post(`${API_BASE_URL}/sessions`, data);
    return response.data;
  },

  // Run automatic negotiation
  runAutoNegotiation: async (sessionId: number) => {
    const response = await axios.post(`${API_BASE_URL}/sessions/${sessionId}/auto`);
    return response.data;
  },

  // Get negotiation timeline
  getTimeline: async (sessionId: number) => {
    const response = await axios.get(`${API_BASE_URL}/sessions/${sessionId}/timeline`);
    return response.data;
  },

  // Finalize agreement
  finalizeAgreement: async (sessionId: number) => {
    const response = await axios.post(`${API_BASE_URL}/sessions/${sessionId}/finalize`);
    return response.data;
  },

  // List all sessions
  getSessions: async (status?: string) => {
    const params = status ? { status } : {};
    const response = await axios.get(`${API_BASE_URL}/sessions`, { params });
    return response.data;
  },

  // Get market price
  getMarketPrice: async (symbol: string, assetType: string) => {
    const response = await axios.get(`${API_BASE_URL}/market-price`, {
      params: { symbol, asset_type: assetType }
    });
    return response.data;
  },



  // Record blockchain transaction
  recordBlockchainTransaction: async (sessionId: number, txHash: string, blockNumber?: number) => {
    const response = await axios.post(`${API_BASE_URL}/sessions/${sessionId}/record-blockchain`, {
      tx_hash: txHash,
      block_number: blockNumber
    });
    return response.data;
  },
};
