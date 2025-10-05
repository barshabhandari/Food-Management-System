from sqlalchemy import TIMESTAMP, Column, Integer, String, text, Boolean, func
from ...database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    is_active = Column(Boolean, server_default=text('true'), nullable=False)
    is_admin = Column(Boolean, server_default=text('false'), nullable=False)
    products = relationship("Product", back_populates="owner")
    carts = relationship("Cart", back_populates="owner")
    payments = relationship("Payment", back_populates="user")
    
    

