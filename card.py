from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from database import get_db

router = APIRouter()

@router.get("/card/{card_id}", response_model=schemas.CardDetailOut)
def get_card_detail(
    card_id: int,
    db: Session = Depends(get_db),
):
    card = (
        db.query(models.Card)
        .filter(models.Card.card_id == card_id)
        .first()
    )
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # 説明文と効果を手動で組み合わせて返す
    return schemas.CardDetailOut(
        card_id=card.card_id,
        name=card.name,
        keyword=card.keyword,
        cost=card.cost,
        effect=card.effect.effect,
        explanation=card.explanation.explanation[0]
    )
