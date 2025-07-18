from datetime import datetime
from pydantic import BaseModel, EmailStr



class PostBase(BaseModel):
    name: str
    actual_price: int
    discount_price: float
    stock: int
    is_published: bool=True
    image_id: int
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id: int
        
    class Config():
        form_attributes = True

