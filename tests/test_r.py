import redis

from redis_manager.RedisManager import RedisManager

#print(RedisManager.send_to_redis("DKK", 0))
#print(RedisManager.get_from_redis("DKK"))
client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
val = RedisManager.get_from_redis("DKK")
print(val)