import redis
import datetime
from typing import Any, Union

pool = redis.ConnectionPool()

class RedisClient(object):

    def __init__(self, *args, **kwargs) -> None:
        self.client = redis.Redis(*args, **kwargs)

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.client, __name)

class RedisBase:

    _prefix_key = "prefix"
    _db = 0

    def __init__(self, client:  Union[RedisClient, redis.Redis]):
        self._client = client

    @property
    def client(self):
        return self._client