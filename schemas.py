# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

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

class MatchPlayerOut(BaseModel):
    match_id: int
    my_id: int
    opponent_id: Optional[int]
    wallet: int
    production_power: int

    model_config = {
        "from_attributes": True
    }
