from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user  # トークンからユーザー取得

router = APIRouter()

@router.post("/match/create", response_model=schemas.MatchOut)
def create_match(
    request: schemas.MatchCreate,
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    opponent = db.query(models.Player).filter_by(username=request.opponent_username).first()
    if not opponent:
        raise HTTPException(status_code=404, detail="Opponent not found")

    if opponent.user_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="Cannot match against yourself")

    new_match = models.Match(
        player1_id=current_user.user_id,
        player2_id=opponent.user_id,
        current_player_id=current_user.user_id
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match
