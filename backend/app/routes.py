from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select, create_engine
from .models import Session as SessionModel, Offer, Agreement, SQLModel
from .agents import BaseAgent, run_negotiation_loop
from .utils import agreement_hash
from .market_service import market_service
import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Create router instance (VERY IMPORTANT)
router = APIRouter()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

@router.get("/")
def health_check():
    return {"status": "OK", "message": "Routes are working!"}


@router.post("/sessions")
def create_session(payload: Dict):
    try:
        with Session(engine) as db:
            # Auto-generate seller address if not provided
            role = payload.get("role", "buyer")
            buyer_addr = payload.get("buyer_address")
            seller_addr = payload.get("seller_address")
            
            # If no seller address provided, generate a dummy one
            if not seller_addr:
                seller_addr = "0x" + "1" * 40  # Dummy seller address
            
            s = SessionModel(
                role=role,
                buyer_address=buyer_addr,
                seller_address=seller_addr,
                target_price=payload.get("target_price"),
                min_price=payload.get("min_price"),
                max_price=payload.get("max_price"),
                quantity=payload.get("quantity"),
                fairness_weight=payload.get("fairness_weight", 0.5),
                max_rounds=payload.get("max_rounds", 8),
                concession_rate=payload.get("concession_rate", 0.05),
                aggressiveness=payload.get("aggressiveness", 0.5),
                market_symbol=payload.get("market_symbol"),
                market_asset_type=payload.get("market_asset_type"),
                status="open"
            )
            db.add(s)
            db.commit()
            db.refresh(s)
            return {"session_id": s.id, "session": s}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/auto")
def run_auto(session_id: int):
    with Session(engine) as db:
        s = db.get(SessionModel, session_id)
        if not s:
            raise HTTPException(status_code=404, detail="Session not found")

        # Fetch market price if symbol provided
        market_price = None
        if s.market_symbol and s.market_asset_type:
            try:
                market_data = market_service.get_market_price(s.market_symbol, s.market_asset_type)
                market_price = market_data.get("price")
                # Update session with fetched market price
                s.market_price = market_price
                db.commit()
            except Exception as e:
                print(f"Failed to fetch market price: {e}")

        # Create agents based on session role
        if s.role == 'buyer':
            # User is buyer, so use their params for buyer agent
            buyer_agent = BaseAgent(
                s.buyer_address or "0x0000000000000000000000000000000000000000", 
                s.target_price, s.min_price, s.max_price,
                s.quantity, fairness_weight=s.fairness_weight,
                concession_rate=s.concession_rate, aggressiveness=s.aggressiveness,
                market_price=market_price
            )
            # AI seller wants higher prices - target closer to max_price
            seller_target = s.min_price + (s.max_price - s.min_price) * 0.8  # 80% toward max
            seller_agent = BaseAgent(
                s.seller_address or "0x1111111111111111111111111111111111111111", 
                seller_target, s.min_price, s.max_price,
                s.quantity, fairness_weight=s.fairness_weight,
                concession_rate=s.concession_rate, aggressiveness=s.aggressiveness,
                market_price=market_price
            )
        else:  # s.role == 'seller'
            # User is seller, so use their params for seller agent
            seller_agent = BaseAgent(
                s.seller_address or "0x1111111111111111111111111111111111111111", 
                s.target_price, s.min_price, s.max_price,
                s.quantity, fairness_weight=s.fairness_weight,
                concession_rate=s.concession_rate, aggressiveness=s.aggressiveness,
                market_price=market_price
            )
            # AI buyer wants lower prices - target closer to min_price
            buyer_target = s.min_price + (s.max_price - s.min_price) * 0.2  # 20% toward max (closer to min)
            buyer_agent = BaseAgent(
                s.buyer_address or "0x0000000000000000000000000000000000000000", 
                buyer_target, s.min_price, s.max_price,
                s.quantity, fairness_weight=s.fairness_weight,
                concession_rate=s.concession_rate, aggressiveness=s.aggressiveness,
                market_price=market_price
            )

        timeline, agreement = run_negotiation_loop(buyer_agent, seller_agent, max_rounds=s.max_rounds)

        # Store offers in database
        for round_data in timeline:
            # Store buyer offer
            buyer_offer = Offer(
                session_id=session_id,
                round=round_data["round"],
                made_by="buyer",
                price=round_data["buyer_offer"],
                quantity=s.quantity,
                fairness=round_data["fairness"],
                proportional_fairness=round_data.get("proportional_fairness"),
                utility=round_data["buyer_util"],
                explanation=round_data.get("buyer_explanation"),
                tom_insights=round_data.get("buyer_tom_insights"),
                payload=json.dumps(round_data)
            )
            db.add(buyer_offer)
            
            # Store seller offer
            seller_offer = Offer(
                session_id=session_id,
                round=round_data["round"],
                made_by="seller",
                price=round_data["seller_offer"],
                quantity=s.quantity,
                fairness=round_data["fairness"],
                proportional_fairness=round_data.get("proportional_fairness"),
                utility=round_data["seller_util"],
                explanation=round_data.get("seller_explanation"),
                tom_insights=round_data.get("seller_tom_insights"),
                payload=json.dumps(round_data)
            )
            db.add(seller_offer)
        
        db.commit()
        return {
            "timeline": timeline, 
            "agreement": agreement,
            "market_price": market_price,
            "market_symbol": s.market_symbol,
            "market_asset_type": s.market_asset_type
        }





@router.get("/sessions/{session_id}/timeline")
def get_timeline(session_id: int):
    """Get negotiation timeline for a session"""
    try:
        with Session(engine) as db:
            offers = db.exec(
                select(Offer)
                .where(Offer.session_id == session_id)
                .order_by(Offer.round)
            ).all()
            
            # Group offers by round
            rounds_data = {}
            for offer in offers:
                round_num = offer.round
                if round_num not in rounds_data:
                    rounds_data[round_num] = {
                        "round": round_num,
                        "buyer_offer": None,
                        "seller_offer": None,
                        "buyer_util": None,
                        "seller_util": None,
                        "fairness": offer.fairness,
                        "proportional_fairness": offer.proportional_fairness,
                        "buyer_explanation": None,
                        "seller_explanation": None
                    }
                
                if offer.made_by == "buyer":
                    rounds_data[round_num]["buyer_offer"] = offer.price
                    rounds_data[round_num]["buyer_util"] = offer.utility
                    rounds_data[round_num]["buyer_explanation"] = offer.explanation
                else:
                    rounds_data[round_num]["seller_offer"] = offer.price
                    rounds_data[round_num]["seller_util"] = offer.utility
                    rounds_data[round_num]["seller_explanation"] = offer.explanation
            
            timeline = list(rounds_data.values())
            
            # Get session for market price info
            session = db.get(SessionModel, session_id)
            return {
                "timeline": timeline,
                "market_price": session.market_price if session else None,
                "market_symbol": session.market_symbol if session else None,
                "market_asset_type": session.market_asset_type if session else None
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/finalize")
def finalize_agreement(session_id: int):
    """Finalize agreement for a session"""
    try:
        with Session(engine) as db:
            session = db.get(SessionModel, session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Get the latest offers to determine final price
            latest_offers = db.exec(
                select(Offer)
                .where(Offer.session_id == session_id)
                .order_by(Offer.round.desc())
                .limit(2)
            ).all()
            
            if not latest_offers:
                raise HTTPException(status_code=400, detail="No offers found")
            
            # Calculate final price (average of last offers)
            if len(latest_offers) >= 2:
                final_price = (latest_offers[0].price + latest_offers[1].price) / 2
            else:
                final_price = latest_offers[0].price
            
            # Create agreement hash
            hash_value = agreement_hash(
                session.buyer_address or "0x0000000000000000000000000000000000000000",
                session.seller_address or "0x0000000000000000000000000000000000000000",
                int(final_price),
                session.quantity or 1
            )
            
            # Calculate final fairness and utilities from last round
            final_fairness = None
            final_proportional_fairness = None
            buyer_utility = None
            seller_utility = None
            
            if latest_offers:
                # Get fairness from the last offer
                final_fairness = latest_offers[0].fairness
                final_proportional_fairness = latest_offers[0].proportional_fairness
                
                # Get utilities from both agents
                for offer in latest_offers:
                    if offer.made_by == "buyer":
                        buyer_utility = offer.utility
                    else:
                        seller_utility = offer.utility
            
            agreement = Agreement(
                session_id=session_id,
                price=final_price,
                quantity=session.quantity,
                agreement_hash=hash_value,
                final_fairness=final_fairness,
                final_proportional_fairness=final_proportional_fairness,
                buyer_utility=buyer_utility,
                seller_utility=seller_utility
            )
            
            db.add(agreement)
            session.status = "finalized"
            db.commit()
            db.refresh(agreement)
            
            return {
                "agreement_hash": hash_value,
                "price": final_price,
                "quantity": session.quantity,
                "buyer_address": session.buyer_address,
                "seller_address": session.seller_address,
                "final_fairness": final_fairness,
                "final_proportional_fairness": final_proportional_fairness,
                "buyer_utility": buyer_utility,
                "seller_utility": seller_utility
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions")
def get_sessions(status: Optional[str] = Query(None)):
    """Get all sessions, optionally filtered by status"""
    try:
        with Session(engine) as db:
            query = select(SessionModel)
            if status:
                query = query.where(SessionModel.status == status)
            
            sessions = db.exec(query).all()
            return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-price")
def get_market_price(symbol: str = Query(...), asset_type: str = Query("stock")):
    """Get market price for a symbol"""
    try:
        price_data = market_service.get_market_price(symbol, asset_type)
        return price_data
    except Exception as e:
        # Return a fallback response if market service fails
        return {
            "symbol": symbol,
            "asset_type": asset_type,
            "price": 100.0,  # Default price
            "source": "fallback",
            "timestamp": "2024-01-01T00:00:00",
            "error": str(e)
        }


@router.post("/sessions/{session_id}/record-blockchain")
def record_blockchain_transaction(session_id: int, payload: Dict):
    """Record blockchain transaction hash for a session"""
    tx_hash = payload.get("tx_hash")
    block_number = payload.get("block_number")
    
    if not tx_hash:
        raise HTTPException(status_code=400, detail="tx_hash required")
    
    try:
        with Session(engine) as db:
            session = db.get(SessionModel, session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Update session with blockchain info
            session.blockchain_tx_hash = tx_hash
            session.blockchain_block_number = block_number
            session.status = "recorded"
            
            db.commit()
            
            return {
                "message": "Blockchain transaction recorded",
                "tx_hash": tx_hash,
                "block_number": block_number
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
