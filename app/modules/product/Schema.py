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
    manufacture_date: date | None = None


class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id : int
    name: str
    actual_price: int
    discount_price: float
    stock: int
    is_published: bool
    category_id: Optional[int] = None
    expire_date: date | None = None
    manufacture_date: date | None = None
    created_at : datetime
    owner_id: int
    image_url: Optional[str] = None

    class Config():
        form_attributes = True

class Product(ProductBase):
    id : int
    created_at : datetime
    owner_id: int
    image_url: Optional[str] = None

    class Config():
        form_attributes = True

class ProductSearchResponse(BaseModel):
    products: List[ProductResponse]
    message: Optional[str] = None

