from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import EffectOut
from sqlalchemy import create_engine, text
import os
from auth import router as auth_router
from match import router as match_router



app = FastAPI()
router = APIRouter()
app.include_router(auth_router)
app.include_router(match_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "world ver 1120"}#更新数


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


@router.get("/effect")
def get_effect_all(db: Session = Depends(get_db)):
    effects = db.query(models.Effect).all()
    return effects

@router.get("/effect.effect")
def get_effect_effect(db: Session = Depends(get_db)):
    effects = db.query(models.Effect).all()
    return [effect.effect for effect in effects]  

@router.get("/effect.effect/filter")
def get_effect_effect_filter(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(models.Effect).filter(models.Effect.effect_id == effect_id).first()
    if not effect:
        return "該当する効果が見つかりません"
    return effect.effect


@router.get("/card")
def get_card_all(db: Session = Depends(get_db)):
    cards = db.query(models.Card).all()
    return cards

@router.get("/card.name")
def get_card_name(db: Session = Depends(get_db)):
    cards = db.query(models.Card).all()
    return [card.name for card in cards]  

@router.get("/card.name/filter")
def get_card_name_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.name

@router.get("/card.cost")
def get_card_cost(db: Session = Depends(get_db)):
    cards = db.query(models.Card).all()
    return [card.cost for card in cards]  

@router.get("/card.cost/filter")
def get_card_cost_filter(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        return "該当する効果が見つかりません"
    return card.name

app.include_router(router)



    