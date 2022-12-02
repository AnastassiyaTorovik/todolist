from pydantic import BaseModel, validator, Field
from datetime import date, datetime
from typing import Optional
import re


class TaskValidator(BaseModel):
    """data types enforcement"""
    deadline: date
    task_id: str = Field(max_length=36)
    text: str = Field(max_length=255)
    is_done: Optional[bool] = False

    @validator('task_id')
    def task_id_characters_check(cls, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError('Task id can only contain characters [a-zA-Z0-9_]')
        return value

    @validator('deadline', pre=True)
    def date_check(cls, value):
        assert datetime.strptime(value, '%Y-%m-%d')
        return value
