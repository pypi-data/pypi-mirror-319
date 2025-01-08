from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
import json
from datetime import datetime, date
from decimal import Decimal

class BaseCache(ABC):
    """Clase base para implementaciones de caché"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Guarda un valor en el caché"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Elimina una clave del caché"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Limpia todo el caché"""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe"""
        pass

    def serialize(self, value: Any) -> str:
        """Serializa un valor para almacenamiento"""
        def default(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            if isinstance(obj, Decimal):
                return str(obj)
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

        return json.dumps(value, default=default)

    def deserialize(self, value: str) -> Any:
        """Deserializa un valor almacenado"""
        def object_hook(dct):
            for k, v in dct.items():
                if isinstance(v, str):
                    # Intentar parsear fechas ISO
                    try:
                        if 'T' in v:  # Probable datetime
                            dct[k] = datetime.fromisoformat(v)
                        elif '-' in v:  # Probable date
                            dct[k] = date.fromisoformat(v)
                    except ValueError:
                        pass
            return dct

        return json.loads(value, object_hook=object_hook)

    def build_key(self, key: str, prefix: Optional[str] = None) -> str:
        """Construye una clave con prefijo opcional"""
        if prefix:
            return f"{prefix}:{key}"
        return key 