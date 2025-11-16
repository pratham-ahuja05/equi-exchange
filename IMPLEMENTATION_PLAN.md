# EquiExchange - Implementation Plan & Confirmation

## 📋 Current State Analysis

### ✅ Already Implemented
- Basic negotiation engine (BaseAgent)
- Simple fairness metric
- Database models (Session, Offer, Agreement)
- Basic API endpoints
- Frontend negotiation flow
- Smart contract structure
- Wallet integration setup

### ❌ Needs Implementation
All 10 features listed below

---

## 🎯 Implementation Plan for 10 Features

### **Feature 1: Enhanced Automated Negotiation Engine**
**Status**: Partially exists, needs enhancement

**Changes Required**:
- ✅ Add Proportional Fairness: `log(buyer_util) + log(seller_util)`
- ✅ Keep Simple Fairness: `1 - abs(buyer_util - seller_util)`
- ✅ Return both metrics in timeline
- ✅ Store full timeline in database (already done)
- ✅ Ensure 6-8 round negotiation (configurable)

**Files to Modify**:
- `backend/app/agents.py` - Add proportional fairness calculation
- `backend/app/routes.py` - Return both fairness metrics
- `backend/app/models.py` - Add fairness_type field (optional)

---

### **Feature 2: Theory-of-Mind Opponent Modeling**
**Status**: Code exists in `theory_of_mind_agent.py`, needs integration

**Changes Required**:
- ✅ Integrate TheoryOfMindAgent into routes
- ✅ Estimate opponent concession rate
- ✅ Estimate opponent target price from trend
- ✅ Store ToM estimates in session/offer data
- ✅ Return ToM insights in API responses

**Files to Modify**:
- `backend/app/routes.py` - Use TheoryOfMindAgent instead of BaseAgent
- `backend/app/models.py` - Add ToM fields to Offer model
- `backend/app/theory_of_mind_agent.py` - Already created, verify it works

---

### **Feature 3: Explainability Layer**
**Status**: New feature

**Changes Required**:
- ✅ Add `explanation` field to each offer
- ✅ Generate 1-2 sentence reasoning for each move
- ✅ Examples:
  - "Opponent conceding slowly, so I held firm."
  - "Conceded 5% to improve fairness."
  - "Adjusted toward market price to increase cooperation."

**Files to Create/Modify**:
- `backend/app/explainer.py` - New file for explanation generation
- `backend/app/agents.py` - Add explanation generation to propose()
- `backend/app/models.py` - Add explanation field to Offer
- `frontend/components/NegotiationFlow.tsx` - Display explanations

---

### **Feature 4: User-Configurable Parameters**
**Status**: Partially exists, needs frontend exposure

**Changes Required**:
- ✅ Expose from frontend:
  - `max_rounds` (6-20, default 8)
  - `concession_rate` (0.01-0.2, default 0.05)
  - `fairness_weight` (0-1, default 0.5)
  - `aggressiveness` (0-1, default 0.5) - NEW
- ✅ Agents incorporate these into strategies
- ✅ Store in session model

**Files to Modify**:
- `backend/app/models.py` - Add aggressiveness field
- `backend/app/agents.py` - Use aggressiveness in propose()
- `frontend/components/NegotiationForm.tsx` - Add parameter inputs
- `frontend/lib/api.ts` - Include parameters in session creation

---

### **Feature 5: Smart Contract Integration (Testnet)**
**Status**: Contract exists, needs testnet deployment

**Changes Required**:
- ✅ Deploy to Sepolia testnet
- ✅ Update frontend with contract address
- ✅ Add transaction status tracking
- ✅ Show transaction hash + Etherscan link
- ✅ Prevent duplicate submissions (already in contract)

**Files to Modify**:
- `contracts/scripts/deploy.js` - Testnet deployment
- `frontend/lib/contract.ts` - Update contract address
- `frontend/components/AgreementDisplay.tsx` - Show transaction status
- `frontend/env.example` - Add testnet RPC URL

---

### **Feature 6: Real-Time Negotiation Timeline**
**Status**: Exists but needs enhancement

**Changes Required**:
- ✅ Display all required fields:
  - Round number ✅
  - Buyer offer ✅
  - Seller offer ✅
  - Buyer utility ✅
  - Seller utility ✅
  - Fairness value ✅
  - Explanation text (NEW)
- ✅ Update immediately after auto-negotiation
- ✅ Show both fairness metrics

**Files to Modify**:
- `frontend/components/NegotiationFlow.tsx` - Enhance timeline display
- `backend/app/routes.py` - Include explanations in timeline

---

### **Feature 7: Multi-Session History**
**Status**: New feature

**Changes Required**:
- ✅ Backend: Store session history
- ✅ API endpoint: `GET /sessions` - List all sessions
- ✅ Frontend: Session history page/component
- ✅ View full timeline for any past session
- ✅ Filter by status, date, fairness

**Files to Create/Modify**:
- `backend/app/routes.py` - Add GET /sessions endpoint
- `frontend/components/SessionHistory.tsx` - New component
- `frontend/app/page.tsx` - Add history view
- `frontend/lib/api.ts` - Add getSessions() function

---

### **Feature 8: Market Context Module**
**Status**: New feature

**Changes Required**:
- ✅ Backend: MarketDataService
- ✅ API endpoint: `GET /market-price?symbol=XYZ&asset_type=stock|crypto|forex`
- ✅ Integrate free API (AlphaVantage/TwelveData/Finnhub/FMP)
- ✅ Cache results within session
- ✅ Inject market_price into negotiation context
- ✅ Agent behavior adjustment:
  - Price trending up → sellers hold firm
  - Price trending down → buyers hold firm
- ✅ Frontend: Market symbol input, display market context

**Files to Create/Modify**:
- `backend/app/market_service.py` - New file
- `backend/app/routes.py` - Add /market-price endpoint
- `backend/app/agents.py` - Use market context in propose()
- `frontend/components/NegotiationForm.tsx` - Add market inputs
- `frontend/components/NegotiationFlow.tsx` - Display market context
- `backend/requirements.txt` - Add API client library

---

### **Feature 9: Manual Gemini API Chatbot**
**Status**: New feature

**Changes Required**:
- ✅ Backend endpoint: `POST /chat/manual`
- ✅ Input: `{session_id, user_message}`
- ✅ Use Gemini API (GEMINI_API_KEY)
- ✅ Return analysis/suggestions
- ✅ Frontend: Toggle for "Manual Chat / Override Mode"
- ✅ Side chat panel
- ✅ User can ask questions, get suggestions
- ✅ Chat does NOT auto-alter negotiation
- ✅ User manually applies suggestions

**Files to Create/Modify**:
- `backend/app/chat_service.py` - New file for Gemini integration
- `backend/app/routes.py` - Add /chat/manual endpoint
- `frontend/components/ChatPanel.tsx` - New component
- `frontend/components/NegotiationFlow.tsx` - Add chat toggle
- `backend/requirements.txt` - Add google-generativeai
- `frontend/lib/api.ts` - Add chatManual() function

---

### **Feature 10: Final Deliverables Checklist**
**Status**: Summary

**All Features Combined**:
- ✅ Fully working automated negotiation engine
- ✅ Improved agent intelligence via ToM
- ✅ Explainable decision reasoning
- ✅ Real-time market price integration
- ✅ Manual Gemini chatbot override system
- ✅ Blockchain recording of agreements
- ✅ Timeline visualization
- ✅ Multi-session history
- ✅ Adjustable negotiation parameters

---

## 📦 New Dependencies Required

### Backend (`requirements.txt`)
```
google-generativeai>=0.3.0  # For Gemini API
requests>=2.32.5  # Already exists, for market APIs
python-dotenv>=1.1.1  # Already exists
```

### Frontend (`package.json`)
No new dependencies needed (already has axios, wagmi, etc.)

---

## 🔧 Environment Variables Needed

### Backend (`.env`)
```
DATABASE_URL=sqlite:///./data.db
GEMINI_API_KEY=your_gemini_api_key_here
MARKET_API_KEY=your_market_api_key_here  # AlphaVantage/TwelveData/etc.
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=0x...  # Sepolia testnet address
NEXT_PUBLIC_SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/...
```

---

## 📁 Files to Create

1. `backend/app/explainer.py` - Explanation generation
2. `backend/app/market_service.py` - Market data fetching
3. `backend/app/chat_service.py` - Gemini chatbot integration
4. `frontend/components/SessionHistory.tsx` - Session history view
5. `frontend/components/ChatPanel.tsx` - Chat interface
6. `frontend/components/MarketContext.tsx` - Market display component

## 📝 Files to Modify

1. `backend/app/agents.py` - Add proportional fairness, aggressiveness, explanations
2. `backend/app/routes.py` - Add new endpoints, integrate ToM, market, chat
3. `backend/app/models.py` - Add new fields (explanation, aggressiveness, ToM data)
4. `backend/app/theory_of_mind_agent.py` - Verify and integrate
5. `frontend/components/NegotiationFlow.tsx` - Enhance timeline, add chat
6. `frontend/components/NegotiationForm.tsx` - Add parameters, market inputs
7. `frontend/lib/api.ts` - Add new API functions
8. `frontend/app/page.tsx` - Add session history view
9. `contracts/scripts/deploy.js` - Testnet deployment

---

## ⚠️ Important Notes

1. **API Keys**: User will need to obtain:
   - Gemini API key from Google AI Studio
   - Market API key (AlphaVantage free tier or similar)

2. **Testnet Deployment**: Requires:
   - Sepolia testnet ETH for gas
   - Hardhat configuration for testnet
   - Contract verification on Etherscan

3. **Database Migration**: Adding new fields may require:
   - Database migration or recreation
   - Backward compatibility handling

4. **Error Handling**: All new features need:
   - Proper error handling
   - User-friendly error messages
   - Fallback behaviors

---

## ✅ Confirmation Checklist

Before proceeding, please confirm:

- [ ] You have Gemini API key ready (or want me to add placeholder)
- [ ] You have Market API key ready (or want me to use free tier)
- [ ] You want testnet deployment (Sepolia) or local Hardhat node
- [ ] You're okay with database changes (may need to recreate)
- [ ] You want all features implemented or prioritize some first

**Ready to proceed?** Reply "CONFIRM" and I'll start implementation!

