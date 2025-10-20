from sqlalchemy import Column, Integer, Float, String, ForeignKey, TIMESTAMP, text, Enum, Boolean, Date
from sqlalchemy.orm import relationship
from ...database import Base
import enum


# ---------------- ENUM FOR PAYMENT STATUS ----------------
class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ---------------- PRODUCT MODEL ----------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    actual_price = Column(Integer, nullable=False)
    discount_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    is_published = Column(Boolean, server_default=text('true'), nullable=False)
    image_id = Column(Integer, ForeignKey("images.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    expire_date = Column(Date, nullable=True)
    manufacture_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")
    image = relationship("Image")


# ---------------- PAYMENT MODEL ----------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), server_default="PENDING", nullable=False)

    # ✅ Transaction ID is used by your /initiate route
    transaction_id = Column(String, nullable=True)

    # ✅ Created timestamp (works in PostgreSQL)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    # ✅ Updated timestamp (optional but now matches DB)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    # ✅ Relationships
    user = relationship("User", back_populates="payments")
    cart = relationship("Cart", back_populates="payments")
