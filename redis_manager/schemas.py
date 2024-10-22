from pydantic import BaseModel, field_validator
from fastapi.exceptions import HTTPException


def validate_key(v: str) -> str:
    if not (len(v) == 3 and v.isupper() and v.isalpha()):
        raise HTTPException(status_code=422, detail=f'key {v} must be exactly 3 uppercase English letters')
    return v


class RedisSendData(BaseModel):
    key: str
    value: float

    @staticmethod
    @field_validator('key')
    def check_key(v):
        return validate_key(v)


class RedisGetData(BaseModel):
    key: str

    @staticmethod
    @field_validator('key')
    def check_key(v):
        return validate_key(v)
