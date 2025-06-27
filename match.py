from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user  # トークンからユーザー取得

router = APIRouter()

'''@router.post("/match/create", response_model=schemas.MatchOut)
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
    return new_match'''

from sqlalchemy.exc import SQLAlchemyError

@router.post("/match/random", response_model=schemas.MatchOut)
def auto_match(
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    try:
        # トランザクションの中で open match をロックつきで取得
        with db.begin_nested():
            open_match = db.query(models.Match)\
                .filter(models.Match.player2_id == None)\
                .with_for_update(skip_locked=True)\
                .first()

            if open_match and open_match.player1_id != current_user.user_id:
                open_match.player2_id = current_user.user_id
                open_match.current_player_id = open_match.player1_id
                db.commit()
                db.refresh(open_match)
                return open_match

            # 自分がすでに作ったマッチがある場合、それを再利用
            existing = db.query(models.Match).filter(
                models.Match.player1_id == current_user.user_id,
                models.Match.player2_id == None
            ).first()
            if existing:
                return existing

            # 新しくマッチ作成
            new_match = models.Match(
                player1_id=current_user.user_id,
                current_player_id=current_user.user_id
            )
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            return new_match

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="マッチング中にエラーが発生しました")
