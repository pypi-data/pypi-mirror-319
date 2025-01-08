from typing import Any, Optional
from pymemcache.client.base import Client
from .base import BaseCache

class MemcachedCache(BaseCache):
    def __init__(self, host: str = 'localhost', 
                 port: int = 11211,
                 ttl: int = 300):
        self._client = Client((host, port))
        self._default_ttl = ttl

    async def get(self, key: str) -> Optional[Any]:
        value = self._client.get(key)
        if value is None:
            return None
        return self.deserialize(value.decode())

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._client.set(
            key,
            self.serialize(value).encode(),
            expire=(ttl or self._default_ttl)
        )

    async def delete(self, key: str) -> None:
        self._client.delete(key)

    async def clear(self) -> None:
        self._client.flush_all()

    async def exists(self, key: str) -> bool:
        return self._client.get(key) is not None 