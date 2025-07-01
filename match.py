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

@router.post("/match/random", response_model=schemas.MatchOut)
def auto_match(
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # 自分がすでに待機中か確認
    existing = db.query(models.Match).filter(
        models.Match.player1_id == current_user.user_id,
        models.Match.player2_id == 0
    ).first()
    if existing:
        return existing

    # 他人が待機してるマッチがあれば参加
    open_match = db.query(models.Match).filter(
        models.Match.player2_id == 0,
        models.Match.player1_id != current_user.user_id
    ).first()

    if open_match:
        open_match.player2_id = current_user.user_id
        open_match.current_player_id = open_match.player1_id
        db.commit()
        db.refresh(open_match)
        return open_match

    # 新しく待機マッチを作成
    new_match = models.Match(
        player1_id=current_user.user_id,
        current_player_id=current_user.user_id
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match

@router.get("/match/{match_id}", response_model=schemas.MatchOut)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    match = db.query(models.Match).filter_by(id=match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if current_user.user_id not in [match.player1_id, match.player2_id]:
        raise HTTPException(status_code=403, detail="You are not a participant in this match")

    return schemas.MatchOut(
        id=match.id,
        player1_id=match.player1_id,
        player2_id=match.player2_id or 0,
        current_turn=match.current_turn,
        current_player_id=match.current_player_id,
        wallet_player1=match.wallet_player1,
        wallet_player2=match.wallet_player2,
        production_power_player1=match.production_power_player1,
        production_power_player2=match.production_power_player2,
        created_at=match.created_at,
    )
