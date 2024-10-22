import logging

import pydantic
import redis


def exception_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pydantic.ValidationError as e:
            logging.warning("Cant validate params")
            raise AttributeException
        except redis.exceptions.ConnectionError as e:
            logging.warning("Connection not established\n")
            raise redis.exceptions.ConnectionError

    return wrapper


class AttributeException(AttributeError):
    def __init__(self, message="Ошибка при проверке параметров, проверьте параметры запроса"):
        self.message = message
        super().__init__(self.message)


class NoneDataException(AttributeError):
    def __init__(self, message="Данной валюты нет в базе ", key=""):
        self.message = message + key
        super().__init__(self.message)
