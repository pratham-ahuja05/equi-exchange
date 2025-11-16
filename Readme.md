# EquiExchange - AI-Powered Decentralized Trading Platform

A complete decentralized trading platform featuring AI-powered negotiations, smart contract integration, and blockchain recording. Built with Solidity, FastAPI, and Next.js.

## 🚀 Features

- **AI Negotiation Agents**: Smart agents with market-aware strategies
- **Real-time Market Integration**: AlphaVantage API for live price data
- **Explainable AI**: Human-readable decision explanations
- **Fairness Metrics**: Dual fairness algorithms (Simple + Proportional)
- **Smart Contracts**: Ethereum integration with agreement recording
- **Modern UI**: Next.js with wallet connection and real-time updates

## 🏗️ Architecture

```
equi-exchange/
├── contracts/          # Hardhat Solidity smart contracts
├── backend/           # FastAPI Python backend
└── frontend/          # Next.js React frontend
```

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- MetaMask wallet

### Installation

1. **Clone repository**
```bash
git clone https://github.com/YOUR_USERNAME/equi-exchange.git
cd equi-exchange
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python -m uvicorn app.main:app --reload --port 8000
```

3. **Frontend Setup**
```bash
cd frontend
npm install --legacy-peer-deps
cp env.example .env.local  # Configure environment
npm run dev
```

4. **Smart Contracts**
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
```

## 🎯 Usage

1. **Connect Wallet**: MetaMask integration
2. **Set Parameters**: Price range, quantity, market symbol
3. **Run Negotiation**: AI agents negotiate automatically
4. **View Results**: Real-time timeline with explanations
5. **Record Agreement**: Store on blockchain

## 🤖 AI Features

- **Market-Aware Agents**: Adjust strategy based on real market prices
- **Fairness Optimization**: Balanced outcomes for both parties
- **Explainable Decisions**: Natural language reasoning
- **Q-Learning**: Adaptive strategies that improve over time

## 📊 Supported Markets

- **Stocks**: AAPL, GOOGL, MSFT, etc.
- **Crypto**: BTC, ETH, SOL, etc.
- **Forex**: EURUSD, GBPUSD, etc.

## 🔧 Tech Stack

- **Frontend**: Next.js, React, TailwindCSS, RainbowKit
- **Backend**: FastAPI, Python, SQLModel
- **Blockchain**: Solidity, Hardhat, Ethereum
- **AI**: NumPy, Custom negotiation algorithms
- **APIs**: AlphaVantage for market data

## 📄 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

**Built for hackathons and educational purposes. Demonstrates AI-powered negotiations with real market integration.**