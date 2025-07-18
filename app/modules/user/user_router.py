from fastapi import APIRouter, Depends,  status, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from . import models, Schema
from ... import utils

router = APIRouter(prefix="/users", 
                   tags=['User'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.UserOut)
async def create_user(user:Schema.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=Schema.UserOut)
async def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Td {id} not availabe")
    return user


    

