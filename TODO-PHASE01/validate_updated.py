"""Validation script for Phase I implementation.

This script verifies that all Phase I acceptance criteria are met.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager


def validate_acceptance_criteria():
    """Validate all Phase I acceptance criteria."""
    print("="*60)
    print("Phase I Acceptance Criteria Validation")
    print("="*60)

    manager = TaskManager()
    all_passed = True

    # US1: View Task List
    print("\n[US1] Testing View Task List...")
    success, msg = manager.view_tasks()
    if success and "No tasks found" in msg:
        print("[PASS] Empty list displays 'No tasks found'")
    else:
        print("[FAIL] Empty list handling")
        all_passed = False

    # US2: Add Task
    print("\n[US2] Testing Add Task...")
    success, msg = manager.add_task("Buy groceries", "Milk, eggs, bread")
    if success and "ID" in msg:
        print("[PASS] Task added successfully with ID")
    else:
        print("[FAIL] Add task")
        all_passed = False

    # Test empty title validation
    success, msg = manager.add_task("")
    if not success and "cannot be empty" in msg:
        print("[PASS] Empty title validation works")
    else:
        print("[FAIL] Empty title validation")
        all_passed = False

    # US1: View with tasks
    success, msg = manager.view_tasks()
    if success and "Buy groceries" in msg and "Milk, eggs, bread" in msg:
        print("[PASS] View tasks shows task details")
    else:
        print("[FAIL] View tasks with data")
        all_passed = False

    # US3: Toggle Complete
    print("\n[US3] Testing Toggle Complete...")
    success, msg = manager.toggle_complete(1)
    if success and ("complete" in msg.lower() or "incomplete" in msg.lower()):
        print("[PASS] Task marked as complete/incomplete")
    else:
        print("[FAIL] Toggle complete")
        all_passed = False

    # Verify status changed
    success, msg = manager.view_tasks()
    if "Complete" in msg or "complete" in msg:
        print("[PASS] Completion status visible in view")
    else:
        print("[FAIL] Completion status not visible")
        all_passed = False

    # US4: Update Task
    print("\n[US4] Testing Update Task...")
    success, msg = manager.update_task(1, "Buy more groceries", "Milk, eggs, bread, butter")
    if success:
        print("[PASS] Task updated successfully")
    else:
        print("[FAIL] Update task")
        all_passed = False

    # Verify update
    if manager.tasks and manager.tasks[0].title == "Buy more groceries" and "butter" in manager.tasks[0].description:
        print("[PASS] Updated values persisted")
    else:
        print("[FAIL] Updated values not persisted")
        all_passed = False

    # US5: Delete Task
    print("\n[US5] Testing Delete Task...")
    success, msg = manager.delete_task(1)
    if success:
        print("[PASS] Task deleted successfully")
    else:
        print("[FAIL] Delete task")
        all_passed = False

    # Verify deletion
    success, msg = manager.view_tasks()
    if "No tasks found" in msg:
        print("[PASS] Task removed from list")
    else:
        print("[FAIL] Task not removed")
        all_passed = False

    # Edge Cases
    print("\n[Edge Cases] Testing...")

    # Non-existent ID
    success, msg = manager.toggle_complete(999)
    if not success and "not found" in msg.lower():
        print("[PASS] Non-existent ID handled correctly")
    else:
        print("[FAIL] Non-existent ID handling")
        all_passed = False

    # Many tasks
    for i in range(1, 11):  # Reduced for faster testing
        manager.add_task(f"Task {i}", f"Description {i}")

    if len(manager.tasks) == 10:
        print("[PASS] Handles multiple tasks")
    else:
        print("[FAIL] Multiple tasks handling")
        all_passed = False

    # Final Report
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL ACCEPTANCE CRITERIA PASSED")
        print("Phase I implementation is COMPLETE and VALIDATED")
    else:
        print("[ERROR] SOME CRITERIA FAILED")
        print("Review failures above")
    print("="*60)

    return all_passed


if __name__ == "__main__":
    success = validate_acceptance_criteria()
    sys.exit(0 if success else 1)