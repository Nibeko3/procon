from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from database import get_db
from auth import get_current_user  # トークンからユーザー取得

router = APIRouter()

@router.post("/match/random", response_model=schemas.MatchOut)
def random_match(
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # すでに待機中ならそのマッチを返す
    existing_entry = db.query(models.MatchPlayer).filter(
        models.MatchPlayer.my_id == current_user.user_id
    ).first()

    if existing_entry:
        match = db.query(models.Match).filter_by(id=existing_entry.match_id).first()
        return match

    # 相手がまだいないマッチを探す（マッチID単位で1人だけのもの）
    subquery = db.query(
        models.MatchPlayer.match_id
    ).group_by(models.MatchPlayer.match_id).having(func.count() == 1).subquery()

    open_match = db.query(models.Match).filter(models.Match.id.in_(subquery)).first()

    if open_match:
        # 相手となるプレイヤーのIDを取得
        opponent_entry = db.query(models.MatchPlayer).filter_by(match_id=open_match.id).first()
        opponent_id = opponent_entry.my_id

        # 自分側を登録
        new_entry = models.MatchPlayer(
            match_id=open_match.id,
            my_id=current_user.user_id,
            opponent_id=opponent_id
        )
        db.add(new_entry)

        # 相手のopponent_idも更新
        opponent_entry.opponent_id = current_user.user_id

        # ターン情報も初期化（必要なら）
        open_match.current_player_id = opponent_id
        db.commit()
        return open_match

    # 空きマッチがなければ新規作成
    new_match = models.Match(
        current_turn=1,
        current_player_id=current_user.user_id
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    new_entry = models.MatchPlayer(
        match_id=new_match.id,
        my_id=current_user.user_id,
        opponent_id=None
    )
    db.add(new_entry)
    db.commit()

    return new_match

@router.get("/match/{match_id}", response_model=schemas.MatchOut)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
):
    match = db.query(models.Match).filter_by(id=match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    return match

