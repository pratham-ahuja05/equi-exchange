"""
Manual Gemini API Chatbot - Provides negotiation analysis and suggestions
Uses Gemini API when available, falls back to placeholder
"""

import os
import json
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Try to import Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ChatService:
    """Service for Gemini chatbot integration"""
    
    def __init__(self):
        # Explicitly define API key (replace with your actual key)
        self.api_key = "AIzaSyAiLm3mB3aMx2iG7OXiedk4mxIdmrMwAQg"
        print(f"DEBUG: API Key loaded: {self.api_key is not None}, Key: {self.api_key[:10] if self.api_key else 'None'}...")
        self.model = None
        self.use_placeholder = False  # Try to use real API first
        
        # Check if Gemini is available
        if not GEMINI_AVAILABLE:
            print("WARNING: google-generativeai package not installed. Using placeholder mode.")
            self.use_placeholder = True
            return
        
        # Check if API key is provided
        if not self.api_key or self.api_key.strip() == "":
            print("WARNING: GEMINI_API_KEY not set. Using placeholder mode.")
            self.use_placeholder = True
            return
        
        # Initialize Gemini
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_placeholder = False
            print("SUCCESS: Gemini API initialized successfully")
        except Exception as e:
            print(f"WARNING: Gemini API initialization failed: {e}")
            self.use_placeholder = True
        
    def chat(
        self, 
        session_id: int,
        user_message: str,
        session_context: Optional[Dict] = None,
        timeline: Optional[list] = None
    ) -> Dict:
        """
        Process user chat message and return AI response
        
        Args:
            session_id: Session ID
            user_message: User's question/message
            session_context: Session data (prices, parameters, etc.)
            timeline: Negotiation timeline data
        
        Returns:
            {
                "reply": str,
                "source": "gemini" | "placeholder",
                "timestamp": str
            }
        """
        
        if self.use_placeholder or self.model is None:
            return self._placeholder_chat(user_message, session_context, timeline)
        
        # Use real Gemini API
        try:
            return self._gemini_chat(user_message, session_context, timeline)
        except Exception as e:
            print(f"WARNING: Gemini API error: {e}, falling back to placeholder")
            return self._placeholder_chat(user_message, session_context, timeline)
    
    def _gemini_chat(
        self,
        user_message: str,
        session_context: Optional[Dict],
        timeline: Optional[list]
    ) -> Dict:
        """Use real Gemini API for chat responses"""
        
        # Build context for the AI
        context_parts = []
        
        if session_context:
            context_parts.append("Negotiation Session Context:")
            context_parts.append(f"- Target Price: ${session_context.get('target_price', 'N/A')}")
            context_parts.append(f"- Price Range: ${session_context.get('min_price', 'N/A')} - ${session_context.get('max_price', 'N/A')}")
            context_parts.append(f"- Fairness Weight: {session_context.get('fairness_weight', 0.5)}")
            context_parts.append(f"- Aggressiveness: {session_context.get('aggressiveness', 0.5)}")
            if session_context.get('market_price'):
                context_parts.append(f"- Market Price: ${session_context.get('market_price')}")
        
        if timeline and len(timeline) > 0:
            context_parts.append("\nRecent Negotiation Timeline:")
            for round_data in timeline[-3:]:  # Last 3 rounds
                context_parts.append(f"Round {round_data.get('round', '?')}:")
                context_parts.append(f"  Buyer: ${round_data.get('buyer_offer', 0):.2f} (utility: {round_data.get('buyer_util', 0):.2f})")
                context_parts.append(f"  Seller: ${round_data.get('seller_offer', 0):.2f} (utility: {round_data.get('seller_util', 0):.2f})")
                context_parts.append(f"  Fairness: {round_data.get('fairness', 0):.1%}")
                if round_data.get('buyer_explanation'):
                    context_parts.append(f"  Buyer reasoning: {round_data.get('buyer_explanation')}")
        
        context = "\n".join(context_parts) if context_parts else "No negotiation context available."
        
        # Build prompt
        prompt = f"""You are an expert negotiation assistant for EquiExchange, a decentralized trading platform with AI-powered negotiations.

{context}

User Question: {user_message}

Provide a helpful, concise response (2-3 sentences) analyzing the negotiation or answering the user's question. Focus on:
- Fairness metrics and balance
- Strategic advice for better outcomes
- Understanding of the negotiation process
- Market context if available

Be practical and actionable."""

        # Call Gemini API
        response = self.model.generate_content(prompt)
        
        return {
            "reply": response.text,
            "source": "gemini",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _placeholder_chat(
        self, 
        user_message: str,
        session_context: Optional[Dict],
        timeline: Optional[list]
    ) -> Dict:
        """Placeholder chat responses when Gemini API is not available"""
        
        message_lower = user_message.lower()
        
        # Analyze user intent
        if any(word in message_lower for word in ["good", "fair", "reasonable", "acceptable"]):
            if timeline and len(timeline) > 0:
                last_round = timeline[-1]
                fairness = last_round.get("fairness", 0.5)
                proportional_fairness = last_round.get("proportional_fairness")
                buyer_offer = last_round.get("buyer_offer")
                seller_offer = last_round.get("seller_offer")
                buyer_util = last_round.get("buyer_util", 0)
                seller_util = last_round.get("seller_util", 0)
                
                # Build detailed response with timeline data
                response_parts = []
                response_parts.append(f"**Current Negotiation State (Round {last_round.get('round', '?')}):**")
                if buyer_offer is not None:
                    response_parts.append(f"- Buyer Offer: ${buyer_offer:.2f} (utility: {buyer_util:.2f})")
                if seller_offer is not None:
                    response_parts.append(f"- Seller Offer: ${seller_offer:.2f} (utility: {seller_util:.2f})")
                if fairness is not None:
                    response_parts.append(f"- Simple Fairness: {fairness:.1%}")
                if proportional_fairness is not None:
                    response_parts.append(f"- Proportional Fairness: {proportional_fairness:.3f}")
                
                if fairness is not None:
                    if fairness > 0.7:
                        response_parts.append(f"\nGOOD: This offer looks good! The fairness score is {fairness:.1%}, which indicates a balanced negotiation. Both parties are getting reasonable value.")
                    else:
                        response_parts.append(f"\nWARNING: The current fairness is {fairness:.1%}, which is below ideal. Consider making a small concession to improve the balance.")
                
                # Show recent rounds summary
                if len(timeline) > 1:
                    response_parts.append(f"\n**Recent Rounds Summary:**")
                    for r in timeline[-3:]:
                        response_parts.append(f"Round {r.get('round')}: Buyer ${r.get('buyer_offer', 0):.2f} ↔ Seller ${r.get('seller_offer', 0):.2f} (Fairness: {r.get('fairness', 0):.1%})")
                
                return {
                    "reply": "\n".join(response_parts),
                    "source": "placeholder",
                    "timestamp": datetime.utcnow().isoformat()
                }
            return {
                "reply": "I'd need to see the current negotiation state to assess if the offer is good. Please check the timeline to see the latest offers and fairness metrics. Make sure a negotiation has been run first.",
                "source": "placeholder",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        elif any(word in message_lower for word in ["counteroffer", "counter", "suggest", "should"]):
            if timeline and len(timeline) > 0:
                last_round = timeline[-1]
                buyer_offer = last_round.get("buyer_offer", 0)
                seller_offer = last_round.get("seller_offer", 0)
                midpoint = (buyer_offer + seller_offer) / 2
                gap = abs(buyer_offer - seller_offer)
                
                if gap > 5:
                    return {
                        "reply": f"The offers are still {gap:.2f} apart. I suggest proposing ${midpoint:.2f} as a counteroffer - this is the midpoint and would improve fairness. Consider conceding about 10-15% toward the opponent's position.",
                        "source": "placeholder",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "reply": f"The offers are close (${gap:.2f} apart). A counteroffer around ${midpoint:.2f} would likely lead to agreement. You're very close to a deal!",
                        "source": "placeholder",
                        "timestamp": datetime.utcnow().isoformat()
                    }
            return {
                "reply": "To suggest a counteroffer, I need to see the current negotiation state. Please run the negotiation first or check the timeline.",
                "source": "placeholder",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        elif any(word in message_lower for word in ["explain", "why", "how", "reason"]):
            if timeline and len(timeline) > 0:
                rounds_count = len(timeline)
                return {
                    "reply": f"The negotiation has progressed through {rounds_count} rounds. Each agent is adjusting offers based on fairness, target prices, and opponent behavior. The agents use a concession strategy where they move toward the opponent's position while balancing their own utility. Check the explanations in the timeline for specific reasoning behind each move.",
                    "source": "placeholder",
                    "timestamp": datetime.utcnow().isoformat()
                }
            return {
                "reply": "The negotiation uses AI agents that balance individual utility (how good the price is for them) with fairness (how balanced the deal is). Agents make concessions over rounds, adjusting based on opponent behavior and market conditions if available.",
                "source": "placeholder",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        elif any(word in message_lower for word in ["fairness", "fair"]):
            if timeline and len(timeline) > 0:
                last_round = timeline[-1]
                fairness = last_round.get("fairness", 0.5)
                return {
                    "reply": f"Current fairness is {fairness:.1%}. Fairness measures how balanced the deal is - a score of 1.0 means both parties get equal utility. The system uses two metrics: Simple Fairness (difference in utilities) and Proportional Fairness (log-sum of utilities). Higher fairness indicates a more mutually beneficial agreement.",
                    "source": "placeholder",
                    "timestamp": datetime.utcnow().isoformat()
                }
            return {
                "reply": "Fairness measures how balanced the negotiation is. It compares buyer and seller utilities - when both parties get similar value, fairness is high. The system tracks both simple and proportional fairness metrics.",
                "source": "placeholder",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Default response
        return {
            "reply": f"I understand you're asking about: '{user_message}'. To provide better assistance, I can help with: analyzing if an offer is good, suggesting counteroffers, explaining the negotiation process, or discussing fairness metrics. Please ask a specific question about the negotiation.",
            "source": "placeholder",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "This is a placeholder response. Add GEMINI_API_KEY to environment for AI-powered responses."
        }


# Singleton instance
chat_service = ChatService()

