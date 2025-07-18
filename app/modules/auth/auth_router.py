from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from . import Schema
from sqlalchemy.orm import Session
from ...database import get_db
from app.modules.user import models
from ... import utils
from app.modules.oauth2 import Schema, oauth2_router


router = APIRouter(prefix="/login",
                   tags=['Authentication'])

@router.post("/", response_model= Schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    access_token= oauth2_router.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
