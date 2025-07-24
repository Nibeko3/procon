from fastapi import APIRouter, Depends,HTTPException
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

@router.get("/player/{user_id}")
def get_player_profile(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.Player = Depends(get_current_user)
):
    # 自分自身かどうか
    if user_id == "me":
        target_user = current_user
    else:
        try:
            target_user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id")

        target_user = db.query(models.Player).filter_by(user_id=target_user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="Player not found")

    # ランキング順位を取得
    ranked_players = (
        db.query(models.Player)
        .order_by(models.Player.score.desc())
        .all()
    )

    position = next(
        (i + 1 for i, p in enumerate(ranked_players) if p.user_id == target_user.user_id),
        None
    )

    return {
        "username": target_user.username,
        "score": target_user.score,
        "rank": get_rank(target_user.score),
        "position": position
    }
