# """Main CLI application for Phase I Todo App.

# This module provides the command-line interface for interacting with
# the todo application. It displays a menu, handles user input, and
# calls TaskManager methods to perform operations.
# """

# import sys
# import os

# # Add current directory to path for imports
# sys.path.insert(0, os.path.dirname(__file__))

# from task_manager import TaskManager


# def display_menu():
#     """Display the main menu."""
#     print("\n===== Todo App Menu =====")
#     print("1. View all tasks")
#     print("2. Add new task")
#     print("3. Update task")
#     print("4. Delete task")
#     print("5. Toggle task complete/incomplete")
#     print("6. Exit")
#     print("==========================")


# def get_menu_choice():
#     """Get and validate menu choice from user.

#     Returns:
#         int: Valid menu choice (1-6), or None if invalid
#     """
#     try:
#         choice = int(input("Enter your choice (1-6): "))
#         if 1 <= choice <= 6:
#             return choice
#         else:
#             print("Invalid choice. Please enter a number between 1 and 6.")
#             return None
#     except ValueError:
#         print("Invalid input. Please enter a number between 1 and 6.")
#         return None


# def get_task_id():
#     """Get and validate task ID from user.

#     Returns:
#         int: Task ID, or None if invalid
#     """
#     try:
#         task_id = int(input("Enter task ID: "))
#         return task_id
#     except ValueError:
#         print("Invalid input. Please enter a valid task ID.")
#         return None


# def handle_view_tasks(manager):
#     """Handle viewing all tasks.

#     Args:
#         manager: TaskManager instance
#     """
#     print("\n--- All Tasks ---")
#     success, message = manager.view_tasks()
#     print(message)


# def handle_add_task(manager):
#     """Handle adding a new task.

#     Args:
#         manager: TaskManager instance
#     """
#     print("\n--- Add New Task ---")
#     title = input("Enter task title: ")
#     description = input("Enter task description (optional, press Enter to skip): ")

#     success, message = manager.add_task(title, description)
#     print(message)


# def handle_update_task(manager):
#     """Handle updating an existing task.

#     Args:
#         manager: TaskManager instance
#     """
#     print("\n--- Update Task ---")
#     task_id = get_task_id()

#     if task_id is None:
#         return

#     new_title = input("Enter new title: ")
#     new_description = input("Enter new description (optional, press Enter to skip): ")

#     success, message = manager.update_task(task_id, new_title, new_description)
#     print(message)


# def handle_delete_task(manager):
#     """Handle deleting a task.

#     Args:
#         manager: TaskManager instance
#     """
#     print("\n--- Delete Task ---")
#     task_id = get_task_id()

#     if task_id is None:
#         return

#     success, message = manager.delete_task(task_id)
#     print(message)


# def handle_toggle_complete(manager):
#     """Handle toggling task completion status.

#     Args:
#         manager: TaskManager instance
#     """
#     print("\n--- Toggle Task Complete/Incomplete ---")
#     task_id = get_task_id()

#     if task_id is None:
#         return

#     success, message = manager.toggle_complete(task_id)
#     print(message)


# def main():
#     """Main application loop."""
#     print("\n" + "="*50)
#     print("Welcome to Todo CLI - Phase I")
#     print("In-memory task management (data lost on exit)")
#     print("="*50)

#     manager = TaskManager()

#     while True:
#         display_menu()
#         choice = get_menu_choice()

#         if choice is None:
#             continue

#         if choice == 1:
#             handle_view_tasks(manager)
#         elif choice == 2:
#             handle_add_task(manager)
#         elif choice == 3:
#             handle_update_task(manager)
#         elif choice == 4:
#             handle_delete_task(manager)
#         elif choice == 5:
#             handle_toggle_complete(manager)
#         elif choice == 6:
#             print("\nGoodbye!")
#             break


# if __name__ == "__main__":
#     main()




"""Main CLI application for Phase I Todo App.

This module provides the command-line interface for interacting with
the todo application. It displays a menu, handles user input, and
calls TaskManager methods to perform operations.
"""

import sys
import os
from datetime import datetime, timedelta
import json
from typing import Optional, List
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from task_manager import TaskManager


def display_menu():
    """Display the main menu."""
    print(f"\n{Fore.CYAN}" + "="*50)
    print(f"{Fore.MAGENTA} " * 15 + "📝 TODO APP MENU 📝")
    print(f"{Fore.CYAN}" + "="*50)
    print(f"{Fore.LIGHTYELLOW_EX}1.  View all tasks")
    print(f"{Fore.LIGHTGREEN_EX}2.  Add new task")
    print(f"{Fore.LIGHTCYAN_EX}3.  Update task")
    print(f"{Fore.LIGHTRED_EX}4.  Delete task")
    print(f"{Fore.LIGHTBLUE_EX}5.  Toggle task complete/incomplete")
    print(f"{Fore.RED}6.  Set task priority")
    print(f"{Fore.YELLOW}7.  Add tags/categories to task")
    print(f"{Fore.GREEN}8.  Search tasks")
    print(f"{Fore.BLUE}9.  Filter tasks")
    print(f"{Fore.MAGENTA}10. Sort tasks")
    print(f"{Fore.CYAN}11. Set due date & reminder")
    print(f"{Fore.LIGHTMAGENTA_EX}12. Add recurring task")
    print(f"{Fore.LIGHTWHITE_EX}13. View upcoming deadlines")
    print(f"{Fore.LIGHTYELLOW_EX}14. Export tasks to JSON")
    print(f"{Fore.LIGHTGREEN_EX}15. Import tasks from JSON")
    print(f"{Fore.LIGHTRED_EX}16. Exit")
    print(f"{Fore.CYAN}" + "="*50)


def get_menu_choice():
    """Get and validate menu choice from user.

    Returns:
        int: Valid menu choice (1-16), or None if invalid
    """
    try:
        choice = int(input(f"{Fore.LIGHTYELLOW_EX}Enter your choice (1-16): {Style.RESET_ALL}"))
        if 1 <= choice <= 16:
            return choice
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter a number between 1 and 16.{Style.RESET_ALL}")
            return None
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter a number between 1 and 16.{Style.RESET_ALL}")
        return None


def get_task_id():
    """Get and validate task ID from user.

    Returns:
        int: Task ID, or None if invalid
    """
    try:
        task_id = int(input(f"{Fore.LIGHTCYAN_EX}Enter task ID: {Style.RESET_ALL}"))
        return task_id
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter a valid task ID.{Style.RESET_ALL}")
        return None


def get_priority():
    """Get priority level from user."""
    print(f"\n{Fore.LIGHTYELLOW_EX}Priority Levels:{Style.RESET_ALL}")
    print(f"{Fore.RED}1. High 🔴{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Medium 🟡{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Low 🟢{Style.RESET_ALL}")
    print(f"{Fore.WHITE}4. None (default){Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.LIGHTYELLOW_EX}Select priority (1-4): {Style.RESET_ALL}"))
        priorities = {1: "High", 2: "Medium", 3: "Low", 4: None}
        return priorities.get(choice, None)
    except ValueError:
        return None


def get_tags():
    """Get tags/categories from user."""
    tags_input = input(f"{Fore.LIGHTYELLOW_EX}Enter tags (comma-separated, e.g., work,home,urgent): {Style.RESET_ALL}")
    if tags_input.strip():
        tags = [tag.strip() for tag in tags_input.split(",")]
        return tags
    return []


def get_due_date():
    """Get due date from user."""
    print(f"\n{Fore.LIGHTCYAN_EX}Due Date Options:{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}1. Today{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}2. Tomorrow{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}3. Next week{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}4. Custom date{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}5. No due date{Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.LIGHTCYAN_EX}Select option (1-5): {Style.RESET_ALL}"))

        today = datetime.now()

        if choice == 1:
            return today.date()
        elif choice == 2:
            return (today + timedelta(days=1)).date()
        elif choice == 3:
            return (today + timedelta(days=7)).date()
        elif choice == 4:
            date_str = input(f"{Fore.LIGHTGREEN_EX}Enter date (YYYY-MM-DD): {Style.RESET_ALL}")
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        elif choice == 5:
            return None
    except (ValueError, Exception):
        print(f"{Fore.RED}❌ Invalid date format. Using no due date.{Style.RESET_ALL}")
        return None


def get_recurrence_pattern():
    """Get recurrence pattern for tasks."""
    print(f"\n{Fore.LIGHTMAGENTA_EX}Recurrence Pattern:{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}1. Daily{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}2. Weekly{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}3. Monthly{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}4. Yearly{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}5. None{Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.LIGHTMAGENTA_EX}Select recurrence pattern (1-5): {Style.RESET_ALL}"))
        patterns = {1: "daily", 2: "weekly", 3: "monthly", 4: "yearly", 5: None}
        return patterns.get(choice, None)
    except ValueError:
        return None


def handle_view_tasks(manager):
    """Handle viewing all tasks.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.CYAN}" + "📋 ALL TASKS ".ljust(50, "─"))

    if not manager.tasks:
        print("No tasks found")
        return

    # Print each task with its colored representation
    for task in manager.tasks:
        print(task.colored_str())


def handle_add_task(manager):
    """Handle adding a new task.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTGREEN_EX}" + "➕ ADD NEW TASK ".ljust(50, "─"))
    title = input(f"{Fore.LIGHTGREEN_EX}Enter task title: {Style.RESET_ALL}")
    description = input(f"{Fore.LIGHTGREEN_EX}Enter task description (optional, press Enter to skip): {Style.RESET_ALL}")

    # Get additional details
    priority = get_priority()
    tags = get_tags()
    due_date = get_due_date()
    recurrence = get_recurrence_pattern()

    success, message = manager.add_task(
        title=title,
        description=description,
        priority=priority,
        tags=tags,
        due_date=due_date,
        recurrence=recurrence
    )
    print(message)


def handle_update_task(manager):
    """Handle updating an existing task.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTCYAN_EX}" + "✏️ UPDATE TASK ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    new_title = input(f"{Fore.LIGHTCYAN_EX}Enter new title (press Enter to keep current): {Style.RESET_ALL}")
    new_description = input(f"{Fore.LIGHTCYAN_EX}Enter new description (press Enter to keep current): {Style.RESET_ALL}")

    success, message = manager.update_task(
        task_id,
        new_title if new_title else None,
        new_description if new_description else None
    )
    print(message)


def handle_delete_task(manager):
    """Handle deleting a task.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.RED}" + "🗑️ DELETE TASK ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    confirm = input(f"{Fore.RED}Are you sure you want to delete task {task_id}? (y/n): {Style.RESET_ALL}")
    if confirm.lower() == 'y':
        success, message = manager.delete_task(task_id)
        print(message)
    else:
        print(f"{Fore.YELLOW}❌ Deletion cancelled.{Style.RESET_ALL}")


def handle_toggle_complete(manager):
    """Handle toggling task completion status.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTBLUE_EX}" + "🔄 TOGGLE COMPLETION ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    success, message = manager.toggle_complete(task_id)
    print(message)


def handle_set_priority(manager):
    """Handle setting task priority.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.RED}" + "🎯 SET PRIORITY ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    priority = get_priority()
    success, message = manager.set_priority(task_id, priority)
    print(message)


def handle_add_tags(manager):
    """Handle adding tags to task.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.YELLOW}" + "🏷️ ADD TAGS ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    tags = get_tags()
    success, message = manager.add_tags(task_id, tags)
    print(message)


def handle_search_tasks(manager):
    """Handle searching tasks.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.GREEN}" + "🔍 SEARCH TASKS ".ljust(50, "─"))
    keyword = input(f"{Fore.GREEN}Enter keyword to search: {Style.RESET_ALL}")

    success, results = manager.search_tasks(keyword)
    if success:
        if results:
            print(f"\n{Fore.CYAN}Found {len(results)} task(s):{Style.RESET_ALL}")
            for task in results:
                print(f"\n{Fore.LIGHTYELLOW_EX}ID: {task['id']}{Style.RESET_ALL}")
                print(f"{Fore.LIGHTWHITE_EX}Title: {task['title']}{Style.RESET_ALL}")
                print(f"{Fore.LIGHTWHITE_EX}Description: {task.get('description', 'N/A')}{Style.RESET_ALL}")
                status = '✅ Complete' if task.get('completed') else '⏳ Pending'
                status_color = Fore.GREEN if task.get('completed') else Fore.YELLOW
                print(f"{Fore.LIGHTWHITE_EX}Status: {status_color}{status}{Style.RESET_ALL}")
                if task.get('priority'):
                    priority_color = manager._get_priority_color(task['priority'])
                    print(f"{Fore.LIGHTWHITE_EX}Priority: {priority_color}{task['priority']}{Style.RESET_ALL}")
                if task.get('tags'):
                    print(f"{Fore.LIGHTWHITE_EX}Tags: {Fore.CYAN}{', '.join(task['tags'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ No tasks found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Search failed.{Style.RESET_ALL}")


def handle_filter_tasks(manager):
    """Handle filtering tasks.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.MAGENTA}" + "🎯 FILTER TASKS ".ljust(50, "─"))
    print(f"{Fore.MAGENTA}Filter by:{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}1. Status (completed/incomplete){Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}2. Priority{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}3. Tags{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}4. Due date{Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.MAGENTA}Select filter type (1-4): {Style.RESET_ALL}"))

        if choice == 1:
            status = input(f"{Fore.LIGHTYELLOW_EX}Filter by (1. Completed, 2. Incomplete): {Style.RESET_ALL}")
            status_filter = "completed" if status == "1" else "incomplete"
            success, results = manager.filter_by_status(status_filter)

        elif choice == 2:
            priority = input(f"{Fore.LIGHTYELLOW_EX}Enter priority (High/Medium/Low): {Style.RESET_ALL}")
            success, results = manager.filter_by_priority(priority)

        elif choice == 3:
            tag = input(f"{Fore.LIGHTYELLOW_EX}Enter tag: {Style.RESET_ALL}")
            success, results = manager.filter_by_tag(tag)

        elif choice == 4:
            print(f"{Fore.LIGHTYELLOW_EX}Due date options: overdue, today, tomorrow, this_week{Style.RESET_ALL}")
            due_filter = input(f"{Fore.LIGHTYELLOW_EX}Enter due date filter: {Style.RESET_ALL}")
            success, results = manager.filter_by_due_date(due_filter)

        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")
            return

        if success and results:
            print(f"\n{Fore.CYAN}Found {len(results)} task(s):{Style.RESET_ALL}")
            for task in results:
                print(f"\n{Fore.LIGHTYELLOW_EX}ID: {task['id']} | {task['title']}{Style.RESET_ALL}")
                if task.get('due_date'):
                    due_date_color = manager._get_due_date_color(task['due_date'], False)
                    print(f"   Due: {due_date_color}{task['due_date']}{Style.RESET_ALL}")
                if task.get('priority'):
                    priority_color = manager._get_priority_color(task['priority'])
                    print(f"   Priority: {priority_color}{task['priority']}{Style.RESET_ALL}")
        elif success and not results:
            print(f"{Fore.RED}❌ No tasks match the filter.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Filter failed.{Style.RESET_ALL}")

    except ValueError:
        print(f"{Fore.RED}❌ Invalid input.{Style.RESET_ALL}")


def handle_sort_tasks(manager):
    """Handle sorting tasks.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.BLUE}" + "📊 SORT TASKS ".ljust(50, "─"))
    print(f"{Fore.BLUE}Sort by:{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}1. Priority (High to Low){Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}2. Due Date (Earliest first){Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}3. Creation Date (Newest first){Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}4. Title (A to Z){Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.BLUE}Select sort option (1-4): {Style.RESET_ALL}"))

        sort_options = {
            1: "priority",
            2: "due_date",
            3: "creation_date",
            4: "title"
        }

        sort_by = sort_options.get(choice)
        if sort_by:
            success, results = manager.sort_tasks(sort_by)
            if success and results:
                print(f"\n{Fore.CYAN}Sorted tasks ({sort_by}):{Style.RESET_ALL}")
                for task in results:
                    status = "✅" if task.get('completed') else "⏳"
                    status_color = Fore.GREEN if task.get('completed') else Fore.YELLOW
                    priority_icon = ""
                    if task.get('priority') == "High":
                        priority_icon = "🔴"
                    elif task.get('priority') == "Medium":
                        priority_icon = "🟡"
                    elif task.get('priority') == "Low":
                        priority_icon = "🟢"

                    due_info = ""
                    if task.get('due_date'):
                        due_info = f" | Due: {task['due_date']}"

                    priority_color = manager._get_priority_color(task.get('priority'))
                    print(f"{status_color}{status} {priority_color}{priority_icon}{Style.RESET_ALL} ID: {task['id']} | {task['title']}{due_info}")
        else:
            print(f"{Fore.RED}❌ Invalid sort option.{Style.RESET_ALL}")

    except ValueError:
        print(f"{Fore.RED}❌ Invalid input.{Style.RESET_ALL}")


def handle_set_due_date(manager):
    """Handle setting due date and reminder.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.CYAN}" + "📅 SET DUE DATE ".ljust(50, "─"))
    task_id = get_task_id()

    if task_id is None:
        return

    due_date = get_due_date()
    if due_date:
        success, message = manager.set_due_date(task_id, due_date)
        print(message)

        # Ask for reminder
        set_reminder = input(f"{Fore.CYAN}Set reminder for this task? (y/n): {Style.RESET_ALL}")
        if set_reminder.lower() == 'y':
            success, msg = manager.set_reminder(task_id)
            print(msg)
    else:
        print(f"{Fore.RED}❌ No due date set.{Style.RESET_ALL}")


def handle_add_recurring_task(manager):
    """Handle adding recurring task.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTMAGENTA_EX}" + "🔄 ADD RECURRING TASK ".ljust(50, "─"))
    title = input(f"{Fore.LIGHTMAGENTA_EX}Enter task title: {Style.RESET_ALL}")
    description = input(f"{Fore.LIGHTMAGENTA_EX}Enter task description (optional): {Style.RESET_ALL}")

    recurrence = get_recurrence_pattern()
    if recurrence:
        success, message = manager.add_recurring_task(title, description, recurrence)
        print(message)
    else:
        print(f"{Fore.RED}❌ No recurrence pattern selected.{Style.RESET_ALL}")


def handle_view_upcoming(manager):
    """Handle viewing upcoming deadlines.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.CYAN}" + "⏰ UPCOMING DEADLINES ".ljust(50, "─"))
    # Use the new colored method
    colored_output = manager.get_colored_upcoming_deadlines()
    print(colored_output)


def handle_export_tasks(manager):
    """Handle exporting tasks to JSON.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTYELLOW_EX}" + "💾 EXPORT TASKS ".ljust(50, "─"))
    filename = input(f"{Fore.LIGHTYELLOW_EX}Enter filename (default: tasks.json): {Style.RESET_ALL}") or "tasks.json"

    success, message = manager.export_to_json(filename)
    print(message)


def handle_import_tasks(manager):
    """Handle importing tasks from JSON.

    Args:
        manager: TaskManager instance
    """
    print(f"\n{Fore.LIGHTBLUE_EX}" + "📥 IMPORT TASKS ".ljust(50, "─"))
    filename = input(f"{Fore.LIGHTBLUE_EX}Enter filename (default: tasks.json): {Style.RESET_ALL}") or "tasks.json"

    confirm = input(f"{Fore.RED}This will overwrite current tasks. Continue? (y/n): {Style.RESET_ALL}")
    if confirm.lower() == 'y':
        success, message = manager.import_from_json(filename)
        print(message)
    else:
        print(f"{Fore.YELLOW}❌ Import cancelled.{Style.RESET_ALL}")


def main():
    """Main application loop."""
    print(f"\n{Fore.CYAN}" + "="*60)
    print(f"{Fore.MAGENTA} " * 20 + "🎯 TODO CLI - ENHANCED EDITION 🎯")
    print(f"{Fore.CYAN}" + "="*60)
    print(f"{Fore.YELLOW}Features: Priorities | Tags | Search | Filter | Sort")
    print(f"{Fore.YELLOW}          Recurring Tasks | Due Dates | Export/Import")
    print(f"{Fore.CYAN}" + "="*60)

    manager = TaskManager()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice is None:
            continue

        if choice == 1:
            handle_view_tasks(manager)
        elif choice == 2:
            handle_add_task(manager)
        elif choice == 3:
            handle_update_task(manager)
        elif choice == 4:
            handle_delete_task(manager)
        elif choice == 5:
            handle_toggle_complete(manager)
        elif choice == 6:
            handle_set_priority(manager)
        elif choice == 7:
            handle_add_tags(manager)
        elif choice == 8:
            handle_search_tasks(manager)
        elif choice == 9:
            handle_filter_tasks(manager)
        elif choice == 10:
            handle_sort_tasks(manager)
        elif choice == 11:
            handle_set_due_date(manager)
        elif choice == 12:
            handle_add_recurring_task(manager)
        elif choice == 13:
            handle_view_upcoming(manager)
        elif choice == 14:
            handle_export_tasks(manager)
        elif choice == 15:
            handle_import_tasks(manager)
        elif choice == 16:
            print(f"\n{Fore.CYAN}" + "="*50)
            print(f"{Fore.GREEN}👋 Goodbye! Your tasks are saved (if exported).")
            print(f"{Fore.CYAN}" + "="*50)
            break


if __name__ == "__main__":
    main()