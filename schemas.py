# schemas.py
from pydantic import BaseModel, ConfigDict

class EffectOut(BaseModel):
    effect_id: int
    effect: str

    model_config = ConfigDict(from_attributes=True)
