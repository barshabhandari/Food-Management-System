from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String, text, Date, func
from ...database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False )
    name = Column(String, nullable=False)
    actual_price = Column(Integer, nullable=False)
    discount_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    is_published = Column(Boolean, server_default=text('True'), nullable=False)
    expire_date = Column(Date, nullable=True)
    image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'),
                        nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="products")
    image = relationship("Image", back_populates="product")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")