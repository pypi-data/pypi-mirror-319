from .base import BaseCache
from .memory import MemoryCache
from .redis import RedisCache
from .memcached import MemcachedCache

def get_cache(config: dict) -> BaseCache:
    """Factory para crear la instancia de caché apropiada"""
    cache_type = config.get('type', 'memory')
    
    if cache_type == 'memory':
        return MemoryCache(
            max_size=config.get('max_size', 1000),
            ttl=config.get('ttl', 300)
        )
    elif cache_type == 'redis':
        return RedisCache(
            host=config.get('host', 'localhost'),
            port=config.get('port', 6379),
            db=config.get('db', 0),
            password=config.get('password'),
            prefix=config.get('key_prefix', 'groovindb:'),
            ttl=config.get('ttl', 300)
        )
    elif cache_type == 'memcached':
        return MemcachedCache(
            host=config.get('host', 'localhost'),
            port=config.get('port', 11211),
            ttl=config.get('ttl', 300)
        )
    else:
        raise ValueError(f"Tipo de caché no soportado: {cache_type}")

__all__ = ['BaseCache', 'MemoryCache', 'RedisCache', 'MemcachedCache', 'get_cache'] 