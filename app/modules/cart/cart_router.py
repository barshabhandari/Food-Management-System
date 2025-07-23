from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.modules.cart import models
from app.modules.cart import Schema

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.get("/")
def get_carts(db:Session = Depends(get_db)):
    carts = db.query(models.Cart).all()
    return carts

