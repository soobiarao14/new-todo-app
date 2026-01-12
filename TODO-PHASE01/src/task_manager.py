# """TaskManager class for Phase I CLI Todo App.

# This module implements the business logic for managing tasks in memory.
# It provides CRUD operations (Create, Read, Update, Delete) and completion toggling.
# """

# from task import Task


# class TaskManager:
#     """Manages in-memory task collection and provides CRUD operations.

#     Attributes:
#         tasks (list[Task]): List of all tasks in memory
#         next_id (int): Counter for generating unique task IDs
#     """

#     def __init__(self):
#         """Initialize TaskManager with empty task list and ID counter starting at 1."""
#         self.tasks = []
#         self.next_id = 1

#     def add_task(self, title: str, description: str = "") -> tuple[bool, str]:
#         """Add a new task to the task list.

#         Args:
#             title: Task title (required, must be non-empty)
#             description: Task description (optional, defaults to empty string)

#         Returns:
#             Tuple of (success: bool, message: str)
#             - On success: (True, "Task added successfully with ID {id}")
#             - On failure: (False, "Task title cannot be empty")
#         """
#         # Validate title is not empty or whitespace-only
#         if not title or not title.strip():
#             return (False, "Task title cannot be empty")

#         # Create new task with auto-assigned ID
#         new_task = Task(
#             task_id=self.next_id,
#             title=title,
#             description=description,
#             completed=False
#         )

#         # Add to list and increment ID counter
#         self.tasks.append(new_task)
#         task_id = self.next_id
#         self.next_id += 1

#         return (True, f"Task added successfully with ID {task_id}")

#     def view_tasks(self) -> tuple[bool, str]:
#         """Retrieve all tasks formatted for display.

#         Returns:
#             Tuple of (success: bool, message: str)
#             - If tasks exist: (True, formatted string with all task details)
#             - If no tasks: (True, "No tasks found")
#         """
#         if not self.tasks:
#             return (True, "No tasks found")

#         # Format all tasks for display
#         lines = []
#         for task in self.tasks:
#             status = "Complete" if task.completed else "Incomplete"
#             lines.append(f"[{task.id}] Title: {task.title}")
#             lines.append(f"    Description: {task.description}")
#             lines.append(f"    Status: {status}")
#             lines.append("")  # Blank line between tasks

#         return (True, "\n".join(lines))

#     def update_task(self, task_id: int, new_title: str, new_description: str = "") -> tuple[bool, str]:
#         """Update an existing task's title and description.

#         Args:
#             task_id: ID of task to update
#             new_title: New title (required, must be non-empty)
#             new_description: New description (optional, defaults to empty string)

#         Returns:
#             Tuple of (success: bool, message: str)
#             - On success: (True, "Task updated successfully")
#             - On failure: (False, error message)
#         """
#         # Validate new title is not empty
#         if not new_title or not new_title.strip():
#             return (False, "Task title cannot be empty")

#         # Find task by ID
#         task = self._find_task_by_id(task_id)
#         if task is None:
#             return (False, "Task ID not found")

#         # Update task fields
#         task.title = new_title
#         task.description = new_description

#         return (True, "Task updated successfully")

#     def delete_task(self, task_id: int) -> tuple[bool, str]:
#         """Permanently remove a task from the task list.

#         Args:
#             task_id: ID of task to delete

#         Returns:
#             Tuple of (success: bool, message: str)
#             - On success: (True, "Task deleted successfully")
#             - On failure: (False, "Task ID not found")
#         """
#         # Find task by ID
#         task = self._find_task_by_id(task_id)
#         if task is None:
#             return (False, "Task ID not found")

#         # Remove task from list
#         self.tasks.remove(task)

#         return (True, "Task deleted successfully")

#     def toggle_complete(self, task_id: int) -> tuple[bool, str]:
#         """Toggle a task's completion status between complete and incomplete.

#         Args:
#             task_id: ID of task to toggle

#         Returns:
#             Tuple of (success: bool, message: str)
#             - On success: (True, "Task marked as complete") or (True, "Task marked as incomplete")
#             - On failure: (False, "Task ID not found")
#         """
#         # Find task by ID
#         task = self._find_task_by_id(task_id)
#         if task is None:
#             return (False, "Task ID not found")

#         # Toggle completion status
#         task.completed = not task.completed

#         # Return appropriate message based on new status
#         if task.completed:
#             return (True, "Task marked as complete")
#         else:
#             return (True, "Task marked as incomplete")

#     def _find_task_by_id(self, task_id: int):
#         """Find a task by its ID.

#         Args:
#             task_id: ID to search for

#         Returns:
#             Task object if found, None otherwise
#         """
#         for task in self.tasks:
#             if task.id == task_id:
#                 return task
#         return None



"""TaskManager class for Phase I CLI Todo App.

This module implements the business logic for managing tasks in memory.
It provides CRUD operations (Create, Read, Update, Delete) and completion toggling.
"""

from task import Task
from datetime import datetime, timedelta
import json
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


class TaskManager:
    """Manages in-memory task collection and provides CRUD operations.

    Attributes:
        tasks (list[Task]): List of all tasks in memory
        next_id (int): Counter for generating unique task IDs
    """

    def __init__(self):
        """Initialize TaskManager with empty task list and ID counter starting at 1."""
        self.tasks = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "", priority: str = None,
                 tags: list = None, due_date: str = None, recurrence: str = None) -> tuple[bool, str]:
        """Add a new task to the task list.

        Args:
            title: Task title (required, must be non-empty)
            description: Task description (optional, defaults to empty string)
            priority: Priority level (High/Medium/Low)
            tags: List of tags/categories
            due_date: Due date in string format
            recurrence: Recurrence pattern (daily/weekly/monthly/yearly)

        Returns:
            Tuple of (success: bool, message: str)
            - On success: (True, "Task added successfully with ID {id}")
            - On failure: (False, "Task title cannot be empty")
        """
        # Validate title is not empty or whitespace-only
        if not title or not title.strip():
            return (False, f"{Fore.RED}❌ Task title cannot be empty{Style.RESET_ALL}")

        # Create new task with auto-assigned ID
        new_task = Task(
            task_id=self.next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence=recurrence,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Add to list and increment ID counter
        self.tasks.append(new_task)
        task_id = self.next_id
        self.next_id += 1

        # Color the task ID based on priority
        priority_color = self._get_priority_color(priority) if priority else Fore.WHITE
        return (True, f"{Fore.GREEN}Task added successfully with ID {priority_color}{task_id}{Style.RESET_ALL}")

    def view_tasks(self) -> tuple[bool, str]:
        """Retrieve all tasks formatted for display.

        Returns:
            Tuple of (success: bool, message: str)
            - If tasks exist: (True, formatted string with all task details)
            - If no tasks: (True, "No tasks found")
        """
        if not self.tasks:
            return (True, "No tasks found")

        # Format all tasks for display
        lines = []
        for task in self.tasks:
            status = "✅ Complete" if task.completed else "⏳ Incomplete"
            priority_icon = ""
            if task.priority == "High":
                priority_icon = "🔴 "
            elif task.priority == "Medium":
                priority_icon = "🟡 "
            elif task.priority == "Low":
                priority_icon = "🟢 "

            # Apply color based on task priority/completion
            task_color = task.get_color()

            lines.append(f"\n{task_color}[{task.id}] {priority_icon}{task.title}{Style.RESET_ALL}")
            lines.append(f"    Description: {task.description}")
            lines.append(f"    Status: {status}")

            if task.priority:
                priority_color = self._get_priority_color(task.priority)
                lines.append(f"    Priority: {priority_color}{task.priority}{Style.RESET_ALL}")

            if task.tags:
                lines.append(f"    Tags: {', '.join(task.tags)}")

            if task.due_date:
                due_date_color = self._get_due_date_color(task.due_date, task.completed)
                lines.append(f"    Due Date: {due_date_color}{task.due_date}{Style.RESET_ALL}")

            if task.recurrence:
                lines.append(f"    Recurrence: {task.recurrence.capitalize()}")

            lines.append(f"    Created: {task.created_at}")

        return (True, "\n".join(lines))

    def _get_priority_color(self, priority: str):
        """Get color based on priority level."""
        if priority == "High":
            return Fore.RED
        elif priority == "Medium":
            return Fore.YELLOW
        elif priority == "Low":
            return Fore.GREEN
        else:
            return Fore.WHITE

    def _get_due_date_color(self, due_date: str, completed: bool):
        """Get color based on due date proximity."""
        if completed:
            return Fore.GREEN

        from datetime import datetime
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            days_diff = (due - today).days

            if days_diff < 0:  # Overdue
                return Fore.RED
            elif days_diff == 0:  # Due today
                return Fore.MAGENTA
            elif days_diff <= 3:  # Due in next 3 days
                return Fore.LIGHTYELLOW_EX
            else:
                return Fore.CYAN
        except:
            return Fore.WHITE

    def update_task(self, task_id: int, new_title: str = None, new_description: str = None) -> tuple[bool, str]:
        """Update an existing task's title and description.

        Args:
            task_id: ID of task to update
            new_title: New title (optional)
            new_description: New description (optional)

        Returns:
            Tuple of (success: bool, message: str)
            - On success: (True, "Task updated successfully")
            - On failure: (False, error message)
        """
        # Find task by ID
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, f"{Fore.RED}❌ Task ID not found{Style.RESET_ALL}")

        # Update task fields if provided
        if new_title is not None and new_title.strip():
            task.title = new_title

        if new_description is not None:
            task.description = new_description

        return (True, f"{Fore.CYAN}✏️ Task {task_id} updated successfully{Style.RESET_ALL}")

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Permanently remove a task from the task list.

        Args:
            task_id: ID of task to delete

        Returns:
            Tuple of (success: bool, message: str)
            - On success: (True, "Task deleted successfully")
            - On failure: (False, "Task ID not found")
        """
        # Find task by ID
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, f"{Fore.RED}❌ Task ID not found{Style.RESET_ALL}")

        # Remove task from list
        self.tasks.remove(task)

        return (True, f"{Fore.RED}🗑️ Task {task_id} deleted successfully{Style.RESET_ALL}")

    def toggle_complete(self, task_id: int) -> tuple[bool, str]:
        """Toggle a task's completion status between complete and incomplete.

        Args:
            task_id: ID of task to toggle

        Returns:
            Tuple of (success: bool, message: str)
            - On success: (True, "Task marked as complete") or (True, "Task marked as incomplete")
            - On failure: (False, "Task ID not found")
        """
        # Find task by ID
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, "Task ID not found")

        # Toggle completion status
        task.completed = not task.completed

        # Return appropriate message based on new status
        if task.completed:
            return (True, f"{Fore.GREEN}✅ Task marked as complete{Style.RESET_ALL}")
        else:
            return (True, f"{Fore.YELLOW}⏳ Task marked as incomplete{Style.RESET_ALL}")

    def set_priority(self, task_id: int, priority: str) -> tuple[bool, str]:
        """Set priority for a task.

        Args:
            task_id: ID of task
            priority: Priority level (High/Medium/Low/None)

        Returns:
            Tuple of (success: bool, message: str)
        """
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, "Task ID not found")

        task.priority = priority
        priority_color = self._get_priority_color(priority)
        return (True, f"{Fore.GREEN}✅ Priority set to {priority_color}{priority}{Fore.GREEN} for task {task_id}{Style.RESET_ALL}")

    def add_tags(self, task_id: int, tags: list) -> tuple[bool, str]:
        """Add tags to a task.

        Args:
            task_id: ID of task
            tags: List of tags to add

        Returns:
            Tuple of (success: bool, message: str)
        """
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, "Task ID not found")

        if not hasattr(task, 'tags'):
            task.tags = []

        for tag in tags:
            if tag not in task.tags:
                task.tags.append(tag)

        return (True, f"{Fore.GREEN}✅ Tags added: {Fore.CYAN}{', '.join(tags)}{Fore.GREEN}{Style.RESET_ALL}")

    def search_tasks(self, keyword: str) -> tuple[bool, list]:
        """Search tasks by keyword in title or description.

        Args:
            keyword: Keyword to search for

        Returns:
            Tuple of (success: bool, list of matching tasks)
        """
        if not keyword:
            return (False, [])
        
        keyword = keyword.lower()
        results = []
        
        for task in self.tasks:
            if (keyword in task.title.lower() or 
                keyword in task.description.lower() or
                any(keyword in tag.lower() for tag in task.tags)):
                
                results.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date
                })
        
        return (True, results)

    def filter_by_status(self, status: str) -> tuple[bool, list]:
        """Filter tasks by completion status.

        Args:
            status: 'completed' or 'incomplete'

        Returns:
            Tuple of (success: bool, list of filtered tasks)
        """
        is_completed = (status == "completed")
        results = []
        
        for task in self.tasks:
            if task.completed == is_completed:
                results.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date
                })
        
        return (True, results)

    def filter_by_priority(self, priority: str) -> tuple[bool, list]:
        """Filter tasks by priority.

        Args:
            priority: Priority level (High/Medium/Low)

        Returns:
            Tuple of (success: bool, list of filtered tasks)
        """
        results = []
        
        for task in self.tasks:
            if task.priority == priority:
                results.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date
                })
        
        return (True, results)

    def filter_by_tag(self, tag: str) -> tuple[bool, list]:
        """Filter tasks by tag.

        Args:
            tag: Tag to filter by

        Returns:
            Tuple of (success: bool, list of filtered tasks)
        """
        results = []
        
        for task in self.tasks:
            if hasattr(task, 'tags') and tag in task.tags:
                results.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date
                })
        
        return (True, results)

    def filter_by_due_date(self, due_filter: str) -> tuple[bool, list]:
        """Filter tasks by due date.

        Args:
            due_filter: Filter type (overdue, today, tomorrow, this_week)

        Returns:
            Tuple of (success: bool, list of filtered tasks)
        """
        results = []
        today = datetime.now().date()
        
        for task in self.tasks:
            if not task.due_date:
                continue
                
            try:
                due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                days_diff = (due_date - today).days
                
                if due_filter == "overdue" and days_diff < 0 and not task.completed:
                    results.append({
                        'id': task.id,
                        'title': task.title,
                        'due_date': task.due_date,
                        'priority': task.priority,
                        'days_late': abs(days_diff)
                    })
                elif due_filter == "today" and days_diff == 0:
                    results.append({
                        'id': task.id,
                        'title': task.title,
                        'due_date': task.due_date,
                        'priority': task.priority
                    })
                elif due_filter == "tomorrow" and days_diff == 1:
                    results.append({
                        'id': task.id,
                        'title': task.title,
                        'due_date': task.due_date,
                        'priority': task.priority
                    })
                elif due_filter == "this_week" and 0 <= days_diff <= 7:
                    results.append({
                        'id': task.id,
                        'title': task.title,
                        'due_date': task.due_date,
                        'priority': task.priority,
                        'days_left': days_diff
                    })
            except:
                continue
        
        return (True, results)

    def sort_tasks(self, sort_by: str) -> tuple[bool, list]:
        """Sort tasks by specified criteria.

        Args:
            sort_by: Sorting criteria (priority, due_date, creation_date, title)

        Returns:
            Tuple of (success: bool, list of sorted tasks)
        """
        if not self.tasks:
            return (True, [])
        
        # Create a copy for sorting
        tasks_copy = list(self.tasks)
        
        # Define priority order
        priority_order = {"High": 1, "Medium": 2, "Low": 3, None: 4}
        
        if sort_by == "priority":
            tasks_copy.sort(key=lambda x: priority_order.get(x.priority, 4))
        
        elif sort_by == "due_date":
            def get_due_date(task):
                if task.due_date:
                    try:
                        return datetime.strptime(task.due_date, "%Y-%m-%d")
                    except:
                        return datetime.max
                return datetime.max
            tasks_copy.sort(key=get_due_date)
        
        elif sort_by == "creation_date":
            tasks_copy.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') else "", reverse=True)
        
        elif sort_by == "title":
            tasks_copy.sort(key=lambda x: x.title.lower())
        
        # Convert to dictionary format for display
        results = []
        for task in tasks_copy:
            results.append({
                'id': task.id,
                'title': task.title,
                'completed': task.completed,
                'priority': task.priority,
                'due_date': task.due_date,
                'created_at': task.created_at if hasattr(task, 'created_at') else ""
            })
        
        return (True, results)

    def set_due_date(self, task_id: int, due_date) -> tuple[bool, str]:
        """Set due date for a task.

        Args:
            task_id: ID of task
            due_date: Due date object or string

        Returns:
            Tuple of (success: bool, message: str)
        """
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, f"{Fore.RED}❌ Task ID not found{Style.RESET_ALL}")

        if isinstance(due_date, datetime):
            due_date_str = due_date.strftime("%Y-%m-%d")
        else:
            due_date_str = str(due_date)

        task.due_date = due_date_str
        due_date_color = self._get_due_date_color(due_date_str, task.completed)
        return (True, f"{Fore.GREEN}✅ Due date set to {due_date_color}{due_date_str}{Style.RESET_ALL}")

    def set_reminder(self, task_id: int) -> tuple[bool, str]:
        """Set reminder for a task (simulated).

        Args:
            task_id: ID of task

        Returns:
            Tuple of (success: bool, message: str)
        """
        task = self._find_task_by_id(task_id)
        if task is None:
            return (False, f"{Fore.RED}❌ Task ID not found{Style.RESET_ALL}")

        if task.due_date:
            due_date_color = self._get_due_date_color(task.due_date, task.completed)
            return (True, f"{Fore.CYAN}🔔 Reminder set for task {task_id} due on {due_date_color}{task.due_date}{Style.RESET_ALL}")
        else:
            return (False, f"{Fore.RED}❌ Cannot set reminder: No due date set{Style.RESET_ALL}")

    def add_recurring_task(self, title: str, description: str, recurrence: str) -> tuple[bool, str]:
        """Add a recurring task.

        Args:
            title: Task title
            description: Task description
            recurrence: Recurrence pattern

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not title or not title.strip():
            return (False, f"{Fore.RED}❌ Task title cannot be empty{Style.RESET_ALL}")

        # Add the initial task
        success, message = self.add_task(
            title=title,
            description=description,
            recurrence=recurrence
        )

        if success:
            recurrence_color = self._get_recurrence_color(recurrence)
            return (True, f"{Fore.GREEN}✅ Recurring task added ({recurrence_color}{recurrence}{Fore.GREEN}): {message}{Style.RESET_ALL}")
        else:
            return (False, message)

    def _get_recurrence_color(self, recurrence: str):
        """Get color based on recurrence pattern."""
        if recurrence == "daily":
            return Fore.LIGHTYELLOW_EX
        elif recurrence == "weekly":
            return Fore.CYAN
        elif recurrence == "monthly":
            return Fore.MAGENTA
        elif recurrence == "yearly":
            return Fore.LIGHTBLUE_EX
        else:
            return Fore.WHITE

    def get_upcoming_deadlines(self) -> tuple[bool, list]:
        """Get upcoming deadlines.

        Returns:
            Tuple of (success: bool, list of upcoming tasks)
        """
        results = []
        today = datetime.now().date()

        for task in self.tasks:
            if task.due_date and not task.completed:
                try:
                    due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    days_left = (due_date - today).days

                    if days_left >= 0:  # Only future dates
                        results.append({
                            'id': task.id,
                            'title': task.title,
                            'due_date': task.due_date,
                            'days_left': days_left,
                            'priority': task.priority
                        })
                except:
                    continue

        # Sort by days left
        results.sort(key=lambda x: x['days_left'])

        return (True, results)

    def get_colored_upcoming_deadlines(self) -> str:
        """Get upcoming deadlines with colored output.

        Returns:
            Formatted string with colored upcoming tasks
        """
        results = []
        today = datetime.now().date()

        for task in self.tasks:
            if task.due_date and not task.completed:
                try:
                    due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    days_left = (due_date - today).days

                    if days_left >= 0:  # Only future dates
                        results.append({
                            'id': task.id,
                            'title': task.title,
                            'due_date': task.due_date,
                            'days_left': days_left,
                            'priority': task.priority
                        })
                except:
                    continue

        # Sort by days left
        results.sort(key=lambda x: x['days_left'])

        if not results:
            return f"{Fore.GREEN}✅ No upcoming deadlines!{Style.RESET_ALL}"

        output_lines = [f"{Fore.CYAN}\n⏰ UPCOMING DEADLINES{Style.RESET_ALL}"]
        for task in results:
            days_left = task.get('days_left', 0)
            urgency = ""
            if days_left == 0:
                urgency = f"{Fore.RED}🔴 TODAY!{Style.RESET_ALL}"
            elif days_left == 1:
                urgency = f"{Fore.YELLOW}🟡 TOMORROW{Style.RESET_ALL}"
            elif days_left <= 3:
                urgency = f"{Fore.LIGHTYELLOW_EX}🟢 Due in {days_left} days{Style.RESET_ALL}"
            elif days_left <= 7:
                urgency = f"{Fore.CYAN}🔵 This week{Style.RESET_ALL}"

            due_date_color = self._get_due_date_color(task['due_date'], False)
            priority_color = self._get_priority_color(task.get('priority'))

            output_lines.append(f"\n{urgency} | ID: {task['id']} | {task['title']}")
            output_lines.append(f"   Due: {due_date_color}{task['due_date']}{Style.RESET_ALL} ({days_left} days left)")
            if task.get('priority'):
                output_lines.append(f"   Priority: {priority_color}{task['priority']}{Style.RESET_ALL}")

        return "\n".join(output_lines)

    def export_to_json(self, filename: str) -> tuple[bool, str]:
        """Export tasks to JSON file.

        Args:
            filename: JSON filename

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            tasks_data = []
            for task in self.tasks:
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date,
                    'recurrence': task.recurrence,
                    'created_at': task.created_at if hasattr(task, 'created_at') else ""
                }
                tasks_data.append(task_dict)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)

            return (True, f"{Fore.GREEN}✅ Tasks exported to {Fore.CYAN}{filename}{Style.RESET_ALL}")

        except Exception as e:
            return (False, f"{Fore.RED}❌ Export failed: {str(e)}{Style.RESET_ALL}")

    def import_from_json(self, filename: str) -> tuple[bool, str]:
        """Import tasks from JSON file.

        Args:
            filename: JSON filename

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Clear current tasks
            self.tasks = []
            
            # Find max ID
            max_id = 0
            for task_data in tasks_data:
                if task_data['id'] > max_id:
                    max_id = task_data['id']
                
                # Recreate task
                task = Task(
                    task_id=task_data['id'],
                    title=task_data['title'],
                    description=task_data['description'],
                    completed=task_data['completed'],
                    priority=task_data.get('priority'),
                    tags=task_data.get('tags', []),
                    due_date=task_data.get('due_date'),
                    recurrence=task_data.get('recurrence')
                )
                
                if 'created_at' in task_data:
                    task.created_at = task_data['created_at']
                
                self.tasks.append(task)
            
            # Set next_id
            self.next_id = max_id + 1

            return (True, f"{Fore.GREEN}✅ {len(tasks_data)} tasks imported from {Fore.CYAN}{filename}{Style.RESET_ALL}")

        except FileNotFoundError:
            return (False, f"{Fore.RED}❌ File not found: {filename}{Style.RESET_ALL}")
        except Exception as e:
            return (False, f"{Fore.RED}❌ Import failed: {str(e)}{Style.RESET_ALL}")

    def _find_task_by_id(self, task_id: int):
        """Find a task by its ID.

        Args:
            task_id: ID to search for

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None