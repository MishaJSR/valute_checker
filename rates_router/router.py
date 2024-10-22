import asyncio
import logging
from typing import Optional, Union

import redis
from fastapi import APIRouter, Depends, HTTPException, Query

from base_config import Settings
from redis_manager.RedisManager import RedisManager
from redis_manager.exceptions import NoneDataException, AttributeException

router = APIRouter(
    prefix="/rates",
    tags=["Rates"]
)


@router.get("")
async def convert_values(from_param: str = Query(..., alias="from"), to: str = None,
                         value: Optional[Union[int, float]] = 1):
    """
    Возвращает обьект dict вида: \n

        some_dict =
            {
              "result": 124.123,
            }
    """
    value = round(value, 2)
    try:
        first_param = RedisManager.get_from_redis(from_param)
        second_param = RedisManager.get_from_redis(to)
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

