from ...database import Base
from sqlalchemy import TIMESTAMP, Column, Float, Integer, ForeignKey, text
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"),
                        nullable=False)
    total_amount = Column(Float, nullable=False)
    owner = relationship("User", back_populates="carts")
    payments = relationship("Payment", back_populates="cart")
    
