from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    actual_price: int
    discount_price: float
    stock: int
    is_published: bool = True
    image_id: Optional[int] = None
    category_id: Optional[int] = None
    expire_date: date | None = None


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id : int
    created_at : datetime
    owner_id: int
    image_id: int

    class Config():
        form_attributes = True

class ProductSearchResponse(BaseModel):
    products: List[Product]
    message: Optional[str] = None

