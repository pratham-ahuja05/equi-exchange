#!/bin/bash

echo "🚀 Setting up EquiExchange Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local from template..."
    cp env.example .env.local
    echo "⚠️  Please edit .env.local with your configuration:"
    echo "   - NEXT_PUBLIC_CONTRACT_ADDRESS: Your deployed contract address"
    echo "   - NEXT_PUBLIC_SEPOLIA_RPC_URL: Your Sepolia RPC URL"
    echo "   - NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID: Your WalletConnect project ID"
else
    echo "✅ .env.local already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.local with your configuration"
echo "2. Make sure your backend is running on the configured API URL"
echo "3. Deploy your contract to Sepolia and update the contract address"
echo "4. Run 'npm run dev' to start the development server"
echo ""
echo "Happy coding! 🚀"
