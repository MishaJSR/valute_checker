from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel, field_validator

from redis_manager.schemas import validate_key


class ConvertData(BaseModel):
    fr_key: str
    to_key: str
    value: int | float

    @field_validator('fr_key', mode="after")
    @classmethod
    def check_key(cls, v):
        return validate_key(v)

    @field_validator('to_key', mode="after")
    @classmethod
    def check_key(cls, v):
        return validate_key(v)
