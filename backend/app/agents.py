import numpy as np
import math
import os
from typing import Tuple, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class WhaleManager:
    def __init__(self, threshold_share=0.2):
        self.threshold_share = threshold_share
    def detect(self, holdings_share: float) -> bool:
        return holdings_share >= self.threshold_share

class WashTradeDetector:
    def __init__(self):
        pass
    def suspicious(self, recent_pairs: list) -> bool:
        if len(recent_pairs) < 4:
            return False
        return len(set(recent_pairs[-4:])) < 4

class FeeOptimizer:
    def __init__(self):
        pass
    def estimate_fee(self, gas_price_gwei: float, gas_used: int=21000):
        return gas_price_gwei * 1e-9 * gas_used

class Reputation:
    def __init__(self):
        self.scores = {}
    def get(self, addr):
        return self.scores.get(addr, 0.5)
    def update(self, addr, delta):
        self.scores[addr] = max(0.0, min(1.0, self.get(addr) + delta))

class Limits:
    def __init__(self, max_offers=20):
        self.max_offers = max_offers
    def allowed(self, offer_count):
        return offer_count < self.max_offers

class AdaptiveAgent:
    def __init__(self, agent_id, actions, state_space_size, target_price=50, min_price=40, max_price=60, quantity=10):
        self.agent_id = agent_id
        self.actions = actions
        self.state_space_size = state_space_size
        self.q_table = np.zeros((state_space_size, len(actions)))
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9
        self.target_price = float(target_price)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.quantity = int(quantity)

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def update(self, state, action, reward, next_state):
        a_idx = self.actions.index(action)
        best_next = np.max(self.q_table[next_state])
        self.q_table[state, a_idx] += self.alpha * (reward + self.gamma * best_next - self.q_table[state, a_idx])

    def propose(self, last_offer_price=None):
        if last_offer_price is None:
            return self.target_price
        delta = last_offer_price - self.target_price
        return float(self.target_price + delta * 0.5)

    def utility(self, price: float) -> float:
        return 1.0 - abs(price - self.target_price) / max(1.0, abs(self.max_price - self.min_price))

class BaseAgent:
    def __init__(
        self, 
        address: str, 
        target_price: float, 
        min_price: float, 
        max_price: float, 
        quantity: int, 
        fairness_weight=0.5,
        concession_rate=0.05,
        aggressiveness=0.5,
        market_price: Optional[float] = None
    ):
        self.address = address
        self.target_price = float(target_price)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.quantity = int(quantity)
        self.fairness_weight = fairness_weight
        self.concession_rate = float(concession_rate)
        self.aggressiveness = float(aggressiveness)
        self.market_price = market_price
        self.agent_type = "buyer" if target_price < (min_price + max_price) / 2 else "seller"

    def propose(self, last_offer_price: float=None) -> float:
        if last_offer_price is None:
            if self.market_price:
                if self.agent_type == "buyer":
                    proposed = self.target_price - (self.target_price - self.market_price) * (1 - self.aggressiveness) * 0.3
                else:
                    proposed = self.target_price + (self.market_price - self.target_price) * (1 - self.aggressiveness) * 0.3
                return float(max(self.min_price, min(self.max_price, proposed)))
            return self.target_price
        
        delta = last_offer_price - self.target_price
        concession_factor = 0.5 + (1 - self.aggressiveness) * 0.3
        
        if self.market_price:
            if self.agent_type == "buyer":
                if self.market_price < last_offer_price:
                    concession_factor *= 0.9
            else:
                if self.market_price > last_offer_price:
                    concession_factor *= 0.9
        
        proposed = self.target_price + delta * concession_factor
        return float(max(self.min_price, min(self.max_price, proposed)))

    def utility(self, price: float) -> float:
        return 1.0 - abs(price - self.target_price) / max(1.0, abs(self.max_price - self.min_price))

def calculate_proportional_fairness(buyer_util: float, seller_util: float) -> float:
    epsilon = 1e-6
    buyer_log = math.log(max(epsilon, buyer_util))
    seller_log = math.log(max(epsilon, seller_util))
    return buyer_log + seller_log

from .explainer import explain_offer

def run_negotiation_loop(
    buyer_agent: BaseAgent, 
    seller_agent: BaseAgent, 
    max_rounds=8,
    use_tom: bool = False
):
    timeline = []
    last_buyer = None
    last_seller = None
    
    tom_buyer = None
    tom_seller = None
    if use_tom:
        try:
            from .theory_of_mind_agent import TheoryOfMindAgent
            tom_buyer = TheoryOfMindAgent(
                buyer_agent.address,
                buyer_agent.target_price,
                buyer_agent.min_price,
                buyer_agent.max_price,
                buyer_agent.quantity,
                buyer_agent.fairness_weight
            )
            tom_seller = TheoryOfMindAgent(
                seller_agent.address,
                seller_agent.target_price,
                seller_agent.min_price,
                seller_agent.max_price,
                seller_agent.quantity,
                seller_agent.fairness_weight
            )
        except ImportError:
            use_tom = False
    
    active_buyer = tom_buyer if tom_buyer else buyer_agent
    active_seller = tom_seller if tom_seller else seller_agent

    for r in range(1, max_rounds+1):
        bprice = active_buyer.propose(last_seller)
        buyer_util = buyer_agent.utility(bprice)
        
        sprice = active_seller.propose(bprice)
        seller_util = seller_agent.utility(sprice)
        
        simple_fairness = 1.0 - abs(buyer_util - seller_util)
        proportional_fairness = calculate_proportional_fairness(buyer_util, seller_util)
        
        buyer_tom_insights = None
        seller_tom_insights = None
        if use_tom and tom_buyer and tom_seller:
            buyer_tom_insights = tom_buyer.get_opponent_model_summary()
            seller_tom_insights = tom_seller.get_opponent_model_summary()
        
        buyer_explanation = explain_offer(
            "buyer", bprice, last_seller, buyer_agent.target_price,
            buyer_agent.concession_rate, buyer_agent.aggressiveness,
            simple_fairness, buyer_agent.market_price, buyer_tom_insights
        )
        seller_explanation = explain_offer(
            "seller", sprice, bprice, seller_agent.target_price,
            seller_agent.concession_rate, seller_agent.aggressiveness,
            simple_fairness, seller_agent.market_price, seller_tom_insights
        )
        
        timeline.append({
            "round": r,
            "buyer_offer": float(bprice),
            "seller_offer": float(sprice),
            "buyer_util": float(buyer_util),
            "seller_util": float(seller_util),
            "fairness": float(simple_fairness),
            "proportional_fairness": float(proportional_fairness),
            "buyer_explanation": buyer_explanation,
            "seller_explanation": seller_explanation,
            "buyer_tom_insights": buyer_tom_insights,
            "seller_tom_insights": seller_tom_insights,
            "market_price": buyer_agent.market_price or seller_agent.market_price
        })

        if abs(bprice - sprice) <= 1.0 or simple_fairness >= 0.9:
            final_price = (bprice + sprice) / 2.0
            final_buyer_util = buyer_agent.utility(final_price)
            final_seller_util = seller_agent.utility(final_price)
            final_simple_fairness = 1.0 - abs(final_buyer_util - final_seller_util)
            final_prop_fairness = calculate_proportional_fairness(final_buyer_util, final_seller_util)
            
            return timeline, {
                "price": float(final_price),
                "quantity": buyer_agent.quantity,
                "fairness": final_simple_fairness,
                "proportional_fairness": final_prop_fairness,
                "buyer_utility": float(final_buyer_util),
                "seller_utility": float(final_seller_util)
            }
        last_buyer, last_seller = bprice, sprice
    
    final_price = (last_buyer + last_seller) / 2.0
    final_buyer_util = buyer_agent.utility(final_price)
    final_seller_util = seller_agent.utility(final_price)
    final_simple_fairness = 1.0 - abs(final_buyer_util - final_seller_util)
    final_prop_fairness = calculate_proportional_fairness(final_buyer_util, final_seller_util)
    
    return timeline, {
        "price": float(final_price),
        "quantity": buyer_agent.quantity,
        "fairness": final_simple_fairness,
        "proportional_fairness": final_prop_fairness,
        "buyer_utility": float(final_buyer_util),
        "seller_utility": float(final_seller_util)
    }