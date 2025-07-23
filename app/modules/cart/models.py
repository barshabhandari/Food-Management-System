from database import Base
from sqlalchemy import TIMESTAMP, Column, Float, Integer, ForeignKey, text
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"),
                        nullable=False)
    total_amount = Column(Float, nullable=False)
    user = relationship("User", back_populates="carts")
    
