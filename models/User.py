from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    firebase_uuid = Column(String)
    role = Column(Enum("USER", "ADMIN", name="roleenum"), default="USER")

    groups = relationship("GroupUsers", back_populates="user")