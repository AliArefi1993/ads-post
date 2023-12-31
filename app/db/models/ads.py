from sqlalchemy import Column, Integer, ForeignKey, Float, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.database import Base


class Ads(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    pic_path = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="adses")
    comments = relationship("Comment", back_populates="ads")
