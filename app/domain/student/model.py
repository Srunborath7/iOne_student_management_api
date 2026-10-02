from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    email: str
    phone: str
    age: int
    major: str | None = None