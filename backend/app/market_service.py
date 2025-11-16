"""
Market Context Module - Fetches real-time market prices from free APIs
Uses AlphaVantage as primary, with fallbacks to other free APIs
"""

import os
import requests
import time
from typing import Optional, Dict
from datetime import datetime


class MarketDataService:
    """Service for fetching market data from free APIs"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        print(f"AlphaVantage API Key: {self.alpha_vantage_key[:10] if self.alpha_vantage_key else 'None'}...")
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 60  # Cache for 60 seconds
        
    def get_market_price(
        self, 
        symbol: str, 
        asset_type: str = "stock"
    ) -> Dict:
        """
        Get market price for a symbol
        
        Args:
            symbol: Asset symbol (e.g., 'AAPL', 'BTC', 'EURUSD')
            asset_type: 'stock', 'crypto', or 'forex'
        
        Returns:
            {
                "symbol": str,
                "asset_type": str,
                "price": float,
                "timestamp": str,
                "source": str
            }
        """
        
        # Check cache
        cache_key = f"{symbol}_{asset_type}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_data
        
        try:
            if asset_type == "stock":
                data = self._get_stock_price(symbol)
            elif asset_type == "crypto":
                data = self._get_crypto_price(symbol)
            elif asset_type == "forex":
                data = self._get_forex_price(symbol)
            else:
                return {
                    "symbol": symbol,
                    "asset_type": asset_type,
                    "price": None,
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": f"Unsupported asset type: {asset_type}",
                    "source": "none"
                }
            
            # Cache the result
            self.cache[cache_key] = (data, time.time())
            return data
            
        except Exception as e:
            return {
                "symbol": symbol,
                "asset_type": asset_type,
                "price": None,
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "source": "error"
            }
    
    def _get_stock_price(self, symbol: str) -> Dict:
        """Get stock price from AlphaVantage"""
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.alpha_vantage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            price = float(quote.get("05. price", 0))
            
            return {
                "symbol": symbol,
                "asset_type": "stock",
                "price": price,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "alphavantage"
            }
        
        # Fallback: Use demo data if API key is "demo"
        if self.alpha_vantage_key == "demo":
            return {
                "symbol": symbol,
                "asset_type": "stock",
                "price": 150.0,  # Demo price
                "timestamp": datetime.utcnow().isoformat(),
                "source": "demo",
                "note": "Using demo data. Get free API key from alphavantage.co"
            }
        
        raise Exception(f"Failed to fetch stock price: {data.get('Note', 'Unknown error')}")
    
    def _get_crypto_price(self, symbol: str) -> Dict:
        """Get crypto price from AlphaVantage"""
        # AlphaVantage uses format like "BTC" for Bitcoin
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": symbol,
            "to_currency": "USD",
            "apikey": self.alpha_vantage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "Realtime Currency Exchange Rate" in data:
            rate = data["Realtime Currency Exchange Rate"]
            price = float(rate.get("5. Exchange Rate", 0))
            
            return {
                "symbol": symbol,
                "asset_type": "crypto",
                "price": price,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "alphavantage"
            }
        
        # Fallback: Use demo data
        if self.alpha_vantage_key == "demo":
            demo_prices = {"BTC": 45000.0, "ETH": 2500.0, "SOL": 100.0}
            return {
                "symbol": symbol,
                "asset_type": "crypto",
                "price": demo_prices.get(symbol.upper(), 100.0),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "demo",
                "note": "Using demo data. Get free API key from alphavantage.co"
            }
        
        raise Exception(f"Failed to fetch crypto price: {data.get('Note', 'Unknown error')}")
    
    def _get_forex_price(self, symbol: str) -> Dict:
        """Get forex price from AlphaVantage"""
        # Format: "EURUSD" -> from_currency="EUR", to_currency="USD"
        if len(symbol) == 6:
            from_curr = symbol[:3]
            to_curr = symbol[3:]
        else:
            raise Exception("Forex symbol must be 6 characters (e.g., EURUSD)")
        
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_curr,
            "to_currency": to_curr,
            "apikey": self.alpha_vantage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "Realtime Currency Exchange Rate" in data:
            rate = data["Realtime Currency Exchange Rate"]
            price = float(rate.get("5. Exchange Rate", 0))
            
            return {
                "symbol": symbol,
                "asset_type": "forex",
                "price": price,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "alphavantage"
            }
        
        # Fallback: Use demo data
        if self.alpha_vantage_key == "demo":
            demo_prices = {"EURUSD": 1.08, "GBPUSD": 1.25, "USDJPY": 150.0}
            return {
                "symbol": symbol,
                "asset_type": "forex",
                "price": demo_prices.get(symbol.upper(), 1.0),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "demo",
                "note": "Using demo data. Get free API key from alphavantage.co"
            }
        
        raise Exception(f"Failed to fetch forex price: {data.get('Note', 'Unknown error')}")


# Singleton instance
market_service = MarketDataService()

