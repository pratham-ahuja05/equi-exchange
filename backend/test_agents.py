from app.agents import AdaptiveAgent, run_negotiation_loop
import numpy as np

# Define actions and state space size
actions = [10, 105, 110, 1, 120]  # Example offer prices
state_space_size = 10

# Instantiate buyer and seller as AdaptiveAgents
buyer = AdaptiveAgent("buyer1", actions, state_space_size)
seller = AdaptiveAgent("seller1", actions, state_space_size)

# Run negotiation loop
timeline, result = run_negotiation_loop(buyer, seller, max_rounds=5)

print("Negotiation Timeline:")
for round_info in timeline:
    print(round_info)
print("Final Result:", result)