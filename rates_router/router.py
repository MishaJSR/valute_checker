import asyncio
import logging
from typing import Optional, Union

import pydantic
import redis
from fastapi import APIRouter, Depends, HTTPException, Query

from base_config import Settings
from rates_router.schemas import ConvertData
from redis_manager.RedisManager import RedisManager
from redis_manager.exceptions import NoneDataException, AttributeException

router = APIRouter(
    prefix="/rates",
    tags=["Rates"]
)



@router.post("")
async def convert_values(data: ConvertData):
    try:
        value = round(data.value, 2)
        first_param = RedisManager.get_from_redis(data.fr_key)
        second_param = RedisManager.get_from_redis(data.to_key)
        k = round(first_param / second_param, 3)
        res = round(k * value, 3)
        return {
            "result": res
        }
    except NoneDataException as e:
        return HTTPException(status_code=400, detail={e.message})
    except AttributeException as e:
        return HTTPException(status_code=400, detail={e.message})
    except redis.exceptions.ConnectionError:
        return HTTPException(status_code=500, detail={"Ошибка подключения к базе данных"})
    except pydantic.ValidationError:
        return HTTPException(status_code=422, detail={"Ошибка при проверке корректности полей"})


@router.get("/val_list")
async def val_list():
    """
    Возвращает список доступных валют вида dict вида: \n

        some_dict =
            {
              "RUB": 1.0,
              "USD": 97.332,
            }
    """
    try:
        res = RedisManager.get_all()
        return res
    except redis.exceptions.ConnectionError:
        return HTTPException(status_code=500, detail={"Ошибка подключения к базе данных"})
