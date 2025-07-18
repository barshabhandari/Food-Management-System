from typing import Optional
from pydantic import BaseModel

class ImageBase(BaseModel):
    id: int
    key: str
