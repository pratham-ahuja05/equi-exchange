# EquiExchange - Quick Summary

## What It Does
**Automated price negotiation platform** where AI agents (buyer & seller) negotiate prices, optimize for fairness, and record agreements on Ethereum blockchain.

## Core Models

### 1. **BaseAgent** (Current Primary)
- **Type**: Heuristic-based
- **Strategy**: 50% concession toward opponent's offer
- **Utility**: Distance from target price
- **Fairness**: 1 - |buyer_util - seller_util|

### 2. **AdaptiveAgent** (Q-Learning)
- **Type**: Reinforcement Learning
- **Method**: Q-table with ε-greedy exploration
- **Reward**: Fairness score
- **Learning**: Updates Q-values after each round

### 3. **TheoryOfMindAgent** (NEW - Recommended)
- **Type**: Cognitive modeling
- **Features**:
  - Models opponent's target price, strategy, patience
  - Adapts based on opponent behavior
  - First-order: "What does opponent want?"
  - Second-order: "What does opponent think I want?"

## Key Logic Flow

```
1. Create Session → Define price ranges, addresses
2. Run Negotiation → Agents propose back-and-forth
3. Calculate Fairness → Balance buyer/seller utilities
4. Converge or Timeout → Agreement or max rounds
5. Record on Blockchain → Immutable Ethereum storage
```

## Improvements Priority

### 🔴 High Priority
1. **Theory of Mind** - Already implemented in `theory_of_mind_agent.py`
2. **Better Fairness Metrics** - Proportional, max-min, Kalai-Smorodinsky
3. **Explainability** - Show why agents make decisions

### 🟡 Medium Priority
4. **Deep RL** - Replace Q-table with neural networks
5. **Multi-Objective Optimization** - Pareto-optimal solutions
6. **Emotional Modeling** - Frustration, trust, urgency

### 🟢 Advanced
7. **Game Theory** - Nash equilibrium strategies
8. **Multi-Agent Systems** - Auctions, multiple buyers/sellers
9. **Federated Learning** - Learn from multiple users

## Files Structure

```
backend/app/
├── agents.py              # BaseAgent, AdaptiveAgent
├── theory_of_mind_agent.py # NEW: ToM implementation
├── routes.py              # API endpoints
├── models.py              # Database models
└── utils.py               # Agreement hashing

contracts/
└── EquiExchangeRecords.sol # Blockchain storage

frontend/
└── components/
    └── NegotiationFlow.tsx # UI for negotiations
```

## Next Steps

1. **Integrate ToM Agent**: Replace BaseAgent with TheoryOfMindAgent in routes.py
2. **Add Explainability**: Show opponent model insights in frontend
3. **Test & Compare**: Run both agents, compare convergence rates
4. **Enhance Fairness**: Implement advanced fairness metrics

