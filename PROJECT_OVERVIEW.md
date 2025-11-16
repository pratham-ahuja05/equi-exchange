# EquiExchange - Comprehensive Project Overview

## 🎯 What the Project Does

**EquiExchange** is a **decentralized trading platform** that automates price negotiations between buyers and sellers using AI agents, then records finalized agreements on the Ethereum blockchain. It's a complete Web3 application combining:

1. **AI-Powered Negotiation Engine**: Automated buyer/seller agents that negotiate prices through multiple rounds
2. **Fairness-Optimized Trading**: Agents optimize for both individual utility and mutual fairness
3. **Blockchain Recording**: Immutable agreement storage on Ethereum smart contracts
4. **Real-Time Web Interface**: Next.js frontend with wallet integration (MetaMask/RainbowKit)

---

## 🧠 Models & Algorithms Used

### 1. **BaseAgent (Heuristic-Based Negotiation)**
- **Type**: Rule-based agent with simple concession logic
- **Strategy**: 
  - Initial offer: Target price
  - Subsequent offers: Move 50% toward opponent's last offer
  - Concession rate: 5% per round (configurable)
- **Utility Function**: 
  ```
  utility(price) = 1 - |price - target_price| / |max_price - min_price|
  ```
- **Fairness Calculation**: 
  ```
  fairness = 1 - |buyer_utility - seller_utility|
  ```

### 2. **AdaptiveAgent (Q-Learning Reinforcement Learning)**
- **Type**: Q-Learning with ε-greedy exploration
- **Components**:
  - Q-table: State-action value function
  - State space: Round number (discretized)
  - Action space: Discrete price offers
  - Reward: Fairness score from negotiation outcome
- **Hyperparameters**:
  - Learning rate (α): 0.5
  - Discount factor (γ): 0.9
  - Exploration rate (ε): 0.1
- **Update Rule** (Q-Learning):
  ```
  Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
  ```

### 3. **Negotiation Loop Algorithm**
- **Process**:
  1. Buyer proposes price (based on last seller offer or target)
  2. Seller responds (based on buyer's offer)
  3. Calculate utilities and fairness
  4. Check termination: `|buyer_price - seller_price| ≤ 1.0` OR `fairness ≥ 0.9`
  5. If not terminated, continue to next round
  6. Max rounds: 8 (configurable)
- **Final Agreement**: Midpoint of last offers if no convergence

### 4. **Supporting Models**
- **WhaleManager**: Detects large holders (threshold: 20% of supply)
- **WashTradeDetector**: Identifies suspicious repeated trading patterns
- **FeeOptimizer**: Estimates gas costs for transactions
- **Reputation System**: Tracks address reputation scores (0.0-1.0)

---

## 🔧 Logic & Architecture

### Backend Flow
```
1. User creates session → POST /sessions
   - Defines: role, addresses, price range, quantity, fairness_weight
   
2. Run negotiation → POST /sessions/{id}/auto
   - Creates BaseAgent instances (buyer + seller)
   - Executes negotiation loop
   - Persists offers to database
   - Generates agreement hash
   
3. Get timeline → GET /sessions/{id}/timeline
   - Returns all offers with fairness/utility scores
   
4. Finalize → POST /sessions/{id}/finalize
   - Returns agreement data for blockchain recording
```

### Smart Contract Logic
- **EquiExchangeRecords.sol**:
  - Stores agreements with hash verification
  - Prevents duplicate recordings
  - Emits events for transparency
  - Immutable once recorded

### Frontend Flow
1. Connect wallet (MetaMask)
2. Create/join negotiation session
3. Run automated negotiation (AI agents)
4. View real-time timeline
5. Record agreement on blockchain
6. Verify on Etherscan

---

## 🚀 Current Limitations & Improvements

### 1. **Theory of Mind Integration** ⭐ (High Priority)

**Current State**: Agents don't model opponent's mental state or intentions.

**Theory of Mind (ToM) Enhancement**:
```python
class TheoryOfMindAgent(BaseAgent):
    def __init__(self, ...):
        super().__init__(...)
        self.opponent_model = {
            'target_price_estimate': None,
            'concession_rate_estimate': None,
            'patience_level': 0.5,
            'fairness_preference': 0.5,
            'risk_aversion': 0.5
        }
        self.belief_history = []
    
    def update_opponent_model(self, opponent_offers):
        """Update beliefs about opponent's strategy"""
        if len(opponent_offers) >= 2:
            # Estimate concession rate
            concessions = [opponent_offers[i] - opponent_offers[i+1] 
                          for i in range(len(opponent_offers)-1)]
            self.opponent_model['concession_rate_estimate'] = np.mean(concessions)
            
            # Estimate target price (extrapolate from trend)
            if len(opponent_offers) >= 3:
                trend = np.polyfit(range(len(opponent_offers)), 
                                  opponent_offers, 1)
                self.opponent_model['target_price_estimate'] = trend[1]
    
    def propose(self, last_offer_price=None):
        """Strategic proposal using opponent model"""
        if last_offer_price:
            # If opponent is conceding fast, be less aggressive
            if self.opponent_model['concession_rate_estimate'] > 0.1:
                # Opponent is eager - hold firm
                return self.target_price
            else:
                # Opponent is stubborn - concede more
                delta = last_offer_price - self.target_price
                return self.target_price + delta * 0.6
        return self.target_price
```

**Benefits**:
- More realistic negotiations
- Better convergence rates
- Adaptive strategies based on opponent behavior
- Can model deception/detection

### 2. **Deep Reinforcement Learning**

**Current**: Simple Q-Learning with tabular representation

**Improvement**: Deep Q-Network (DQN) or Actor-Critic
```python
import torch
import torch.nn as nn

class DQNAgent(nn.Module):
    def __init__(self, state_dim=10, action_dim=20):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )
    
    def forward(self, state):
        return self.network(state)
```

**Benefits**:
- Handle continuous/continuous-like state spaces
- Learn complex strategies
- Transfer learning across sessions

### 3. **Multi-Objective Optimization**

**Current**: Simple fairness = 1 - |utility_diff|

**Improvement**: Pareto-optimal solutions
```python
from scipy.optimize import minimize

def pareto_optimal_price(buyer_agent, seller_agent):
    """Find Pareto-optimal price using multi-objective optimization"""
    def objective(price):
        buyer_util = buyer_agent.utility(price)
        seller_util = seller_agent.utility(price)
        # Minimize negative of both utilities (maximize both)
        return -(buyer_util + seller_util)
    
    result = minimize(objective, x0=50, bounds=[(min_price, max_price)])
    return result.x[0]
```

### 4. **Temporal Dynamics & Learning**

**Current**: Agents don't learn from past negotiations

**Improvement**: Meta-learning across sessions
```python
class MetaLearningAgent(BaseAgent):
    def __init__(self, ...):
        super().__init__(...)
        self.session_history = []
        self.strategy_weights = {}
    
    def learn_from_history(self):
        """Update strategy based on past successful negotiations"""
        successful_sessions = [s for s in self.session_history 
                              if s['fairness'] > 0.8]
        # Update concession rates, target adjustments, etc.
```

### 5. **Game-Theoretic Foundations**

**Current**: Heuristic-based

**Improvement**: Nash equilibrium strategies
```python
from scipy.optimize import differential_evolution

def nash_equilibrium_price(buyer_agent, seller_agent):
    """Find Nash equilibrium using game theory"""
    # Define payoff matrix
    # Solve for mixed strategy equilibrium
    # Return optimal price
```

### 6. **Emotional/Behavioral Modeling**

**Enhancement**: Add emotional states affecting negotiation
```python
class EmotionalAgent(BaseAgent):
    def __init__(self, ...):
        super().__init__(...)
        self.emotional_state = {
            'frustration': 0.0,  # Increases with failed rounds
            'satisfaction': 0.0,  # Increases with good offers
            'trust': 0.5,  # Trust in opponent
            'urgency': 0.0  # Time pressure
        }
    
    def propose(self, last_offer_price=None):
        # Adjust strategy based on emotional state
        if self.emotional_state['frustration'] > 0.7:
            # More aggressive concessions
            return self.target_price + larger_concession
        elif self.emotional_state['trust'] > 0.8:
            # More cooperative
            return fair_midpoint
```

### 7. **Advanced Fairness Metrics**

**Current**: Simple utility difference

**Improvements**:
- **Proportional Fairness**: Maximize log-sum of utilities
- **Max-Min Fairness**: Maximize minimum utility
- **Kalai-Smorodinsky**: Equal relative concessions
- **Shapley Value**: Game-theoretic fairness

### 8. **Contextual Features**

**Enhancement**: Add market context
```python
class ContextualAgent(BaseAgent):
    def __init__(self, ..., market_context=None):
        super().__init__(...)
        self.market_context = {
            'market_price': None,
            'volatility': None,
            'liquidity': None,
            'trend': None  # 'bullish', 'bearish', 'neutral'
        }
    
    def propose(self, last_offer_price=None):
        # Adjust based on market conditions
        if self.market_context['trend'] == 'bullish':
            # Sellers can hold firm
            return higher_price
```

### 9. **Multi-Agent Systems**

**Enhancement**: Multiple buyers/sellers, auctions
```python
class AuctionSystem:
    def __init__(self):
        self.buyers = []
        self.sellers = []
    
    def run_auction(self):
        # English auction, Dutch auction, Vickrey auction
        # Multi-agent negotiation
```

### 10. **Explainability & Transparency**

**Enhancement**: Explain agent decisions
```python
class ExplainableAgent(BaseAgent):
    def propose(self, last_offer_price=None):
        price = super().propose(last_offer_price)
        explanation = {
            'reasoning': f"Proposing {price} because...",
            'factors': {
                'target_price': self.target_price,
                'opponent_last_offer': last_offer_price,
                'fairness_weight': self.fairness_weight,
                'concession_rate': self.concession_rate
            }
        }
        return price, explanation
```

---

## 📊 Performance Metrics to Track

1. **Convergence Rate**: % of negotiations reaching agreement
2. **Average Rounds**: Mean rounds to agreement
3. **Fairness Distribution**: Histogram of final fairness scores
4. **Utility Efficiency**: Sum of buyer + seller utilities
5. **Time to Agreement**: Wall-clock time
6. **Blockchain Success Rate**: % of successful on-chain recordings

---

## 🔬 Research Directions

1. **Federated Learning**: Agents learn from multiple users without sharing raw data
2. **Zero-Knowledge Proofs**: Verify negotiation fairness without revealing strategies
3. **Cross-Chain Support**: Multi-chain agreement recording
4. **Oracle Integration**: Real-world price feeds for market context
5. **NFT Agreements**: Represent agreements as NFTs
6. **DAO Governance**: Community-driven fairness parameter tuning

---

## 🛠️ Implementation Priority

### Phase 1 (Quick Wins)
1. ✅ Theory of Mind basic implementation
2. ✅ Enhanced fairness metrics
3. ✅ Explainability layer

### Phase 2 (Medium Term)
4. Deep RL integration
5. Multi-objective optimization
6. Emotional modeling

### Phase 3 (Advanced)
7. Game-theoretic foundations
8. Multi-agent systems
9. Federated learning

---

## 📚 References & Inspiration

- **Theory of Mind in AI**: Premack & Woodruff (1978), Rabinowitz et al. (2018)
- **Multi-Agent Negotiation**: Rosenschein & Zlotkin (1994)
- **Fairness in ML**: Barocas et al. (2019)
- **Reinforcement Learning**: Sutton & Barto (2018)
- **Game Theory**: Osborne & Rubinstein (1994)

---

**Built with**: FastAPI, Next.js, Solidity, NumPy, SQLModel, Web3.py, RainbowKit

