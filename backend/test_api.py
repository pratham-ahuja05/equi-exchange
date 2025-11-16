#!/usr/bin/env python3

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing EquiExchange API...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test session creation
    session_data = {
        "role": "buyer",
        "buyer_address": "0x1234567890123456789012345678901234567890",
        "seller_address": "0x0987654321098765432109876543210987654321",
        "target_price": 85,
        "min_price": 50,
        "max_price": 100,
        "quantity": 60,
        "fairness_weight": 0.5,
        "max_rounds": 8,
        "concession_rate": 0.05,
        "aggressiveness": 0.5
    }
    
    try:
        response = requests.post(f"{base_url}/sessions", json=session_data)
        print(f"Session creation: {response.status_code}")
        if response.status_code == 200:
            session_result = response.json()
            session_id = session_result["session_id"]
            print(f"Created session ID: {session_id}")
            
            # Test auto negotiation
            response = requests.post(f"{base_url}/sessions/{session_id}/auto")
            print(f"Auto negotiation: {response.status_code}")
            if response.status_code == 200:
                negotiation_result = response.json()
                print(f"Negotiation completed with {len(negotiation_result['timeline'])} rounds")
                print(f"Final agreement: ${negotiation_result['agreement']['price']:.2f}")
                print(f"Fairness: {negotiation_result['agreement']['fairness']:.1%}")
                
                # Test timeline retrieval
                response = requests.get(f"{base_url}/sessions/{session_id}/timeline")
                print(f"Timeline retrieval: {response.status_code}")
                
                # Test finalization
                response = requests.post(f"{base_url}/sessions/{session_id}/finalize")
                print(f"Agreement finalization: {response.status_code}")
                if response.status_code == 200:
                    finalized = response.json()
                    print(f"Agreement hash: {finalized['agreement_hash']}")
                
                return True
            else:
                print(f"Auto negotiation failed: {response.text}")
        else:
            print(f"Session creation failed: {response.text}")
    except Exception as e:
        print(f"API test failed: {e}")
    
    return False

if __name__ == "__main__":
    test_api()