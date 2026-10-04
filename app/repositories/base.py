from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """
    Abstract Interface for generic repository pattern (OOP - Abstraction).
    """

    @abstractmethod
    def list_all(self) -> List[T]:
        """Retrieve all items."""
        pass

    @abstractmethod
    def get(self, item_id: int) -> Optional[T]:
        """Retrieve an item by ID."""
        pass

    @abstractmethod
    def add(self, item: T) -> T:
        """Add a new item."""
        pass

    @abstractmethod
    def update(self, item_id: int, item: T) -> T:
        """Update an existing item."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Delete an item by ID."""
        pass


class InMemoryRepository(IRepository[T]):
    """
    In-memory implementation of IRepository (OOP - Encapsulation & Inheritance).
    """

    def __init__(self):
        self._items: dict[int, T] = {}

    def list_all(self) -> List[T]:
        return list(self._items.values())

    def get(self, item_id: int) -> Optional[T]:
        return self._items.get(item_id)

    def add(self, item: T) -> T:
        self._items[item.id] = item
        return item

    def update(self, item_id: int, item: T) -> T:
        self._items[item_id] = item
        return item

    def delete(self, item_id: int) -> bool:
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True