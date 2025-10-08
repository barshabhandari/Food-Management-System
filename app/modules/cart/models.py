from ...database import Base
from sqlalchemy import Column, Integer, Float, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)

    owner = relationship("User", back_populates="carts")
    payments = relationship("Payment", back_populates="cart", lazy="select")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
