from eth_utils import keccak, to_bytes
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Explicitly define GEMINI_API_KEY if needed
GEMINI_API_KEY = "AIzaSyAiLm3mB3aMx2iG7OXiedk4mxIdmrMwAQg"

def agreement_hash(buyer: str, seller: str, price: int, qty: int, delivery_days: int=0, escrow: bool=True) -> str:
    # canonical string -> hash
    s = f"{buyer.lower()}|{seller.lower()}|{price}|{qty}|{delivery_days}|{1 if escrow else 0}"
    h = keccak(text=s)
    return "0x" + h.hex()

def sigmoid(x: float) -> float:
    """
    Sigmoid activation function: 1 / (1 + exp(-x))
    Used for risk scoring in UCNA
    """
    # Clip to prevent overflow
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))
