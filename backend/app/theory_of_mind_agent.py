"""
Theory of Mind Agent Implementation
Models opponent's mental state and adapts strategy accordingly
"""

import numpy as np
from typing import List, Dict, Optional
from .agents import BaseAgent


class TheoryOfMindAgent(BaseAgent):
    """
    Enhanced agent that models opponent's beliefs, desires, and intentions
    (Theory of Mind - ToM)
    """
    
    def __init__(self, address: str, target_price: float, min_price: float, 
                 max_price: float, quantity: int, fairness_weight=0.5, 
                 tom_level=2):
        """
        Args:
            tom_level: 0=no ToM, 1=first-order (models opponent), 
                      2=second-order (models opponent modeling me)
        """
        super().__init__(address, target_price, min_price, max_price, 
                        quantity, fairness_weight)
        self.tom_level = tom_level
        self.opponent_model = {
            'target_price_estimate': None,
            'min_price_estimate': None,
            'max_price_estimate': None,
            'concession_rate_estimate': 0.05,
            'patience_level': 0.5,  # 0=impatient, 1=very patient
            'fairness_preference': 0.5,
            'risk_aversion': 0.5,
            'strategy_type': None,  # 'aggressive', 'cooperative', 'stubborn'
            'belief_confidence': 0.0  # How confident we are in our model
        }
        self.opponent_offer_history: List[float] = []
        self.my_offer_history: List[float] = []
        self.round_count = 0
        
    def update_opponent_model(self, opponent_offer: float, my_last_offer: Optional[float]):
        """
        Update beliefs about opponent based on their offer
        Implements recursive reasoning: "What does their offer tell me about what they think?"
        """
        self.opponent_offer_history.append(opponent_offer)
        if my_last_offer is not None:
            self.my_offer_history.append(my_last_offer)
        
        self.round_count += 1
        
        # First-order ToM: Model opponent's strategy
        if len(self.opponent_offer_history) >= 2:
            # Estimate concession rate
            concessions = []
            for i in range(len(self.opponent_offer_history) - 1):
                if self.opponent_offer_history[i] is not None:
                    concession = abs(self.opponent_offer_history[i] - 
                                    self.opponent_offer_history[i+1])
                    concessions.append(concession)
            
            if concessions:
                avg_concession = np.mean(concessions)
                self.opponent_model['concession_rate_estimate'] = avg_concession
                
                # Classify strategy
                if avg_concession > 0.1:
                    self.opponent_model['strategy_type'] = 'cooperative'
                elif avg_concession < 0.02:
                    self.opponent_model['strategy_type'] = 'stubborn'
                else:
                    self.opponent_model['strategy_type'] = 'moderate'
        
        # Estimate target price (extrapolate from trend)
        if len(self.opponent_offer_history) >= 3:
            offers = np.array(self.opponent_offer_history[-5:])  # Last 5 offers
            rounds = np.arange(len(offers))
            
            # Linear regression to estimate target
            if len(offers) > 1:
                coeffs = np.polyfit(rounds, offers, 1)
                # Extrapolate to "round infinity" (target price)
                estimated_target = coeffs[1]  # y-intercept
                
                # Update estimate with confidence weighting
                confidence = min(1.0, len(offers) / 10.0)
                if self.opponent_model['target_price_estimate'] is None:
                    self.opponent_model['target_price_estimate'] = estimated_target
                else:
                    # Weighted average
                    self.opponent_model['target_price_estimate'] = (
                        confidence * estimated_target + 
                        (1 - confidence) * self.opponent_model['target_price_estimate']
                    )
                self.opponent_model['belief_confidence'] = confidence
        
        # Estimate patience (based on how much they're moving)
        if len(self.opponent_offer_history) >= 2:
            total_movement = abs(self.opponent_offer_history[0] - 
                               self.opponent_offer_history[-1])
            expected_movement = self.round_count * 0.05 * (self.max_price - self.min_price)
            
            if total_movement < expected_movement * 0.5:
                self.opponent_model['patience_level'] = 0.8  # Very patient
            elif total_movement > expected_movement * 1.5:
                self.opponent_model['patience_level'] = 0.2  # Impatient
        
        # Second-order ToM: Model what opponent thinks about me
        if self.tom_level >= 2 and my_last_offer is not None:
            # "What does the opponent think my target price is?"
            # "What does the opponent think my concession rate is?"
            # This would require recursive modeling (simplified here)
            pass
    
    def propose(self, last_offer_price: float = None) -> float:
        """
        Strategic proposal using Theory of Mind reasoning
        """
        if last_offer_price is None:
            # First offer: start at target
            return self.target_price
        
        # Update our model of the opponent
        my_last = self.my_offer_history[-1] if self.my_offer_history else None
        self.update_opponent_model(last_offer_price, my_last)
        
        # Strategic decision based on opponent model
        strategy = self.opponent_model['strategy_type']
        confidence = self.opponent_model['belief_confidence']
        
        if confidence < 0.3:
            # Low confidence: use default strategy
            delta = last_offer_price - self.target_price
            return float(self.target_price + delta * 0.5)
        
        # High confidence: use ToM-informed strategy
        if strategy == 'cooperative':
            # Opponent is cooperative - we can be slightly more aggressive
            # but still fair
            delta = last_offer_price - self.target_price
            concession_factor = 0.4  # Less concession needed
            proposed = self.target_price + delta * concession_factor
            
        elif strategy == 'stubborn':
            # Opponent is stubborn - we need to concede more
            delta = last_offer_price - self.target_price
            concession_factor = 0.7  # More concession
            proposed = self.target_price + delta * concession_factor
            
        else:  # moderate
            # Balanced approach
            delta = last_offer_price - self.target_price
            concession_factor = 0.5
            proposed = self.target_price + delta * concession_factor
        
        # Adjust based on estimated opponent target
        if self.opponent_model['target_price_estimate'] is not None:
            opponent_target = self.opponent_model['target_price_estimate']
            midpoint = (self.target_price + opponent_target) / 2.0
            
            # Bias toward midpoint if we want fairness
            if self.fairness_weight > 0.5:
                proposed = (1 - self.fairness_weight) * proposed + \
                          self.fairness_weight * midpoint
        
        # Adjust based on patience
        patience = self.opponent_model['patience_level']
        if patience > 0.7:
            # Opponent is patient - we can hold firm longer
            proposed = 0.7 * proposed + 0.3 * self.target_price
        elif patience < 0.3:
            # Opponent is impatient - we can be more aggressive
            proposed = 0.9 * proposed + 0.1 * self.target_price
        
        # Ensure within bounds
        proposed = max(self.min_price, min(self.max_price, proposed))
        
        # Record our offer
        self.my_offer_history.append(proposed)
        
        return float(proposed)
    
    def get_opponent_model_summary(self) -> Dict:
        """Return summary of opponent model for explainability"""
        return {
            'target_price_estimate': self.opponent_model['target_price_estimate'],
            'strategy_type': self.opponent_model['strategy_type'],
            'concession_rate_estimate': self.opponent_model['concession_rate_estimate'],
            'patience_level': self.opponent_model['patience_level'],
            'belief_confidence': self.opponent_model['belief_confidence'],
            'rounds_observed': len(self.opponent_offer_history)
        }
    
    def utility(self, price: float) -> float:
        """Same utility function as base agent"""
        return super().utility(price)


def run_tom_negotiation_loop(buyer_agent: TheoryOfMindAgent, 
                              seller_agent: TheoryOfMindAgent, 
                              max_rounds=8):
    """
    Negotiation loop with Theory of Mind agents
    Returns timeline with ToM insights
    """
    timeline = []
    last_buyer = None
    last_seller = None
    
    for r in range(1, max_rounds + 1):
        # Buyer proposes (with ToM reasoning)
        bprice = buyer_agent.propose(last_seller)
        buyer_util = buyer_agent.utility(bprice)
        buyer_tom = buyer_agent.get_opponent_model_summary()
        
        # Seller responds (with ToM reasoning)
        sprice = seller_agent.propose(bprice)
        seller_util = seller_agent.utility(sprice)
        seller_tom = seller_agent.get_opponent_model_summary()
        
        # Fairness calculation
        fairness = 1.0 - abs(buyer_util - seller_util)
        
        timeline.append({
            "round": r,
            "buyer_offer": float(bprice),
            "seller_offer": float(sprice),
            "buyer_util": float(buyer_util),
            "seller_util": float(seller_util),
            "fairness": float(fairness),
            "buyer_tom_insights": buyer_tom,
            "seller_tom_insights": seller_tom
        })
        
        # Check convergence
        if abs(bprice - sprice) <= 1.0 or fairness >= 0.9:
            final_price = (bprice + sprice) / 2.0
            return timeline, {
                "price": float(final_price),
                "quantity": buyer_agent.quantity,
                "fairness": fairness,
                "rounds": r
            }
        
        last_buyer, last_seller = bprice, sprice
    
    # Max rounds reached
    final_price = (last_buyer + last_seller) / 2.0
    return timeline, {
        "price": float(final_price),
        "quantity": buyer_agent.quantity,
        "fairness": timeline[-1]["fairness"] if timeline else 1.0,
        "rounds": max_rounds
    }

