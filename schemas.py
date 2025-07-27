# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EffectOut(BaseModel):
    effect_id: int
    effect: str

    model_config = ConfigDict(from_attributes=True)

class PlayerCreate(BaseModel):
    username: str
    password: str

class PlayerLogin(BaseModel):
    username: str
    password: str

class MatchOut(BaseModel):
    id: int
    current_turn: int
    current_player_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

