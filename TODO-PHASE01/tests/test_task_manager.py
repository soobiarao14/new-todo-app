"""Unit tests for TaskManager class."""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task_manager import TaskManager
from task import Task


class TestTaskManagerInit(unittest.TestCase):
    """Test cases for TaskManager initialization."""

    def test_init_empty_list(self):
        """Test TaskManager initializes with empty task list."""
        manager = TaskManager()
        self.assertEqual(len(manager.tasks), 0)
        self.assertEqual(manager.next_id, 1)


class TestViewTasks(unittest.TestCase):
    """Test cases for view_tasks method (User Story 1)."""

    def setUp(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_view_tasks_empty_list(self):
        """Test viewing tasks when list is empty."""
        success, message = self.manager.view_tasks()
        self.assertTrue(success)
        self.assertEqual(message, "No tasks found")

    def test_view_tasks_single_task(self):
        """Test viewing tasks with a single task."""
        self.manager.add_task("Buy groceries", "Milk, eggs, bread")
        success, message = self.manager.view_tasks()

        self.assertTrue(success)
        self.assertIn("[1]", message)
        self.assertIn("Buy groceries", message)
        self.assertIn("Milk, eggs, bread", message)
        self.assertIn("Incomplete", message)

    def test_view_tasks_multiple_tasks(self):
        """Test viewing tasks with multiple tasks (complete and incomplete)."""
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        self.manager.tasks[0].completed = True  # Mark first task complete

        success, message = self.manager.view_tasks()

        self.assertTrue(success)
        self.assertIn("[1]", message)
        self.assertIn("[2]", message)
        self.assertIn("Task 1", message)
        self.assertIn("Task 2", message)
        self.assertIn("Complete", message)
        self.assertIn("Incomplete", message)


class TestAddTask(unittest.TestCase):
    """Test cases for add_task method (User Story 2)."""

    def setUp(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_add_task_with_valid_title(self):
        """Test adding a task with valid title."""
        success, message = self.manager.add_task("Buy groceries")

        self.assertTrue(success)
        self.assertIn("ID 1", message)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "Buy groceries")
        self.assertEqual(self.manager.tasks[0].id, 1)
        self.assertEqual(self.manager.next_id, 2)

    def test_add_task_with_title_and_description(self):
        """Test adding a task with both title and description."""
        success, message = self.manager.add_task("Call dentist", "Schedule annual checkup")

        self.assertTrue(success)
        self.assertEqual(self.manager.tasks[0].title, "Call dentist")
        self.assertEqual(self.manager.tasks[0].description, "Schedule annual checkup")

    def test_add_task_with_empty_title(self):
        """Test adding a task with empty title (should fail)."""
        success, message = self.manager.add_task("")

        self.assertFalse(success)
        self.assertEqual(message, "Task title cannot be empty")
        self.assertEqual(len(self.manager.tasks), 0)

    def test_add_task_with_whitespace_only_title(self):
        """Test adding a task with whitespace-only title (should fail)."""
        success, message = self.manager.add_task("   ")

        self.assertFalse(success)
        self.assertEqual(message, "Task title cannot be empty")
        self.assertEqual(len(self.manager.tasks), 0)

    def test_next_id_increments_correctly(self):
        """Test that next_id increments correctly after adding tasks."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")

        self.assertEqual(self.manager.tasks[0].id, 1)
        self.assertEqual(self.manager.tasks[1].id, 2)
        self.assertEqual(self.manager.tasks[2].id, 3)
        self.assertEqual(self.manager.next_id, 4)


class TestToggleComplete(unittest.TestCase):
    """Test cases for toggle_complete method (User Story 3)."""

    def setUp(self):
        """Set up TaskManager with a test task."""
        self.manager = TaskManager()
        self.manager.add_task("Test task", "Test description")

    def test_toggle_complete_with_valid_id(self):
        """Test toggling completion with valid task ID."""
        success, message = self.manager.toggle_complete(1)

        self.assertTrue(success)
        self.assertIn("complete", message.lower())
        self.assertTrue(self.manager.tasks[0].completed)

    def test_toggle_from_false_to_true(self):
        """Test toggling from incomplete to complete."""
        self.assertEqual(self.manager.tasks[0].completed, False)

        success, message = self.manager.toggle_complete(1)

        self.assertTrue(success)
        self.assertEqual(message, "Task marked as complete")
        self.assertTrue(self.manager.tasks[0].completed)

    def test_toggle_from_true_to_false(self):
        """Test toggling from complete to incomplete."""
        self.manager.tasks[0].completed = True

        success, message = self.manager.toggle_complete(1)

        self.assertTrue(success)
        self.assertEqual(message, "Task marked as incomplete")
        self.assertFalse(self.manager.tasks[0].completed)

    def test_toggle_with_non_existent_id(self):
        """Test toggling with non-existent task ID."""
        success, message = self.manager.toggle_complete(999)

        self.assertFalse(success)
        self.assertEqual(message, "Task ID not found")

    def test_toggle_with_empty_task_list(self):
        """Test toggling when task list is empty."""
        self.manager.tasks = []

        success, message = self.manager.toggle_complete(1)

        self.assertFalse(success)
        self.assertEqual(message, "Task ID not found")


class TestUpdateTask(unittest.TestCase):
    """Test cases for update_task method (User Story 4)."""

    def setUp(self):
        """Set up TaskManager with a test task."""
        self.manager = TaskManager()
        self.manager.add_task("Old Title", "Old Description")

    def test_update_task_with_valid_id_and_title(self):
        """Test updating task with valid ID and new title."""
        success, message = self.manager.update_task(1, "New Title")

        self.assertTrue(success)
        self.assertEqual(message, "Task updated successfully")
        self.assertEqual(self.manager.tasks[0].title, "New Title")

    def test_update_task_with_title_and_description(self):
        """Test updating both title and description."""
        success, message = self.manager.update_task(1, "New Title", "New Description")

        self.assertTrue(success)
        self.assertEqual(self.manager.tasks[0].title, "New Title")
        self.assertEqual(self.manager.tasks[0].description, "New Description")

    def test_update_task_with_empty_title(self):
        """Test updating with empty title (should fail)."""
        success, message = self.manager.update_task(1, "")

        self.assertFalse(success)
        self.assertEqual(message, "Task title cannot be empty")
        self.assertEqual(self.manager.tasks[0].title, "Old Title")  # Unchanged

    def test_update_task_with_non_existent_id(self):
        """Test updating with non-existent task ID."""
        success, message = self.manager.update_task(999, "New Title")

        self.assertFalse(success)
        self.assertEqual(message, "Task ID not found")

    def test_update_task_with_empty_description(self):
        """Test updating with empty description (should succeed)."""
        success, message = self.manager.update_task(1, "New Title", "")

        self.assertTrue(success)
        self.assertEqual(self.manager.tasks[0].description, "")


class TestDeleteTask(unittest.TestCase):
    """Test cases for delete_task method (User Story 5)."""

    def setUp(self):
        """Set up TaskManager with test tasks."""
        self.manager = TaskManager()
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        self.manager.add_task("Task 3", "Description 3")

    def test_delete_task_with_valid_id(self):
        """Test deleting task with valid ID."""
        success, message = self.manager.delete_task(2)

        self.assertTrue(success)
        self.assertEqual(message, "Task deleted successfully")
        self.assertEqual(len(self.manager.tasks), 2)
        # Verify task 2 is gone
        task_ids = [task.id for task in self.manager.tasks]
        self.assertNotIn(2, task_ids)
        self.assertIn(1, task_ids)
        self.assertIn(3, task_ids)

    def test_delete_task_with_non_existent_id(self):
        """Test deleting with non-existent task ID."""
        success, message = self.manager.delete_task(999)

        self.assertFalse(success)
        self.assertEqual(message, "Task ID not found")
        self.assertEqual(len(self.manager.tasks), 3)  # Unchanged

    def test_delete_task_with_empty_list(self):
        """Test deleting when task list is empty."""
        self.manager.tasks = []

        success, message = self.manager.delete_task(1)

        self.assertFalse(success)
        self.assertEqual(message, "Task ID not found")

    def test_next_id_does_not_decrement_after_deletion(self):
        """Test that next_id does NOT decrement after deletion."""
        original_next_id = self.manager.next_id
        self.manager.delete_task(1)

        self.assertEqual(self.manager.next_id, original_next_id)


if __name__ == '__main__':
    unittest.main()
