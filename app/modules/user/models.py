from sqlalchemy import TIMESTAMP, Column, Integer, String, text, Boolean
from ...database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    is_active = Column(Boolean, server_default=text('True'), nullable=False) 
    products = relationship("Product", back_populates="owner")
    carts = relationship("Cart", back_populates="owner")
    

