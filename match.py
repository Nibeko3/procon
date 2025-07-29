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
        models.MatchPlayer.my_id == current_user.user_id,
        models.MatchPlayer.is_active == True
    ).first()

    if existing_entry:
        match = db.query(models.Match).filter_by(id=existing_entry.match_id).first()
        return match

    # 待機中プレイヤーを探す
    open_entry = (
        db.query(models.MatchPlayer).filter(
            models.MatchPlayer.opponent_id == None,
            models.MatchPlayer.is_active == True,
            models.MatchPlayer.my_id != current_user.user_id
        ).first()
    )

    if open_entry:
        match = db.query(models.Match).filter_by(id=open_entry.match_id).first()
        opponent_id = open_entry.my_id

        # 自分側を登録
        new_entry = models.MatchPlayer(
            match_id=match.id,
            my_id=current_user.user_id,
            opponent_id=opponent_id
        )
        db.add(new_entry)

        # 相手側の opponent_id を更新
        open_entry.opponent_id = current_user.user_id

        # ターン情報も設定
        match.current_player_id = opponent_id
        db.commit()
        return match

    # マッチがなければ新規作成
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

@router.get("/match_players/{match_id}/ready")
def is_match_ready(match_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.MatchPlayer).filter_by(match_id=match_id, opponent_id=None).first()
    return {"ready": entry is None}

@router.post("/match/{match_id}/cancel")
def cancel_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # 該当するマッチプレイヤーエントリを取得
    entry = db.query(models.MatchPlayer).filter_by(
        match_id=match_id, my_id=current_user.user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="You are not in this match")

    # 自分のis_activeをFalseにする
    entry.is_active = False

    db.commit()
    return {"message": "Match canceled successfully"}

@router.get("/match_players/{match_id}/{user_id}", response_model=schemas.MatchPlayerOut)
def get_match_player(
    match_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    entry = db.query(models.MatchPlayer).filter_by(
        match_id=match_id,
        my_id=user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="MatchPlayer not found")

    return entry  # ← response_model により自動でスキーマ形式に変換
