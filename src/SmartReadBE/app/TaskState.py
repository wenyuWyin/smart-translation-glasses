from enum import Enum


class TaskState(Enum):
    IDLE = 1
    IMAGE_RECEIVED = 2
    TEXT_EXTRACTED = 3
    TRANSLATED = 4
    ERROR = 5
