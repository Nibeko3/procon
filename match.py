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

@router.post("/match/random", response_model=schemas.MatchInfo)
def auto_match(
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # 自分が既に待機してないか確認
    existing_match = db.query(models.Match).filter(
        models.Match.player1_id == current_user.user_id,
        models.Match.player2_id == None
    ).first()
    if existing_match:
        return existing_match

    # 相手が待機してるマッチを探す
    open_match = db.query(models.Match).filter(
        models.Match.player2_id == None,
        models.Match.player1_id != current_user.user_id
    ).first()

    if open_match:
        open_match.player2_id = current_user.user_id
        open_match.current_player_id = open_match.player1_id
        db.commit()
        db.refresh(open_match)
        return open_match

    # 自分が待機するマッチを新規作成
    new_match = models.Match(
        player1_id = current_user.user_id,
        current_player_id = current_user.user_id
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match
