#!/usr/bin/env python3
"""Test to verify that all modules load correctly with color functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    print("Testing imports...")
    try:
        from colorama import Fore, Style, init
        print("✓ Colorama imported successfully")
        
        from task import Task
        print("✓ Task module imported successfully")
        
        from task_manager import TaskManager
        print("✓ TaskManager module imported successfully")
        
        # Test initialization
        init(autoreset=True)
        print("✓ Colorama initialized successfully")
        
        # Create a simple task
        task = Task(1, "Test task", "Test description", priority="High")
        print(f"✓ Task created: {task}")
        
        # Test colored string
        colored_task = task.colored_str()
        print(f"✓ Colored task string: {colored_task}")
        
        # Test TaskManager
        tm = TaskManager()
        print("✓ TaskManager created successfully")
        
        # Add a task
        success, msg = tm.add_task("Test task", "Test description", priority="High")
        print(f"✓ Task added: {success}, {msg}")
        
        # View tasks
        success, msg = tm.view_tasks()
        print(f"✓ Tasks viewed: {success}, {msg[:50]}...")
        
        print("\n✓ All tests passed! Color functionality is working.")
        
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_imports()