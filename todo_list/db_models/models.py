"""In this module there are sqlalchemy objects representing database tables and their columns.
"""
from sqlalchemy.orm import declarative_base

from sqlalchemy import (
    Column, String, Boolean, Date)

Base = declarative_base()


class TodoList(Base):
    __tablename__ = 'TODO_LIST'

    __table_args__ = ()

    task_id = Column(
        'task_id', String(36), primary_key=True, unique=True, nullable=False
    )

    text = Column(
        'text', String(255), nullable=False
    )

    status = Column(
        'status', Boolean, nullable=False
    )

    deadline = Column(
        'deadline', Date, nullable=False
    )