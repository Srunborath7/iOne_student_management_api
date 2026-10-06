from dataclasses import dataclass

@dataclass
class Teacher:
    id: int
    name: str
    gender: str
    age: int
    phone: str
    email: str
    address: str | None = None
    note: str | None = None
    user_id: int | None = None
