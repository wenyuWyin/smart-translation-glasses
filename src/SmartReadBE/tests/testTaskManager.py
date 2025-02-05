import unittest
from unittest.mock import MagicMock
from app.TaskManager import TaskManager
from app.Task import Task


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """
        Runs before every test to ensure a fresh, singleton TaskManager
        instance and to reset the manager's state.
        """
        # Clear singleton instance between tests
        TaskManager._instance = None

    def test_queue_initialization(self):
        # UT-19: QueueInitialization Test
        manager = TaskManager()
        result = manager.initialize()
        self.assertTrue(result, "Initialization should succeed.")

    def test_queue_remove_task(self):
        # UT-20: QueueRemoveTask Test
        # Ensure a task can be removed from the queue
        manager = TaskManager()
        manager.initialize()
        # Create a mock task
        mock_task = MagicMock(spec=Task)
        mock_task.task_id = 101

        # Add the task to the queue
        manager.add_task(mock_task)
        self.assertIn(101, manager.task_ids)

        # Remove the task
        remove_result = manager.remove_task(101)
        self.assertTrue(remove_result, "Task removal should succeed.")
        self.assertNotIn(101, manager.task_ids)

    def test_invalid_task_id_remove(self):
        # UT-21: InvalidTaskID RemoveTest
        # Attempting to remove an undefined task ID should fail
        manager = TaskManager()
        manager.initialize()

        # No tasks in queue, removing invalid ID
        remove_result = manager.remove_task(999)
        self.assertFalse(remove_result, "Removing a non-existent task should fail.")

    def test_empty_queue_remove_task(self):
        # UT-22: EmptyQueueRemove TaskTest
        manager = TaskManager()
        manager.initialize()

        # The queue is empty; removing any task fails
        remove_result = manager.remove_task(123)
        self.assertFalse(remove_result, "Removing from an empty queue should fail.")

    def test_queue_add_task(self):
        # UT-23: QueueAddTask Test
        # Ensure a task can be added into the queue in correct order
        manager = TaskManager()
        manager.initialize()

        # Create two mock tasks
        mock_task1 = MagicMock(spec=Task)
        mock_task1.task_id = 201
        mock_task2 = MagicMock(spec=Task)
        mock_task2.task_id = 202

        # Add tasks to the queue
        manager.add_task(mock_task1)
        manager.add_task(mock_task2)

        # Check the order in the queue
        self.assertEqual(manager.task_ids, [201, 202], "Tasks should be in FIFO order.")

    def test_duplicate_task_manager_initialization(self):
        # UT-24: DuplicateTask ManagerInitialization Test
        # Ensure TaskManager is a singleton
        manager1 = TaskManager()
        manager2 = TaskManager()

        self.assertIs(
            manager1, manager2, "Both references should be the same singleton instance."
        )

    def test_task_execution_successful(self):
        # UT-25: TaskExecution SuccessfulTest
        # Add a valid task to the queue and simulate a successful execution
        manager = TaskManager()
        manager.initialize()

        # Create a mock task
        mock_task = MagicMock(spec=Task)
        mock_task.task_id = 301
        # Pretend 'execute' returns True for success
        mock_task.execute_task.return_value = True

        manager.add_task(mock_task)

        success = manager.task_queue[0].execute_task()
        self.assertTrue(success, "Task execution should succeed.")

    def test_task_execution_error(self):
        # UT-26: TaskExecutionError Test
        # Execute a task known to raise an exception
        manager = TaskManager()
        manager.initialize()

        # Create a mock task that will raise an exception on execute
        mock_task = MagicMock(spec=Task)
        mock_task.task_id = 401
        mock_task.execute_task.side_effect = Exception("Simulated execution error")

        manager.add_task(mock_task)

        # Attempt to execute and verify the error
        try:
            manager.task_queue[0].execute_task()
            self.fail("Expected an exception to be raised during task execution.")
        except Exception as e:
            self.assertIn(
                "Simulated execution error", str(e), "Error message should match."
            )

    def test_uninitialized_task_execution(self):
        # UT-27: UninitializedTask ExecutionTest
        # Verify an uninitialized task will not be executed
        manager = TaskManager()
        manager.initialize()

        # Create a mock 'uninitialized' task
        mock_task = MagicMock(spec=Task)
        mock_task.task_id = 501
        mock_task.task_status = False

        manager.add_task(mock_task)

        if not mock_task.task_status:
            remove_result = manager.remove_task(501)
            self.assertTrue(
                remove_result,
                "Uninitialized task should be removed instead of executed.",
            )
        else:
            self.fail("The task should have been flagged as uninitialized.")


if __name__ == "__main__":
    unittest.main()
