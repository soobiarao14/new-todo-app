"""Unit tests for Task class."""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task import Task


class TestTask(unittest.TestCase):
    """Test cases for Task class initialization and attributes."""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(task_id=1, title="Buy groceries", description="Milk, eggs, bread", completed=False)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")
        self.assertEqual(task.completed, False)

    def test_task_creation_with_defaults(self):
        """Test creating a task with default description and completed status."""
        task = Task(task_id=2, title="Call dentist")

        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Call dentist")
        self.assertEqual(task.description, "")
        self.assertEqual(task.completed, False)

    def test_task_creation_completed(self):
        """Test creating a task that is already completed."""
        task = Task(task_id=3, title="Submit report", description="Q4 summary", completed=True)

        self.assertEqual(task.id, 3)
        self.assertEqual(task.completed, True)

    def test_task_repr(self):
        """Test string representation of Task."""
        task = Task(task_id=1, title="Test task", description="Test desc", completed=False)
        repr_str = repr(task)

        self.assertIn("Task(", repr_str)
        self.assertIn("id=1", repr_str)
        self.assertIn("title='Test task'", repr_str)


if __name__ == '__main__':
    unittest.main()
