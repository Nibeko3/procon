from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user  # トークンからユーザー取得
import models

router = APIRouter()

def get_rank(score: int) -> str:
    if score < 1500:
        return "全商Ⅲ"
    elif score < 1600:
        return "全商Ⅱ"
    elif score < 1700:
        return "全商Ⅰ"
    elif score < 1800:
        return "ベーシック"
    elif score < 1900:
        return "ITパスポート"
    elif score < 2100:
        return "基本情報技術者"
    elif score < 2300:
        return "応用情報技術者"
    elif score < 2500:
        return "安全確保支援士"

@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # ランキング位置を計算
    ranked_players = (
        db.query(models.Player)
        .order_by(models.Player.score.desc())
        .all()
    )

    position = next(
        (i + 1 for i, p in enumerate(ranked_players) if p.user_id == current_user.user_id),
        None
    )

    return {
        "username": current_user.username,
        "score": current_user.score,
        "rank": get_rank(current_user.score),
        "position": position
    }
