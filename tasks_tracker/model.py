from datetime import datetime
from typing import Optional

from nanoid import generate

from tasks_tracker.configs import DB_DATE_FORMAT
from tasks_tracker.typing import Priority, Status


class Task:
    def __init__(
        self,
        id: Optional[str],
        title: str,
        status: str,
        priority: str,
        description: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
    ) -> None:
        self.id = id if id else generate("1234567890abcdef", 10)
        self.title = title
        self.status = status if status else Status.NOT_STARTED.value
        self.priority = priority if priority else Priority.LOW.value
        self.description = description
        self.start_date = start_date if start_date else datetime.now().strftime(DB_DATE_FORMAT)
        self.end_date = end_date

    def __repr__(self) -> str:
        return f"({self.title}, {self.status}, {self.priority}, {self.description}, {self.start_date}, {self.end_date})"
