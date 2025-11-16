"""
Unified Cognitive Negotiation Agent (UCNA)
Integrates 5 AI-inspired modules for intelligent negotiation:
1. Risk Scoring Layer (Logistic Regression-like)
2. Behavior Clustering Layer (K-Means-like)
3. Offer Acceptance Predictor (Decision Tree-like)
4. Theory-of-Mind Belief Engine
5. Optimization Layer (Multi-objective)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from .agents import BaseAgent
from .utils import sigmoid


class UnifiedNegotiationAgent(BaseAgent):
    """
    Advanced negotiation agent that combines multiple cognitive modules
    for intelligent, explainable decision-making.
    """
    
    def __init__(
        self,
        address: str,
        target_price: float,
        min_price: float,
        max_price: float,
        quantity: int,
        fairness_weight: float = 0.5,
        concession_rate: float = 0.05,
        aggressiveness: float = 0.5,
        market_price: Optional[float] = None,
        risk_weights: Optional[Dict[str, float]] = None,
        optimization_weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize UCNA with negotiation parameters
        
        Args:
            address: Agent's blockchain address
            target_price: Desired price
            min_price: Minimum acceptable price
            max_price: Maximum acceptable price
            quantity: Quantity to trade
            fairness_weight: Weight for fairness (0-1)
            concession_rate: Base concession rate
            aggressiveness: Aggressiveness level (0-1)
            market_price: Current market price (optional)
            risk_weights: Custom weights for risk scoring {amount, age, tx_count}
            optimization_weights: Custom weights for optimization {utility, fairness, risk, stubbornness}
        """
        super().__init__(
            address, target_price, min_price, max_price, quantity,
            fairness_weight, concession_rate, aggressiveness, market_price
        )
        
        # Risk scoring parameters (logistic regression-like)
        self.risk_weights = risk_weights or {
            'amount': 0.001,      # a1: amount coefficient
            'age_days': -0.01,    # a2: account age coefficient (negative = older = safer)
            'tx_count': 0.0001    # a3: transaction count coefficient
        }
        
        # Optimization weights (multi-objective)
        self.opt_weights = optimization_weights or {
            'utility': 0.4,       # w1: utility weight
            'fairness': 0.3,      # w2: fairness weight
            'risk': 0.2,          # w3: risk penalty weight
            'stubbornness': 0.1   # w4: opponent stubbornness penalty weight
        }
        
        # Theory-of-Mind beliefs
        self.beliefs = {
            'belief_target_price': None,      # Estimated opponent target price
            'belief_stubbornness': 0.5,       # 0=cooperative, 1=stubborn
            'belief_patience': 0.5            # 0=impatient, 1=patient
        }
        
        # Offer history tracking
        self.opponent_offer_history: List[float] = []
        self.my_offer_history: List[float] = []
        self.round_count = 0
        
        # Behavior cluster cache
        self._cached_cluster = None
        self._cached_cluster_score = None
    
    # ========================================================================
    # MODULE 1: RISK SCORING LAYER (Logistic Regression-like)
    # ========================================================================
    
    def evaluate_risk(self, tx_data: Dict) -> Dict:
        """
        Evaluate transaction risk using logistic regression-like scoring
        
        Args:
            tx_data: {
                'amount': float,      # Transaction amount
                'age_days': float,    # Account age in days
                'tx_count': int        # Number of previous transactions
            }
        
        Returns:
            {
                'risk_score': float,      # 0-1 risk score
                'risk_label': str          # 'low', 'medium', or 'high'
            }
        """
        amount = tx_data.get('amount', 0.0)
        age_days = tx_data.get('age_days', 0.0)
        tx_count = tx_data.get('tx_count', 0)
        
        # Compute linear combination (logistic regression input)
        # risk = sigmoid(a1*amount + a2*age_days + a3*tx_count)
        linear_combination = (
            self.risk_weights['amount'] * amount +
            self.risk_weights['age_days'] * age_days +
            self.risk_weights['tx_count'] * tx_count
        )
        
        # Apply sigmoid to get risk score (0-1)
        risk_score = sigmoid(linear_combination)
        
        # Classify risk level
        if risk_score < 0.33:
            risk_label = "low"
        elif risk_score < 0.67:
            risk_label = "medium"
        else:
            risk_label = "high"
        
        return {
            "risk_score": float(risk_score),
            "risk_label": risk_label
        }
    
    # ========================================================================
    # MODULE 2: BEHAVIOR CLUSTERING LAYER (K-Means-like)
    # ========================================================================
    
    def cluster_behavior(self, offer_history: List[float]) -> Dict:
        """
        Classify opponent behavior into clusters: stubborn, moderate, cooperative
        
        Uses heuristic based on average concession rate between offers
        
        Args:
            offer_history: List of opponent's previous offers
        
        Returns:
            {
                'cluster': str,           # 'stubborn', 'moderate', or 'cooperative'
                'cluster_score': float,   # Numeric score (0-1)
                'avg_concession_pct': float  # Average concession percentage
            }
        """
        if len(offer_history) < 2:
            # Not enough data - default to moderate
            return {
                'cluster': 'moderate',
                'cluster_score': 0.5,
                'avg_concession_pct': 0.0
            }
        
        # Calculate concessions between consecutive offers
        concessions = []
        for i in range(len(offer_history) - 1):
            prev_offer = offer_history[i]
            curr_offer = offer_history[i + 1]
            
            if prev_offer > 0:
                # Calculate percentage change (concession)
                concession_pct = abs(curr_offer - prev_offer) / prev_offer * 100
                concessions.append(concession_pct)
        
        if not concessions:
            return {
                'cluster': 'moderate',
                'cluster_score': 0.5,
                'avg_concession_pct': 0.0
            }
        
        # Average concession percentage
        avg_concession_pct = np.mean(concessions)
        
        # Classify based on concession rate
        if avg_concession_pct < 2.0:
            cluster = "stubborn"
            cluster_score = 0.9  # High stubbornness
        elif avg_concession_pct < 7.0:
            cluster = "moderate"
            cluster_score = 0.5  # Medium stubbornness
        else:
            cluster = "cooperative"
            cluster_score = 0.1  # Low stubbornness (high cooperation)
        
        return {
            'cluster': cluster,
            'cluster_score': float(cluster_score),
            'avg_concession_pct': float(avg_concession_pct)
        }
    
    # ========================================================================
    # MODULE 3: OFFER ACCEPTANCE PREDICTOR (Decision Tree-like)
    # ========================================================================
    
    def predict_acceptance(self, offer: float, target_price: float) -> Dict:
        """
        Predict if opponent will accept an offer using threshold-based logic
        
        Args:
            offer: Proposed offer price
            target_price: Opponent's estimated target price
        
        Returns:
            {
                'prediction': str,        # 'reject', 'likely_accept', or 'overpay_accept'
                'acceptance_probability': float,  # 0-1 probability
                'fair_low': float,        # Lower fair threshold
                'fair_high': float        # Upper fair threshold
            }
        """
        # Define fair price range (±5% of target)
        fair_low = target_price * 0.95
        fair_high = target_price * 1.05
        
        # Decision tree-like logic
        if offer < fair_low:
            prediction = "reject"
            acceptance_probability = 0.2  # Low probability
        elif fair_low <= offer <= fair_high:
            prediction = "likely_accept"
            acceptance_probability = 0.8  # High probability
        else:  # offer > fair_high
            prediction = "overpay_accept"
            acceptance_probability = 0.95  # Very high (but we're overpaying)
        
        return {
            'prediction': prediction,
            'acceptance_probability': float(acceptance_probability),
            'fair_low': float(fair_low),
            'fair_high': float(fair_high)
        }
    
    # ========================================================================
    # MODULE 4: THEORY-OF-MIND BELIEF ENGINE
    # ========================================================================
    
    def get_beliefs(self) -> Dict:
        """
        Get current beliefs about opponent
        
        Returns:
            {
                'belief_target_price': float or None,
                'belief_stubbornness': float,
                'belief_patience': float
            }
        """
        return self.beliefs.copy()
    
    def update_beliefs(self, opponent_offer: float) -> None:
        """
        Update ToM beliefs based on opponent's latest offer
        
        Uses exponential moving average for target price estimation
        Updates stubbornness from behavior clustering
        Updates patience from concession speed
        
        Args:
            opponent_offer: Opponent's latest offer price
        """
        self.opponent_offer_history.append(opponent_offer)
        self.round_count += 1
        
        # Update belief_target_price using exponential moving average
        # belief_target_price = 0.7*old + 0.3*last_offer
        if self.beliefs['belief_target_price'] is None:
            # Initialize with first offer
            self.beliefs['belief_target_price'] = opponent_offer
        else:
            # Exponential moving average
            self.beliefs['belief_target_price'] = (
                0.7 * self.beliefs['belief_target_price'] +
                0.3 * opponent_offer
            )
        
        # Update belief_stubbornness from behavior clustering
        if len(self.opponent_offer_history) >= 2:
            cluster_result = self.cluster_behavior(self.opponent_offer_history)
            self._cached_cluster = cluster_result['cluster']
            self._cached_cluster_score = cluster_result['cluster_score']
            
            # Map cluster score to stubbornness (0=cooperative, 1=stubborn)
            self.beliefs['belief_stubbornness'] = cluster_result['cluster_score']
        
        # Update belief_patience based on concession speed
        if len(self.opponent_offer_history) >= 2:
            # Calculate how fast opponent is moving toward agreement
            first_offer = self.opponent_offer_history[0]
            last_offer = self.opponent_offer_history[-1]
            total_movement = abs(last_offer - first_offer)
            
            # Expected movement if patient (slow concessions)
            price_range = self.max_price - self.min_price
            expected_movement_patient = price_range * 0.1 * self.round_count
            
            if total_movement < expected_movement_patient:
                # Moving slowly = patient
                self.beliefs['belief_patience'] = 0.8
            elif total_movement > expected_movement_patient * 2:
                # Moving quickly = impatient
                self.beliefs['belief_patience'] = 0.2
            else:
                # Moderate movement
                self.beliefs['belief_patience'] = 0.5
    
    # ========================================================================
    # MODULE 5: OPTIMIZATION LAYER (Multi-objective)
    # ========================================================================
    
    def optimize_offer(
        self,
        opponent_offer: Optional[float],
        risk_score: float,
        stubbornness: float
    ) -> Dict:
        """
        Optimize offer price using multi-objective scoring
        
        Score = w1*utility + w2*fairness - w3*risk_score - w4*stubbornness
        
        Searches over price range to find optimal offer
        
        Args:
            opponent_offer: Opponent's last offer (None if first round)
            risk_score: Risk score from risk evaluation (0-1)
            stubbornness: Opponent's stubbornness score (0-1)
        
        Returns:
            {
                'best_price': float,
                'max_score': float,
                'score_details': {
                    'utility': float,
                    'fairness': float,
                    'risk_penalty': float,
                    'stubbornness_penalty': float
                }
            }
        """
        # Generate candidate prices (20 points across price range)
        candidate_prices = np.linspace(self.min_price, self.max_price, 20)
        
        best_price = self.target_price
        max_score = float('-inf')
        best_details = {}
        
        # Estimate opponent utility (for fairness calculation)
        # If we don't know opponent's target, use midpoint assumption
        if opponent_offer is not None and self.beliefs['belief_target_price'] is not None:
            opponent_target = self.beliefs['belief_target_price']
        else:
            # Default: assume opponent wants opposite of our target
            midpoint = (self.min_price + self.max_price) / 2.0
            opponent_target = midpoint + (midpoint - self.target_price)
        
        opponent_min = self.min_price
        opponent_max = self.max_price
        
        # Evaluate each candidate price
        for price in candidate_prices:
            # Calculate utility (normalized 0-1)
            utility = self.utility(price)
            
            # Calculate fairness
            # Estimate opponent utility at this price
            opponent_util = 1.0 - abs(price - opponent_target) / max(1.0, abs(opponent_max - opponent_min))
            fairness = 1.0 - abs(utility - opponent_util)
            
            # Calculate multi-objective score
            score = (
                self.opt_weights['utility'] * utility +
                self.opt_weights['fairness'] * fairness -
                self.opt_weights['risk'] * risk_score -
                self.opt_weights['stubbornness'] * stubbornness
            )
            
            # Track best score
            if score > max_score:
                max_score = score
                best_price = price
                best_details = {
                    'utility': float(utility),
                    'fairness': float(fairness),
                    'risk_penalty': float(self.opt_weights['risk'] * risk_score),
                    'stubbornness_penalty': float(self.opt_weights['stubbornness'] * stubbornness)
                }
        
        return {
            'best_price': float(best_price),
            'max_score': float(max_score),
            'score_details': best_details
        }
    
    # ========================================================================
    # MAIN PROPOSAL METHOD
    # ========================================================================
    
    def propose(self, last_offer: Optional[float] = None) -> Dict:
        """
        Main proposal method that integrates all 5 modules
        
        Process:
        1. Evaluate risk
        2. Cluster opponent behavior
        3. Update ToM beliefs
        4. Predict acceptance
        5. Optimize final price
        6. Return full result dict
        
        Args:
            last_offer: Opponent's last offer (None if first round)
        
        Returns:
            {
                'price': float,                    # Proposed price
                'risk_evaluation': Dict,            # Risk scoring results
                'behavior_cluster': Dict,            # Behavior classification
                'acceptance_prediction': Dict,       # Acceptance prediction
                'beliefs': Dict,                     # Current ToM beliefs
                'optimization': Dict,                # Optimization results
                'explanation': str                   # Human-readable explanation
            }
        """
        # Default transaction data (can be enhanced with real blockchain data)
        tx_data = {
            'amount': abs(self.target_price * self.quantity),
            'age_days': 30.0,  # Default - can be fetched from blockchain
            'tx_count': 10     # Default - can be fetched from blockchain
        }
        
        # MODULE 1: Evaluate risk
        risk_eval = self.evaluate_risk(tx_data)
        risk_score = risk_eval['risk_score']
        
        # MODULE 2: Cluster behavior (if we have offer history)
        if last_offer is not None and len(self.opponent_offer_history) > 0:
            behavior_cluster = self.cluster_behavior(self.opponent_offer_history)
        else:
            behavior_cluster = {
                'cluster': 'moderate',
                'cluster_score': 0.5,
                'avg_concession_pct': 0.0
            }
        
        # MODULE 3: Update ToM beliefs
        if last_offer is not None:
            self.update_beliefs(last_offer)
        
        # Get current beliefs
        beliefs = self.get_beliefs()
        stubbornness = beliefs['belief_stubbornness']
        
        # MODULE 4: Predict acceptance (if we have target estimate)
        if beliefs['belief_target_price'] is not None:
            # Use estimated target for prediction
            acceptance_pred = self.predict_acceptance(
                self.target_price,  # Our target as test offer
                beliefs['belief_target_price']
            )
        else:
            acceptance_pred = {
                'prediction': 'unknown',
                'acceptance_probability': 0.5,
                'fair_low': self.min_price,
                'fair_high': self.max_price
            }
        
        # MODULE 5: Optimize offer
        optimization = self.optimize_offer(last_offer, risk_score, stubbornness)
        proposed_price = optimization['best_price']
        
        # Record our offer
        self.my_offer_history.append(proposed_price)
        
        # Generate explanation
        explanation = self._generate_explanation(
            proposed_price, risk_eval, behavior_cluster, 
            acceptance_pred, beliefs, optimization
        )
        
        return {
            'price': proposed_price,
            'risk_evaluation': risk_eval,
            'behavior_cluster': behavior_cluster,
            'acceptance_prediction': acceptance_pred,
            'beliefs': beliefs,
            'optimization': optimization,
            'explanation': explanation
        }
    
    def _generate_explanation(
        self,
        price: float,
        risk_eval: Dict,
        behavior_cluster: Dict,
        acceptance_pred: Dict,
        beliefs: Dict,
        optimization: Dict
    ) -> str:
        """
        Generate human-readable explanation of the proposal
        """
        parts = []
        parts.append(f"Proposed price: ${price:.2f}")
        parts.append(f"Risk: {risk_eval['risk_label']} ({risk_eval['risk_score']:.2%})")
        parts.append(f"Opponent behavior: {behavior_cluster['cluster']}")
        
        if beliefs['belief_target_price'] is not None:
            parts.append(f"Estimated opponent target: ${beliefs['belief_target_price']:.2f}")
        
        parts.append(f"Acceptance probability: {acceptance_pred['acceptance_probability']:.1%}")
        parts.append(f"Optimization score: {optimization['max_score']:.3f}")
        
        return " | ".join(parts)
    
    # Override utility method to maintain compatibility
    def utility(self, price: float) -> float:
        """Same utility function as base agent"""
        return super().utility(price)
    
    def propose_price(self, last_offer: Optional[float] = None) -> float:
        """
        Compatibility method: returns just the price (float)
        For integration with existing negotiation loops that expect float return
        """
        result = self.propose(last_offer)
        return result['price']

