from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import EffectOut
from typing import List
from sqlalchemy import create_engine, text
import os

app = FastAPI()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "world ver 0004"}#更新数


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@router.get("/effect/all")
def get_effect_texts(db: Session = Depends(get_db)):
    effects = db.query(models.Effect).all()
    return [e.effect for e in effects]

@router.get("/effect/filter")
def get_effect_text(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(models.Effect).filter(models.Effect.effect_id == effect_id).first()
    if not effect:
        return "該当する効果が見つかりません"
    return effect.effect

@router.get("/card/all")
def get_effect_texts(db: Session = Depends(get_db)):
    effects = db.query(models.Card).all()
    return [e.effect for e in effects]


app.include_router(router)



    