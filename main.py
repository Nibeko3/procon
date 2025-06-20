from fastapi import APIRouter,FastAPI,Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import EffectOut
from typing import List

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
    return {"message": "fuck u world"}
    
from sqlalchemy import create_engine,text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.get("/test-db")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT now()"))
        return {"db_time": result.scalar()}

@app.get("/effect/", response_model=List[EffectOut])
def get_effects(db: Session = Depends(get_db)):
    return db.query(models.Effect).filter(models.Effect.effect_id<=5).all()

@router.get("/effect/text")
def get_effect_text(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(models.Effect).filter(models.Effect.effect_id == effect_id).first()
    if not effect:
        return "該当する効果が見つかりません"
    return effect.effect  # ← 文字列だけを返す
app.include_router(router)



    