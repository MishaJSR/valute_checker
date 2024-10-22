import asyncio
import logging

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
async def convert_values(from_param: str = Query(..., alias="from"), to: str = None, value: int = 1):
    """
    По telegram id пользователя бота и городу получить данные о погоде \n
    Возвращает обьект dict вида: \n

        some_dict =
            {
              "town": "Лондон",
              "temperature": 15.04,
              "feels_like": 14.74,
              "weather_description": "пасмурно",
              "humidity": 82,
              "wind_speed": 1.54
            }
    """
    try:
        first_param = RedisManager.get_from_redis(from_param)
        second_param = RedisManager.get_from_redis(to)
    except NoneDataException as e:
        return HTTPException(status_code=400, detail={e.message})
    except AttributeException as e:
        return HTTPException(status_code=400, detail={e.message})
    except redis.exceptions.ConnectionError:
        return HTTPException(status_code=500, detail={"Ошибка подключения к базе данных"})

