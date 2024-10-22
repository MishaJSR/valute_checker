import logging

import redis

from redis_manager.exceptions import NoneDataException
from redis_manager.schemas import RedisSendData, RedisGetData
from redis_manager.exceptions import exception_wrapper


class RedisManager:
    client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

    @staticmethod
    @exception_wrapper
    def send_to_redis(key: str, value: float):
        data = RedisSendData(key=key, value=value)
        RedisManager.client.set(data.key, data.value)
        return True

    @staticmethod
    @exception_wrapper
    def get_from_redis(key: str):
        data = RedisGetData(key=key)
        res = RedisManager.client.get(data.key)
        if not res:
            logging.error(f"{NoneDataException().message} {key}")
            raise NoneDataException(key=key)
        return RedisManager.client.get(data.key)
