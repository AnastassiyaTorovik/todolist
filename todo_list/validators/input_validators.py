from pydantic import BaseModel, validator, Field, root_validator
from datetime import date, datetime
from typing import Optional, Literal, Union
import re


Deadline = Union[date, Literal['now']]
Sort = Literal['urgency']


class TaskValidator(BaseModel):
    """data types enforcement"""
    deadline: date
    task_id: str = Field(max_length=36)
    text: str = Field(max_length=255)
    is_done: Optional[bool] = False # accepts values[true, false, yes, no], not case sensitive

    @validator('task_id')
    def task_id_characters_check(cls, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError('Task id can only contain characters [a-zA-Z0-9_]')
        return value

    @validator('deadline', pre=True)
    def date_check(cls, value):
        assert datetime.strptime(value, '%Y-%m-%d')
        return value


class FilterTasksValidator(BaseModel):
    date_from: Optional[Deadline] = None
    date_to: Optional[Deadline] = None
    count: Optional[int] = None
    sort_by: Optional[Sort] = None
    is_done: Optional[bool] = None  # accepts values[true, false, yes, no], not case sensitive

    @validator("date_from", "date_to", pre=True)
    def validate_all_fields_one_by_one(cls, field_value):
        if not field_value:
            return field_value

        if field_value == 'now':
            field_value = datetime.now().date()
        else:
            assert datetime.strptime(field_value, '%Y-%m-%d')
        return field_value

    @root_validator()
    def validate_date_filters_cooperation(cls, field_values):
        if field_values.get("date_from") and field_values.get("date_to"):
            assert field_values["date_from"] <= field_values["date_to"], \
                "date_from needs to be lower or equal to date_to."
        return field_values

