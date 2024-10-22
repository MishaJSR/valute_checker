from pydantic import BaseModel, field_validator


def validate_key(v: str) -> str:
    if not (len(v) == 3 and v.isupper() and v.isalpha()):
        raise ValueError('key must be exactly 3 uppercase English letters')
    return v


class RedisSendData(BaseModel):
    key: str
    value: float

    @field_validator('key')
    def check_key(cls, v):
        return validate_key(v)


class RedisGetData(BaseModel):
    key: str

    @field_validator('key')
    def check_key(cls, v):
        return validate_key(v)
