from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import EffectOut
from sqlalchemy import create_engine, text
import os
from auth import router as auth_router
from match import router as match_router
from profile import router as profile_router
from card import router as card_router



app = FastAPI()
router = APIRouter()
app.include_router(auth_router)
app.include_router(match_router)
app.include_router(card_router)
app.include_router(profile_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "world ver 4566"}#更新数


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


@router.get("/effect")
def get_effect_all(db: Session = Depends(get_db)):
    effects = db.query(models.Effect).all()
    return effects

@router.get("/effect.effect")
def get_effect_effect(db: Session = Depends(get_db)):
    effects = db.query(models.Effect).order_by(models.Card.card_id).all()
    return [effect.effect for effect in effects]  

@router.get("/effect.effect/filter")
def get_effect_effect_filter(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(models.Effect).filter(models.Effect.effect_id == effect_id).first()
    if not effect:
        return "該当する効果が見つかりません"
    return effect.effect

@router.get("/effect/bycards")
def get_effects_by_cards(db: Session = Depends(get_db)):
    cards = (
        db.query(models.Card)
        .join(models.Effect, models.Card.effect_id == models.Effect.effect_id)
        .order_by(models.Card.card_id)
        .all()
    )
    return [card.effect.effect for card in cards]




@router.get("/card")
def get_card_all(db: Session = Depends(get_db)):
    cards = db.query(models.Card).all()
    return cards

@router.get("/card.name")
def get_card_name(db: Session = Depends(get_db)):
    cards = db.query(models.Card).order_by(models.Card.card_id).all()
    return [card.name for card in cards]  

@router.get("/card.name/filter")
def get_card_name_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.name

@router.get("/card.cost")
def get_card_cost(db: Session = Depends(get_db)):
    cards = db.query(models.Card).order_by(models.Card.card_id).all()
    return [card.cost for card in cards]  

@router.get("/card.cost/filter")
def get_card_cost_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.cost

@router.get("/card.keyword")
def get_card_keyword(db: Session = Depends(get_db)):
    cards = db.query(models.Card).order_by(models.Card.card_id).all()
    return [card.keyword for card in cards]  

@router.get("/card.keyword/filter")
def get_card_keyword_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.keyword

@router.get("/card.explanation")
def get_card_explanation(db: Session = Depends(get_db)):
    cards = db.query(models.Explanation).order_by(models.Explanation.card_id).all()
    return [card.explanation for card in cards]  

@router.get("/card.explanation/filter")
def get_card_explanation_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Explanation).filter(models.Explanation.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.explanation

@router.post("/match_players/{match_id}/{user_id}/pay_cost")
def pay_cost(
    match_id: int,
    user_id: int,
    amount: int,  # 消費するコスト（例: 10）
    db: Session = Depends(get_db)
):
    entry = db.query(models.MatchPlayer).filter_by(
        match_id=match_id,
        my_id=user_id
    ).first()

    entry.wallet -= amount
    db.commit()

    return {
        "message": f"{amount} 支払いました。",
        "wallet": entry.wallet
    }





app.include_router(router)



    