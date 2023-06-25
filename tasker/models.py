from sqlalchemy import Boolean, Column, String, Integer
from database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    is_complete = Column(Boolean, nullable=False)
    primary = Column(Boolean, nullable=False)

