from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ...config import settings
from . import Schema
from  app.modules.user import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KRY= settings.secret_key
ALGORITHM= settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode= data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode, SECRET_KRY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        payload= jwt.decode(token, SECRET_KRY, algorithms=ALGORITHM)
        id: str= payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data= Schema.TokenData(id = str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str= Depends(oauth2_scheme),
                     db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Couldnot validate credentielas",
                                          headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credentials_exception)
    try:
        user_id = int(token.id)
    except (ValueError, TypeError):
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
