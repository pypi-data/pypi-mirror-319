from typing import Any, Optional
import redis
from .base import BaseCache

class RedisCache(BaseCache):
    def __init__(self, host: str = 'localhost', 
                 port: int = 6379, 
                 db: int = 0,
                 password: Optional[str] = None,
                 prefix: str = 'groovindb:',
                 ttl: int = 300):
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        self._prefix = prefix
        self._default_ttl = ttl

    async def get(self, key: str) -> Optional[Any]:
        key = self.build_key(key, self._prefix)
        value = self._redis.get(key)
        if value is None:
            return None
        return self.deserialize(value)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        key = self.build_key(key, self._prefix)
        self._redis.set(
            key,
            self.serialize(value),
            ex=(ttl or self._default_ttl)
        )

    async def delete(self, key: str) -> None:
        key = self.build_key(key, self._prefix)
        self._redis.delete(key)

    async def clear(self) -> None:
        pattern = f"{self._prefix}*"
        keys = self._redis.keys(pattern)
        if keys:
            self._redis.delete(*keys)

    async def exists(self, key: str) -> bool:
        key = self.build_key(key, self._prefix)
        return bool(self._redis.exists(key)) 