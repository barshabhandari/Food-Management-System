from typing import Optional
from pydantic import BaseModel
from app.modules.user.Schema import UserOut

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    id: Optional[str]= None
