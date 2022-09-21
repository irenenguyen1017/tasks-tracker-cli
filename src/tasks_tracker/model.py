from datetime import datetime
from typing import Optional

from nanoid import generate


class Task:
    def __init__(
        self,
        id: Optional[str],
        title: Optional[str],
        status: Optional[str],
        priority: Optional[str],
        description: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
    ) -> None:
        self.id = id if id else generate("1234567890abcdef", 10)
        self.title = title
        self.status = status
        self.priority = priority
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self) -> str:
        return f"({self.title}, {self.status}, {self.priority}, {self.description}, {self.start_date}, {self.end_date})"
