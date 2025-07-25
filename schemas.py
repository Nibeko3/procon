# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
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

class MatchCreate(BaseModel):
    opponent_username: str

class MatchOut(BaseModel):
    id: int
    player1_id: int
    player2_id: Optional[int]
    current_turn: int
    current_player_id: int
    wallet_player1: int
    wallet_player2: int
    production_power_player1: int
    production_power_player2: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }