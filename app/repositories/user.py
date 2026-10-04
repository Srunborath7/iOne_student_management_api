from abc import abstractmethod
from typing import List, Optional
from app.repositories.base import InMemoryRepository, IRepository
from app.domain.user.model import User
from app.data.users_seed import SEED_USER
from app.core.security import password_hasher, IPasswordHasher


class IUserRepository(IRepository[User]):
    """
    Interface specific to User domain repository (OOP - Interface Segregation).
    """

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def next_id(self) -> int:
        pass


class UserRepository(InMemoryRepository[User], IUserRepository):
    """
    Concrete UserRepository implementing IUserRepository and InMemoryRepository.
    Uses Dependency Injection for password hashing.
    """

    def __init__(
        self,
        seed: Optional[List[dict]] = None,
        hasher: Optional[IPasswordHasher] = None,
    ):
        super().__init__()
        self._hasher = hasher or password_hasher

        for row in seed or []:
            data = {**row, "password": self._hasher.hash(row["password"])}
            user = User(**data)
            self._items[user.id] = user

    def find_by_username(self, username: str) -> Optional[User]:
        clean_user = username.strip().lower()
        return next(
            (
                user
                for user in self._items.values()
                if user.username.lower() == clean_user
            ),
            None,
        )

    def next_id(self) -> int:
        return max(self._items.keys(), default=0) + 1


# Default repository singleton
user_repo: IUserRepository = UserRepository(SEED_USER)