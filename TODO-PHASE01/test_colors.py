#!/usr/bin/env python3
"""Test script to verify color functionality in the todo app."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task import Task
from task_manager import TaskManager
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def test_colors():
    print("Testing color functionality...\n")

    # Create a task manager
    tm = TaskManager()

    # Add some test tasks with different priorities
    print("Adding test tasks...")
    success, msg = tm.add_task("High priority task", "This is a high priority task", priority="High")
    print(f"Added high priority task: {msg}")

    success, msg = tm.add_task("Medium priority task", "This is a medium priority task", priority="Medium")
    print(f"Added medium priority task: {msg}")

    success, msg = tm.add_task("Low priority task", "This is a low priority task", priority="Low")
    print(f"Added low priority task: {msg}")

    success, msg = tm.add_task("Normal task", "This is a normal task", priority=None)
    print(f"Added normal task: {msg}")

    # Add a completed task
    success, msg = tm.add_task("Completed task", "This task is completed", priority="High")
    print(f"Added completed task: {msg}")

    success, msg = tm.toggle_complete(5)  # Mark the last task as completed
    print(f"Toggled completion: {msg}")

    print("\n" + "="*50)
    # Test colored task display
    print("Testing individual task colors:")
    for task in tm.tasks:
        print(task.colored_str())

    print("\n" + "="*50)
    print("Testing TaskManager view_tasks with colors:")
    success, message = tm.view_tasks()
    print(message)

    print("\n" + "="*50)
    print("Testing colored upcoming deadlines:")
    colored_deadlines = tm.get_colored_upcoming_deadlines()
    print(colored_deadlines)

    print("\nColor functionality test completed successfully!")

if __name__ == "__main__":
    test_colors()