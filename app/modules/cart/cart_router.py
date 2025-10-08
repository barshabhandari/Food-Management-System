import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from app.modules.cart import models, Schema
from app.modules.user.models import User
from app.modules.product.models import Product, Payment
from app.modules.oauth2.oauth2_router import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/carts", tags=["Carts"])


# ---------- GET ALL CARTS ----------
@router.get("/", response_model=List[Schema.CartOut])
def get_carts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    carts = db.query(models.Cart).filter(models.Cart.owner_id == current_user.id).all()
    return carts


# ---------- CREATE CART ----------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.CartOut)
def create_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    new_cart = models.Cart(owner_id=current_user.id, total_amount=0)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


# ---------- ADD ITEM TO CART ----------
@router.post("/{cart_id}/items", response_model=Schema.CartOut)
def add_item_to_cart(
    cart_id: int,
    item: Schema.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Find cart
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Find product
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Calculate price (backend-controlled)
    total_price = product.discount_price * item.quantity

    # Create cart item
    new_item = models.CartItem(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=total_price
    )

    # Update total
    cart.total_amount += total_price
    db.add(new_item)
    db.commit()
    db.refresh(cart)

    return cart


# ---------- UPDATE CART ITEM ----------
@router.put("/{cart_id}/items/{item_id}", response_model=Schema.CartOut)
def update_cart_item(
    cart_id: int,
    item_id: int,
    item_update: Schema.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Recalculate total
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Subtract old item price, then add new
    cart.total_amount -= cart_item.price
    new_price = product.discount_price * item_update.quantity
    cart_item.quantity = item_update.quantity
    cart_item.price = new_price
    cart.total_amount += new_price

    db.commit()
    db.refresh(cart)
    return cart


# ---------- DELETE CART ITEM ----------
@router.delete("/{cart_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    cart_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Adjust total amount
    cart.total_amount -= cart_item.price

    db.delete(cart_item)
    db.commit()
    return None


# ---------- DELETE WHOLE CART ----------
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK)
def delete_cart(cart_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id, models.Cart.owner_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    try:
        # Delete related cart items and payments first to avoid foreign key issues
        db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
        db.query(Payment).filter(Payment.cart_id == cart.id).delete()
        db.delete(cart)
        db.commit()
        logger.info(f"Cart {cart_id} deleted by user {current_user.id}")
        return {"message": "Cart deleted successfully. The admin has been notified."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete cart: {str(e)}")
