from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    URL: str
    REDISHOST: str
    REDISPORT: int
    REDISPASSWORD: str

    def get_url(self):
        return self.URL

    def get_redis_config(self):
        return self.REDISHOST, self.REDISPORT, self.REDISPASSWORD


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
