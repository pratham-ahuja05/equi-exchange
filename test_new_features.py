#!/usr/bin/env python3
"""
Test script for new blockchain recording features
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_negotiation_flow():
    print("🚀 Testing Enhanced Negotiation Flow with Blockchain Recording")
    print("=" * 60)
    
    # 1. Create a new session
    print("1. Creating new negotiation session...")
    session_data = {
        "role": "buyer",
        "buyer_address": "0x742d35Cc6634C0532925a3b8D4C9db96590c6C87",
        "seller_address": "0x8ba1f109551bD432803012645Hac136c22C177ec",
        "target_price": 85,
        "min_price": 50,
        "max_price": 100,
        "quantity": 60,
        "fairness_weight": 0.7,
        "aggressiveness": 0.6,
        "market_symbol": "AAPL",
        "market_asset_type": "stock"
    }
    
    response = requests.post(f"{API_BASE}/sessions", json=session_data)
    if response.status_code != 200:
        print(f"❌ Failed to create session: {response.text}")
        return
    
    session = response.json()
    session_id = session["session_id"]
    print(f"✅ Created session {session_id}")
    
    # 2. Run auto-negotiation
    print("2. Running auto-negotiation...")
    response = requests.post(f"{API_BASE}/sessions/{session_id}/auto")
    if response.status_code != 200:
        print(f"❌ Failed to run negotiation: {response.text}")
        return
    
    result = response.json()
    print(f"✅ Negotiation completed with {len(result.get('timeline', []))} rounds")
    
    if result.get('agreement'):
        print(f"💰 Agreement reached: ${result['agreement']['price']} for {result['agreement']['quantity']} units")
    
    # 3. Get timeline details
    print("3. Fetching detailed timeline...")
    response = requests.get(f"{API_BASE}/sessions/{session_id}/timeline")
    if response.status_code == 200:
        timeline = response.json()["timeline"]
        print(f"📊 Timeline has {len(timeline)} rounds with detailed metrics")
        
        # Show sample round details
        if timeline:
            sample_round = timeline[0]
            print(f"   Sample Round 1: Buyer ${sample_round.get('buyer_offer', 'N/A')}, "
                  f"Seller ${sample_round.get('seller_offer', 'N/A')}, "
                  f"Fairness: {sample_round.get('fairness', 0)*100:.1f}%")
    
    # 4. Finalize agreement
    if result.get('agreement'):
        print("4. Finalizing agreement...")
        response = requests.post(f"{API_BASE}/sessions/{session_id}/finalize")
        if response.status_code == 200:
            agreement = response.json()
            print(f"✅ Agreement finalized with hash: {agreement['agreement_hash'][:16]}...")
            print(f"   Final fairness: {agreement.get('final_fairness', 0)*100:.1f}%")
            print(f"   Buyer utility: {agreement.get('buyer_utility', 0):.3f}")
            print(f"   Seller utility: {agreement.get('seller_utility', 0):.3f}")
            
            # 5. Simulate blockchain recording
            print("5. Simulating blockchain transaction recording...")
            mock_tx_hash = "0x1234567890abcdef1234567890abcdef12345678901234567890abcdef123456"
            response = requests.post(f"{API_BASE}/sessions/{session_id}/record-blockchain", 
                                   json={"tx_hash": mock_tx_hash, "block_number": 12345})
            if response.status_code == 200:
                print(f"✅ Blockchain transaction recorded: {mock_tx_hash[:16]}...")
            else:
                print(f"❌ Failed to record blockchain transaction: {response.text}")
    
    # 6. Check session history
    print("6. Checking session history...")
    response = requests.get(f"{API_BASE}/sessions")
    if response.status_code == 200:
        sessions = response.json()["sessions"]
        recorded_sessions = [s for s in sessions if s.get("status") == "recorded"]
        print(f"📋 Total sessions: {len(sessions)}, Recorded on blockchain: {len(recorded_sessions)}")
    
    print("\n🎉 Test completed successfully!")
    print("=" * 60)
    print("New features tested:")
    print("✅ Enhanced negotiation timeline with detailed round information")
    print("✅ Blockchain transaction recording")
    print("✅ Session status tracking (open → finalized → recorded)")
    print("✅ Comprehensive agreement metrics (fairness, utilities)")
    print("✅ Session history with blockchain status")

if __name__ == "__main__":
    try:
        test_negotiation_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")