from pydantic import BaseModel
from typing import Optional


class bmi(BaseModel):
    Gender: str
    HeightCm: float
    WeightKg: float