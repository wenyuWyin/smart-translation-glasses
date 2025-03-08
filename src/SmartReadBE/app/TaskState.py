from enum import Enum


class TaskState(Enum):
    IDLE = 1
    QUEUED = 2
    IMAGE_RECEIVED = 3
    TEXT_EXTRACTED = 4
    TRANSLATED = 5
    ERROR = 6
    
