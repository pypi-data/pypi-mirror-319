from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from .base import Base

class TaskModel(Base):
    __tablename__ = 'task_info'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(255))
    task_text = Column(Text)
    task_status = Column(Integer, default=0)
    material_id = Column(Integer)
    deleted = Column(Integer, default=0)
    create_time = Column(DateTime, default=lambda: datetime.now(UTC))
    update_time = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)) 