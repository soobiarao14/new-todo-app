"""Integration tests for complete workflows."""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task_manager import TaskManager


class TestCompleteWorkflow(unittest.TestCase):
    """Test complete workflows combining multiple operations."""

    def test_add_view_toggle_update_delete_workflow(self):
        """Test complete workflow: add → view → toggle → update → delete."""
        manager = TaskManager()

        # Step 1: Add task
        success, msg = manager.add_task("Buy groceries", "Milk, eggs, bread")
        self.assertTrue(success)
        self.assertIn("ID 1", msg)

        # Step 2: View tasks
        success, msg = manager.view_tasks()
        self.assertTrue(success)
        self.assertIn("Buy groceries", msg)
        self.assertIn("Incomplete", msg)

        # Step 3: Toggle complete
        success, msg = manager.toggle_complete(1)
        self.assertTrue(success)
        self.assertIn("complete", msg.lower())

        # Verify completion status changed
        success, msg = manager.view_tasks()
        self.assertIn("Complete", msg)

        # Step 4: Update task
        success, msg = manager.update_task(1, "Buy more groceries", "Milk, eggs, bread, butter")
        self.assertTrue(success)

        # Verify update
        success, msg = manager.view_tasks()
        self.assertIn("Buy more groceries", msg)
        self.assertIn("butter", msg)

        # Step 5: Delete task
        success, msg = manager.delete_task(1)
        self.assertTrue(success)

        # Verify deletion
        success, msg = manager.view_tasks()
        self.assertEqual(msg, "No tasks found")

    def test_multiple_tasks_workflow(self):
        """Test managing multiple tasks."""
        manager = TaskManager()

        # Add multiple tasks
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")
        manager.add_task("Task 3", "Description 3")

        # Verify all tasks visible
        success, msg = manager.view_tasks()
        self.assertIn("[1]", msg)
        self.assertIn("[2]", msg)
        self.assertIn("[3]", msg)

        # Toggle some tasks
        manager.toggle_complete(1)
        manager.toggle_complete(3)

        # Verify mixed completion states
        success, msg = manager.view_tasks()
        task_lines = msg.split('\n')
        # Count "Complete" and "Incomplete" occurrences
        complete_count = msg.count("Complete")
        incomplete_count = msg.count("Incomplete")
        self.assertEqual(complete_count, 2)  # Tasks 1 and 3
        self.assertEqual(incomplete_count, 1)  # Task 2

        # Delete middle task
        manager.delete_task(2)

        # Verify correct tasks remain
        success, msg = manager.view_tasks()
        self.assertIn("[1]", msg)
        self.assertNotIn("[2]", msg)
        self.assertIn("[3]", msg)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_very_long_title_and_description(self):
        """Test with very long titles and descriptions (1000+ chars)."""
        manager = TaskManager()

        long_title = "A" * 1000
        long_description = "B" * 1000

        success, msg = manager.add_task(long_title, long_description)
        self.assertTrue(success)

        # Verify task was stored correctly
        self.assertEqual(manager.tasks[0].title, long_title)
        self.assertEqual(manager.tasks[0].description, long_description)

    def test_many_tasks(self):
        """Test with many tasks (100+)."""
        manager = TaskManager()

        # Add 100 tasks
        for i in range(1, 101):
            success, msg = manager.add_task(f"Task {i}", f"Description {i}")
            self.assertTrue(success)

        # Verify all tasks added
        self.assertEqual(len(manager.tasks), 100)

        # Verify IDs are sequential
        for i, task in enumerate(manager.tasks, start=1):
            self.assertEqual(task.id, i)

        # Verify next_id is correct
        self.assertEqual(manager.next_id, 101)

        # Test operations still work correctly
        success, msg = manager.toggle_complete(50)
        self.assertTrue(success)
        self.assertTrue(manager.tasks[49].completed)

    def test_delete_and_add_new_tasks(self):
        """Test that IDs are not reused after deletion."""
        manager = TaskManager()

        # Add 3 tasks
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")

        # Delete task 2
        manager.delete_task(2)

        # Add new task - should get ID 4, not 2
        success, msg = manager.add_task("Task 4")
        self.assertIn("ID 4", msg)

        # Verify no task has ID 2
        task_ids = [task.id for task in manager.tasks]
        self.assertNotIn(2, task_ids)
        self.assertIn(1, task_ids)
        self.assertIn(3, task_ids)
        self.assertIn(4, task_ids)


if __name__ == '__main__':
    unittest.main()
