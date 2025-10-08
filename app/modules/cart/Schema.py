from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


# ---------- Cart Item Schemas ----------
class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True


# ---------- Cart Schemas ----------
class CartCreate(BaseModel):
    pass  # no input needed; backend sets total_amount = 0


class CartOut(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    total_amount: float
    items: Optional[List[CartItemOut]] = []

    class Config:
        orm_mode = True
