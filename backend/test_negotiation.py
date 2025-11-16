#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.agents import BaseAgent, run_negotiation_loop

def test_negotiation():
    print("Testing negotiation system...")
    
    # Create buyer and seller agents
    buyer_agent = BaseAgent(
        address="0x1234567890123456789012345678901234567890",
        target_price=85,
        min_price=50,
        max_price=100,
        quantity=60,
        fairness_weight=0.5,
        concession_rate=0.05,
        aggressiveness=0.5
    )
    
    seller_agent = BaseAgent(
        address="0x0987654321098765432109876543210987654321",
        target_price=95,
        min_price=50,
        max_price=100,
        quantity=60,
        fairness_weight=0.5,
        concession_rate=0.05,
        aggressiveness=0.5
    )
    
    print(f"Buyer target: ${buyer_agent.target_price}")
    print(f"Seller target: ${seller_agent.target_price}")
    
    # Run negotiation
    timeline, agreement = run_negotiation_loop(buyer_agent, seller_agent, max_rounds=8)
    
    print(f"\nNegotiation completed in {len(timeline)} rounds")
    print(f"Final agreement: ${agreement['price']:.2f}")
    print(f"Fairness: {agreement['fairness']:.1%}")
    print(f"Buyer utility: {agreement['buyer_utility']:.2f}")
    print(f"Seller utility: {agreement['seller_utility']:.2f}")
    
    print("\nTimeline:")
    for round_data in timeline:
        print(f"Round {round_data['round']}: Buyer ${round_data['buyer_offer']:.2f} <-> Seller ${round_data['seller_offer']:.2f} (Fairness: {round_data['fairness']:.1%})")
    
    return True

if __name__ == "__main__":
    test_negotiation()