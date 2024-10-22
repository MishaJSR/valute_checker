import logging

import redis

from redis_manager.exceptions import NoneDataException
from redis_manager.schemas import RedisSendData, RedisGetData
from redis_manager.exceptions import exception_wrapper
from base_config import Settings


class RedisManager:
    host, port = Settings().get_redis_config()
    client = redis.Redis(host=host, port=port, db=0, decode_responses=True)

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
        return float(RedisManager.client.get(data.key))

    @staticmethod
    def get_all():
        keys = RedisManager.client.keys("*")
        all_data = {}
        for key in keys:
            value = RedisManager.client.get(key)
            all_data[key] = value
        return all_data
