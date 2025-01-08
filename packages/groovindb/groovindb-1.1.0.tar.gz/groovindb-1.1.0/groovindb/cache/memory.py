from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import time
from .base import BaseCache

class MemoryCache(BaseCache):
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._default_ttl = ttl

    async def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
            
        item = self._cache[key]
        if self._is_expired(item):
            await self.delete(key)
            return None
            
        return self.deserialize(item['value'])

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if len(self._cache) >= self._max_size:
            self._evict_oldest()

        self._cache[key] = {
            'value': self.serialize(value),
            'expires_at': time.time() + (ttl or self._default_ttl)
        }

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def clear(self) -> None:
        self._cache.clear()

    async def exists(self, key: str) -> bool:
        if key not in self._cache:
            return False
        if self._is_expired(self._cache[key]):
            await self.delete(key)
            return False
        return True

    def _is_expired(self, item: Dict[str, Any]) -> bool:
        return time.time() > item['expires_at']

    def _evict_oldest(self) -> None:
        if not self._cache:
            return
        oldest_key = min(self._cache.keys(), 
                        key=lambda k: self._cache[k]['expires_at'])
        self._cache.pop(oldest_key, None) 