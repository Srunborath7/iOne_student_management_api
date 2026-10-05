from dataclasses import dataclass

@dataclass
class Course:
    id: int
    name: str
    status: bool
    description: str