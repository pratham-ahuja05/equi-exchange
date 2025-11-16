"""
Explainability Layer - Generates human-readable explanations for agent decisions
"""

from typing import Optional, Dict


def explain_offer(
    agent_type: str,  # 'buyer' or 'seller'
    price: float,
    last_opponent_offer: Optional[float],
    target_price: float,
    concession_rate: float,
    aggressiveness: float,
    fairness: float,
    market_price: Optional[float] = None,
    tom_insights: Optional[Dict] = None
) -> str:
    """
    Generate 1-2 sentence explanation for an offer
    
    Args:
        agent_type: 'buyer' or 'seller'
        price: Current offer price
        last_opponent_offer: Opponent's last offer (None if first round)
        target_price: Agent's target price
        concession_rate: How much agent is conceding
        aggressiveness: Agent's aggressiveness level (0-1)
        fairness: Current fairness score
        market_price: Market price if available
        tom_insights: Theory of Mind insights dict
    """
    
    if last_opponent_offer is None:
        # First offer
        if market_price and abs(price - market_price) < abs(target_price - market_price):
            return f"Starting at ${price:.2f}, adjusted toward market price of ${market_price:.2f}."
        return f"Opening offer at ${price:.2f}, my target price."
    
    # Calculate movement
    if agent_type == 'buyer':
        movement = last_opponent_offer - price  # Positive if moving down
        direction = "down" if movement > 0 else "up"
    else:  # seller
        movement = price - last_opponent_offer  # Positive if moving up
        direction = "up" if movement > 0 else "down"
    
    # Theory of Mind explanations
    if tom_insights:
        strategy = tom_insights.get('strategy_type')
        if strategy == 'stubborn':
            return f"Opponent is being stubborn (conceding slowly), so I'm holding firm at ${price:.2f}."
        elif strategy == 'cooperative':
            return f"Opponent is cooperative, so I'm making a fair concession to ${price:.2f}."
    
    # Aggressiveness-based explanations
    if aggressiveness > 0.7:
        if agent_type == 'buyer':
            return f"Aggressively pushing price down to ${price:.2f} to maximize my advantage."
        else:
            return f"Aggressively pushing price up to ${price:.2f} to maximize my advantage."
    elif aggressiveness < 0.3:
        if agent_type == 'buyer':
            return f"Making a generous concession to ${price:.2f} to improve cooperation."
        else:
            return f"Making a generous concession to ${price:.2f} to improve cooperation."
    
    # Fairness-based explanations
    if fairness < 0.5:
        return f"Conceded to ${price:.2f} to improve fairness (current: {fairness:.1%})."
    elif fairness > 0.8:
        return f"Maintaining strong position at ${price:.2f} with high fairness ({fairness:.1%})."
    
    # Market-based explanations
    if market_price:
        if agent_type == 'buyer' and price < market_price:
            return f"Offering ${price:.2f}, below market price of ${market_price:.2f}, to secure a good deal."
        elif agent_type == 'seller' and price > market_price:
            return f"Offering ${price:.2f}, above market price of ${market_price:.2f}, capitalizing on market conditions."
    
    # Default concession explanation
    if abs(movement) > 0.01:
        pct_change = abs(movement) / max(abs(last_opponent_offer), 1) * 100
        return f"Conceded {pct_change:.1f}% to ${price:.2f} to move toward agreement."
    
    return f"Proposing ${price:.2f} to balance my target and opponent's position."

