from threading import Lock
from typing import Any, Dict, TypeVar, Generic
import copy

T = TypeVar('T')

class Context(Dict[str, Any], Generic[T]):
    """Thread-safe dictionary that stores data shared between tasks."""
    def __init__(self, initial_data: Dict[str, Any] = None):
        super().__init__()
        self._lock: Lock = Lock()
        if initial_data is not None:
            self.update(initial_data)
        
    def __getitem__(self, key: str) -> T:
        self._validate_key(key)
        with self._lock:
            return copy.deepcopy(super().__getitem__(key))

    def __setitem__(self, key: str, value: Any) -> None:
        self._validate_key(key)
        with self._lock:
            super().__setitem__(key, copy.deepcopy(value))

    def __delitem__(self, key: str) -> None:
        self._validate_key(key)
        with self._lock:
            super().__delitem__(key)

    def clear(self) -> None:
        with self._lock:
            super().clear()

    def update(self, other: Dict[str, Any]) -> None:
        with self._lock:
            super().update(copy.deepcopy(other))

    def get(self, key: str, default: Any = None) -> T:
        self._validate_key(key)
        with self._lock:
            return copy.deepcopy(super().get(key, default))

    def __contains__(self, key: object) -> bool:
        self._validate_key(key)
        with self._lock:
            return super().__contains__(key)

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

    def copy(self) -> 'Context[T]':
        """Create a deep copy of the context."""
        with self._lock:
            return Context(copy.deepcopy(dict(self)))
