from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from app.modules.cart import models
from app.modules.cart import Schema
from typing import List
from app.modules.oauth2.oauth2_router import get_current_user
from app.modules.user.models import User

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.get("/", response_model=List[Schema.CartOut])
def get_carts(db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    carts = db.query(models.Cart).filter(models.Cart.owner_id == current_user.id).all()
    return carts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.CartOut)
def create_cart(cart: Schema.CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_cart = models.Cart(owner_id=current_user.id, total_amount=cart.total_amount)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

@router.put("/{cart_id}", response_model=Schema.CartOut)
def update_cart(cart_id: int, cart_update: Schema.CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_query = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id)
    cart = cart_query.first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found or not authorized")
    cart_query.update({"total_amount": cart_update.total_amount}, synchronize_session=False)
    db.commit()
    return cart_query.first()

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_query = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id)
    cart = cart_query.first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found or not authorized")
    cart_query.delete(synchronize_session=False)
    db.commit()
    return None
