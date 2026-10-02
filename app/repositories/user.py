from app.repositories.base import InMemoryRepository
from app.domain.user.model import User
from app.data.users_seed import SEED_USER
from app.core.security import hash_password

class UserRepository(InMemoryRepository):
    def __init__(self, seed: list[dict] | None = None):
        super().__init__()

        for row in seed or []:
            data = {**row, "password": hash_password(row["password"])}
            user = User(**data)
            self._items[user.id] = user

    def find_by_username(self, username: str) -> User | None:
        return next(
            (
                user
                for user in self._items.values()
                if user.username.lower() == username.lower()
            ),
            None
        )

    def next_id(self) -> int:
        return max(self._items, default=0) + 1

user_repo = UserRepository(SEED_USER)