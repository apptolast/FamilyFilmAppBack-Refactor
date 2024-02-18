from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class GroupUser(Base):
    __tablename__ = 'group_users'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)

    user = relationship('User', back_populates='groups')
    group = relationship('Group', back_populates='users')
