from enum import Enum


class Status(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    DONE = "done"


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
