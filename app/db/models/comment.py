from sqlalchemy import Column, Integer, ForeignKey, Float, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    text = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"), unique=True)
    owner = relationship("User", back_populates="comment")

    ads_id = Column(Integer, ForeignKey("ads.id"))
    ads = relationship("Ads", back_populates="comments")
