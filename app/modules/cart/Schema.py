from datetime import datetime
from pydantic import BaseModel

class CartCreate(BaseModel):
    id: int
    total_amount: float

class CartOut(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    total_amount: float

    class Config:
        form_attributes = True