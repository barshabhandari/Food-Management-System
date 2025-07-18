from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String, text
from ...database import Base
from sqlalchemy.orm import relationship

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False )
    key = Column(String, unique=True)