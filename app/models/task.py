from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import User

class Task(Base):
    __tablename__ = 'tasks'
    __tableargs__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    slug = Column(String, unique=True, index=True)
    user = relationship("User", back_populates='tasks')

# Печать SQL запроса в консоль при помощи CrateTable
# from sqlalchemy.schema import CreateTable
# print(CreateTable(Task.__table__))