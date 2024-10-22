from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    URL: str
    REDISUSERNAME: str
    REDISHOST: str
    REDISPORT: int
    REDISPASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_url(self):
        return self.URL

    def get_redis_config(self):
        return self.REDISHOST, self.REDISPORT, self.REDISUSERNAME, self.REDISPASSWORD,
