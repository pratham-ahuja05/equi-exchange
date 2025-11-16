"""
Comprehensive tests for Unified Cognitive Negotiation Agent (UCNA)
Tests all 5 modules: Risk Scoring, Behavior Clustering, Acceptance Predictor,
Theory-of-Mind Belief Engine, and Optimization Layer
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.unified_agent import UnifiedNegotiationAgent
from app.utils import sigmoid


class TestRiskScoringModule:
    """Test Module 1: Risk Scoring Layer"""
    
    def test_risk_scoring_low_risk(self):
        """Test low risk scenario (old account, low amount)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        tx_data = {
            'amount': 100.0,      # Low amount
            'age_days': 365.0,    # Old account (1 year)
            'tx_count': 50        # Many transactions
        }
        
        result = agent.evaluate_risk(tx_data)
        
        assert 'risk_score' in result
        assert 'risk_label' in result
        assert 0.0 <= result['risk_score'] <= 1.0
        assert result['risk_label'] in ['low', 'medium', 'high']
        # Old account with many transactions should be low risk
        assert result['risk_score'] < 0.5
    
    def test_risk_scoring_high_risk(self):
        """Test high risk scenario (new account, high amount)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        tx_data = {
            'amount': 100000.0,   # High amount
            'age_days': 1.0,      # New account
            'tx_count': 1         # Few transactions
        }
        
        result = agent.evaluate_risk(tx_data)
        
        assert result['risk_label'] in ['low', 'medium', 'high']
        # New account with high amount should be higher risk
        assert result['risk_score'] > 0.3
    
    def test_risk_scoring_medium_risk(self):
        """Test medium risk scenario"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        tx_data = {
            'amount': 1000.0,
            'age_days': 90.0,
            'tx_count': 10
        }
        
        result = agent.evaluate_risk(tx_data)
        assert result['risk_label'] in ['low', 'medium', 'high']


class TestBehaviorClusteringModule:
    """Test Module 2: Behavior Clustering Layer"""
    
    def test_cluster_stubborn(self):
        """Test clustering stubborn behavior (low concessions)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Stubborn: very small concessions (< 2%)
        offer_history = [100.0, 100.5, 100.8, 101.0, 101.2]
        
        result = agent.cluster_behavior(offer_history)
        
        assert 'cluster' in result
        assert 'cluster_score' in result
        assert 'avg_concession_pct' in result
        assert result['cluster'] == 'stubborn'
        assert result['cluster_score'] > 0.7  # High stubbornness score
    
    def test_cluster_cooperative(self):
        """Test clustering cooperative behavior (high concessions)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Cooperative: large concessions (> 7%)
        offer_history = [100.0, 92.0, 85.0, 78.0, 72.0]
        
        result = agent.cluster_behavior(offer_history)
        
        assert result['cluster'] == 'cooperative'
        assert result['cluster_score'] < 0.3  # Low stubbornness (high cooperation)
    
    def test_cluster_moderate(self):
        """Test clustering moderate behavior"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Moderate: medium concessions (2-7%)
        offer_history = [100.0, 97.0, 94.0, 91.0, 88.0]
        
        result = agent.cluster_behavior(offer_history)
        
        assert result['cluster'] == 'moderate'
        assert 0.3 <= result['cluster_score'] <= 0.7
    
    def test_cluster_insufficient_data(self):
        """Test clustering with insufficient data"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Only one offer
        offer_history = [100.0]
        
        result = agent.cluster_behavior(offer_history)
        
        assert result['cluster'] == 'moderate'  # Default
        assert result['cluster_score'] == 0.5


class TestAcceptancePredictorModule:
    """Test Module 3: Offer Acceptance Predictor"""
    
    def test_predict_reject(self):
        """Test prediction for rejected offer (too low)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Offer below fair range (target * 0.95 = 95.0)
        offer = 90.0
        target_price = 100.0
        
        result = agent.predict_acceptance(offer, target_price)
        
        assert 'prediction' in result
        assert 'acceptance_probability' in result
        assert 'fair_low' in result
        assert 'fair_high' in result
        assert result['prediction'] == 'reject'
        assert result['acceptance_probability'] < 0.5
    
    def test_predict_likely_accept(self):
        """Test prediction for likely acceptance (fair range)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Offer in fair range (95-105)
        offer = 100.0
        target_price = 100.0
        
        result = agent.predict_acceptance(offer, target_price)
        
        assert result['prediction'] == 'likely_accept'
        assert result['acceptance_probability'] > 0.7
    
    def test_predict_overpay_accept(self):
        """Test prediction for overpay acceptance (too high)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Offer above fair range (target * 1.05 = 105.0)
        offer = 110.0
        target_price = 100.0
        
        result = agent.predict_acceptance(offer, target_price)
        
        assert result['prediction'] == 'overpay_accept'
        assert result['acceptance_probability'] > 0.9


class TestTheoryOfMindModule:
    """Test Module 4: Theory-of-Mind Belief Engine"""
    
    def test_initial_beliefs(self):
        """Test initial belief state"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        beliefs = agent.get_beliefs()
        
        assert 'belief_target_price' in beliefs
        assert 'belief_stubbornness' in beliefs
        assert 'belief_patience' in beliefs
        assert beliefs['belief_target_price'] is None  # Not initialized yet
        assert 0.0 <= beliefs['belief_stubbornness'] <= 1.0
        assert 0.0 <= beliefs['belief_patience'] <= 1.0
    
    def test_update_beliefs_first_offer(self):
        """Test updating beliefs with first opponent offer"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # First offer
        agent.update_beliefs(95.0)
        
        beliefs = agent.get_beliefs()
        
        assert beliefs['belief_target_price'] == 95.0  # Initialized to first offer
        assert len(agent.opponent_offer_history) == 1
    
    def test_update_beliefs_exponential_average(self):
        """Test exponential moving average for target price"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Update with multiple offers
        agent.update_beliefs(95.0)   # First: sets to 95.0
        agent.update_beliefs(93.0)   # Second: 0.7*95 + 0.3*93 = 94.4
        agent.update_beliefs(91.0)   # Third: 0.7*94.4 + 0.3*91 = 93.38
        
        beliefs = agent.get_beliefs()
        
        # Should converge toward recent offers
        assert beliefs['belief_target_price'] is not None
        assert 90.0 < beliefs['belief_target_price'] < 96.0
    
    def test_update_beliefs_stubbornness(self):
        """Test stubbornness update from behavior clustering"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Add stubborn offers (small concessions)
        agent.update_beliefs(100.0)
        agent.update_beliefs(100.5)
        agent.update_beliefs(100.8)
        
        beliefs = agent.get_beliefs()
        
        # Should detect stubbornness
        assert beliefs['belief_stubbornness'] > 0.5  # High stubbornness


class TestOptimizationModule:
    """Test Module 5: Optimization Layer"""
    
    def test_optimization_basic(self):
        """Test basic optimization functionality"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        risk_score = 0.3
        stubbornness = 0.5
        
        result = agent.optimize_offer(None, risk_score, stubbornness)
        
        assert 'best_price' in result
        assert 'max_score' in result
        assert 'score_details' in result
        assert agent.min_price <= result['best_price'] <= agent.max_price
        assert 'utility' in result['score_details']
        assert 'fairness' in result['score_details']
    
    def test_optimization_with_opponent_offer(self):
        """Test optimization with opponent offer context"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Set up beliefs
        agent.beliefs['belief_target_price'] = 95.0
        
        risk_score = 0.2
        stubbornness = 0.3
        
        result = agent.optimize_offer(95.0, risk_score, stubbornness)
        
        assert result['best_price'] is not None
        assert result['max_score'] > float('-inf')
    
    def test_optimization_weights(self):
        """Test that optimization respects weights"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1,
            optimization_weights={
                'utility': 0.8,      # High utility weight
                'fairness': 0.1,
                'risk': 0.05,
                'stubbornness': 0.05
            }
        )
        
        result = agent.optimize_offer(None, 0.5, 0.5)
        
        # With high utility weight, should favor prices closer to target
        assert abs(result['best_price'] - agent.target_price) < 10.0


class TestUnifiedAgentIntegration:
    """Integration tests for full UCNA agent"""
    
    def test_propose_first_round(self):
        """Test proposal in first round (no opponent offer)"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        result = agent.propose(None)
        
        assert 'price' in result
        assert 'risk_evaluation' in result
        assert 'behavior_cluster' in result
        assert 'acceptance_prediction' in result
        assert 'beliefs' in result
        assert 'optimization' in result
        assert 'explanation' in result
        
        assert agent.min_price <= result['price'] <= agent.max_price
    
    def test_propose_with_opponent_offer(self):
        """Test proposal with opponent offer history"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Simulate negotiation rounds
        result1 = agent.propose(None)  # First round
        result2 = agent.propose(95.0)  # Second round with opponent offer
        result3 = agent.propose(93.0)  # Third round
        
        # Should adapt based on opponent behavior
        assert result2['price'] != result1['price']
        assert result3['price'] != result2['price']
        
        # Beliefs should be updated
        assert agent.beliefs['belief_target_price'] is not None
    
    def test_propose_explanation(self):
        """Test that explanation is generated"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        result = agent.propose(95.0)
        
        assert 'explanation' in result
        assert len(result['explanation']) > 0
        assert 'Proposed price' in result['explanation']
    
    def test_utility_compatibility(self):
        """Test that utility method works correctly"""
        agent = UnifiedNegotiationAgent(
            address="0x123",
            target_price=100.0,
            min_price=80.0,
            max_price=120.0,
            quantity=1
        )
        
        # Utility at target should be high
        util_at_target = agent.utility(100.0)
        assert util_at_target > 0.9
        
        # Utility at edge should be lower
        util_at_edge = agent.utility(80.0)
        assert util_at_edge < util_at_target


class TestSigmoidFunction:
    """Test sigmoid utility function"""
    
    def test_sigmoid_zero(self):
        """Test sigmoid at zero"""
        result = sigmoid(0.0)
        assert abs(result - 0.5) < 0.01
    
    def test_sigmoid_positive(self):
        """Test sigmoid for positive values"""
        result = sigmoid(5.0)
        assert 0.5 < result < 1.0
    
    def test_sigmoid_negative(self):
        """Test sigmoid for negative values"""
        result = sigmoid(-5.0)
        assert 0.0 < result < 0.5
    
    def test_sigmoid_extreme_values(self):
        """Test sigmoid with extreme values (should not overflow)"""
        result_large = sigmoid(1000.0)
        result_small = sigmoid(-1000.0)
        
        assert 0.0 <= result_large <= 1.0
        assert 0.0 <= result_small <= 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

