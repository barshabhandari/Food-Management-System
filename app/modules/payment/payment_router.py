from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from app.modules.product.models import Payment, PaymentStatus
from . import Schema
from app.modules.oauth2.oauth2_router import get_current_user
from app.modules.user.models import User
from app.modules.cart.models import Cart
import uuid

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initiate", response_model=Schema.PaymentResponse)
def initiate_payment(
    payment_data: Schema.PaymentInitiate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Check if cart exists and belongs to user
    cart = db.query(Cart).filter(Cart.id == payment_data.cart_id, Cart.owner_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    # Check if cart has a pending payment
    existing_payment = db.query(models.Payment).filter(
        models.Payment.cart_id == payment_data.cart_id,
        models.Payment.status == models.PaymentStatus.PENDING
    ).first()
    if existing_payment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment already initiated for this cart")

    # Create payment record
    transaction_id = str(uuid.uuid4())
    new_payment = models.Payment(
        user_id=current_user.id,
        cart_id=payment_data.cart_id,
        amount=cart.total_amount,
        transaction_id=transaction_id
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    # Simulate eSewa payment URL (in real implementation, use eSewa API)
    payment_url = f"https://esewa.com.np/epay/main?amt={cart.total_amount}&txAmt=0&psc=0&pdc=0&scd=YOUR_MERCHANT_CODE&tAmt={cart.total_amount}&pid={transaction_id}&su={payment_data.success_url}&fu={payment_data.failure_url}"

    return Schema.PaymentResponse(payment_url=payment_url, transaction_id=transaction_id)

@router.get("/success")
def payment_success(
    oid: str,  # transaction_id
    amt: str,
    refId: str,  # eSewa reference
    db: Session = Depends(get_db)
):
    # Update payment status to completed
    payment = db.query(models.Payment).filter(models.Payment.transaction_id == oid).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    payment.status = models.PaymentStatus.COMPLETED
    db.commit()

    return {"message": "Payment successful", "transaction_id": oid, "ref_id": refId}

@router.get("/failure")
def payment_failure(
    oid: str,
    amt: str,
    db: Session = Depends(get_db)
):
    # Update payment status to failed
    payment = db.query(models.Payment).filter(models.Payment.transaction_id == oid).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    payment.status = models.PaymentStatus.FAILED
    db.commit()

    return {"message": "Payment failed", "transaction_id": oid}

@router.get("/", response_model=list[Schema.PaymentOut])
def get_user_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    payments = db.query(models.Payment).filter(models.Payment.user_id == current_user.id).all()
    return payments
