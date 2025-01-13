"""
Singleton TaskManager manages and executes all translation and text extraction tasks.
"""
import uuid
from threading import Lock
from SmartReadBE.app.Task import Task

class TaskManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.taskQueue = []
            self.taskIDs = [] # tasks ID in the queue
            self.hasTask = not (len(self.taskQueue) == 0) # whether has tasks in the queue

            self.status = False # queue running status
            self.initialized = False

    def initialize(self) -> bool:
        if not self.initialized:
            print("Initializing Task Manager")
            self.initialized = True
            return True
        else:
            print("Task Manager is already initialized")
            return False

    def add_task(self, task: Task) -> None:
        task_id = task.task_id
        self.taskQueue.append(task)
        self.taskIDs.append(task_id)
        print(f"Task {task.task_type} with ID {task_id} initialized.")
    
    def remove_task(self, task_id: int) -> bool:
        try:
            task_index = self.taskIDs.index(task_id)
            self.taskQueue.pop(task_index)
            self.taskIDs.remove(task_id)
            print(f"Successfully removed Task with ID {task_id}.")
            return True
        except Exception as e:
            print(f"Failed to remove Task with ID {task_id}: {e}")
            return False
        
    def terminate_task(self, task_id: int) -> bool:
        try:
            task_index = self.taskIDs.index(task_id)
            results = self.taskQueue[task_index].terminate_task()
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
        return self.taskIDs


if __name__ == "__main__":
    # initialize task manager
    manager = TaskManager()
    manager.initialize()

    # initialize text extraction and translation module

    # create task and initialize

    # add task to the queue

    manager.activate_queue()
    while manager.status:
        if manager.hasTask:
            task = manager.taskQueue[0]
            # If task is initialized and ready to be executed
            if task.get_status():
                success = task.execute_task()
                if success:
                    print(f"Task {task.task_id} executed successfully.")
                    manager.remove_task(task.task_id)
                else:
                    print(f"Task {task.task_id} failed to execute.")
            else:
                print(f"Task {task.task_id} is not active and will be skipped.")
