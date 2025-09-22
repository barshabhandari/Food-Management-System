from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentBase(BaseModel):
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    cart_id: int

class PaymentOut(PaymentBase):
    id: int
    user_id: int
    cart_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class PaymentInitiate(BaseModel):
    cart_id: int
    success_url: str
    failure_url: str

class PaymentResponse(BaseModel):
    payment_url: str
    transaction_id: str
