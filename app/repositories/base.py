from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(self):
        self._items: dict[int, T] = {}

    def list_all(self) -> list[T]:
        return list(self._items.values())

    def get(self, item_id: int) -> T | None:
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