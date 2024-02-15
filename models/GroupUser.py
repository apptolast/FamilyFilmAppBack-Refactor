from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class GroupUsers(Base):
    __tablename__ = "group_users"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", backref="group_users")
    group = relationship("Group", backref="group_users")

    __table_args__ = (UniqueConstraint("user_id", "group_id", name="unique_user_group"),)
