"""
Singleton TaskManager manages and executes all translation and text extraction tasks.
"""

from threading import Lock
from .Task import Task


class TaskManager:
    _instance = None
    _lock = Lock()

    # Create singleton class
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.task_queue = []
            self.task_ids = []  # tasks ID in the queue
            self.has_task = not (
                len(self.task_queue) == 0
            )  # whether has tasks in the queue

            self.status = False  # queue running status
            self.initialized = False

    def initialize(self) -> bool:
        if not self.initialized:
            self.initialized = True
            return True
        else:
            print("Task Manager is already initialized")
            return False

    def add_task(self, task: Task) -> None:
        task_id = task.task_id
        self.task_queue.append(task)
        self.task_ids.append(task_id)

    def remove_task(self, task_id: int) -> bool:
        # Remove a task based on the id of the task
        try:
            task_index = self.task_ids.index(task_id)
            self.task_queue.pop(task_index)
            self.task_ids.remove(task_id)
            print(f"Successfully removed Task with ID {task_id}.")
            return True
        except Exception as e:
            print(f"Failed to remove Task with ID {task_id}: {e}")
            return False

    def terminate_task(self, task_id: int) -> bool:
        try:
            task_index = self.task_ids.index(task_id)
            results = self.task_queue[task_index].terminate_task()
            if results:
                print(f"Successfully terminated Task with ID {task_id}.")
            return True
        except Exception as e:
            print(f"Failed to terminate Task with ID {task_id}: {e}")
            return False

    def activate_queue(self) -> None:
        print("Executing tasks in the queue...")
        self.status = True

    def get_all_task_id(self) -> list[int]:
        return self.task_ids
