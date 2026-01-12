# """Task data class for Phase I CLI Todo App.

# This module defines the Task class, which represents a single todo item
# with an ID, title, description, and completion status.
# """


# class Task:
#     """Represents a single todo item.

#     Attributes:
#         id (int): Unique integer identifier
#         title (str): Non-empty string describing the task
#         description (str): String with optional details (can be empty)
#         completed (bool): Boolean completion status
#     """

#     def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
#         """Initialize a Task instance.

#         Args:
#             task_id: Unique integer ID (assigned by TaskManager)
#             title: Task title (must be non-empty, validated by TaskManager)
#             description: Optional task description (defaults to empty string)
#             completed: Completion status (defaults to False)
#         """
#         self.id = task_id
#         self.title = title
#         self.description = description
#         self.completed = completed

#     def __repr__(self):
#         """Return string representation of Task for debugging."""
#         return (f"Task(id={self.id}, title='{self.title}', "
#                 f"description='{self.description}', completed={self.completed})")



"""Task data class for Phase I CLI Todo App.

This module defines the Task class, which represents a single todo item
with an ID, title, description, and completion status.
"""

from colorama import Fore, Style


class Task:
    """Represents a single todo item.

    Attributes:
        id (int): Unique integer identifier
        title (str): Non-empty string describing the task
        description (str): String with optional details (can be empty)
        completed (bool): Boolean completion status
        priority (str): Priority level (High/Medium/Low/None)
        tags (list): List of tags/categories for the task
        due_date (str): Due date in YYYY-MM-DD format
        recurrence (str): Recurrence pattern (daily/weekly/monthly/yearly)
        created_at (str): Creation timestamp
    """

    def __init__(self, task_id: int, title: str, description: str = "",
                 completed: bool = False, priority: str = None, tags: list = None,
                 due_date: str = None, recurrence: str = None, created_at: str = None):
        """Initialize a Task instance.

        Args:
            task_id: Unique integer ID (assigned by TaskManager)
            title: Task title (must be non-empty, validated by TaskManager)
            description: Optional task description (defaults to empty string)
            completed: Completion status (defaults to False)
            priority: Priority level (High/Medium/Low/None)
            tags: List of tags/categories for the task
            due_date: Due date in YYYY-MM-DD format
            recurrence: Recurrence pattern
            created_at: Creation timestamp
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.tags = tags or []
        self.due_date = due_date
        self.recurrence = recurrence
        self.created_at = created_at

    def __repr__(self):
        """Return string representation of Task for debugging."""
        return (f"Task(id={self.id}, title='{self.title}', "
                f"description='{self.description}', completed={self.completed}, "
                f"priority={self.priority}, tags={self.tags}, "
                f"due_date={self.due_date}, recurrence={self.recurrence}, "
                f"created_at={self.created_at})")

    def get_color(self):
        """Return color code based on priority and completion status."""
        if self.completed:
            return Fore.GREEN
        elif self.priority == "High":
            return Fore.RED
        elif self.priority == "Medium":
            return Fore.YELLOW
        elif self.priority == "Low":
            return Fore.GREEN
        else:
            return Fore.WHITE

    def __str__(self):
        """Return user-friendly string representation of Task."""
        status = "✓" if self.completed else "✗"
        priority_icon = ""

        if self.priority == "High":
            priority_icon = "🔴 "
        elif self.priority == "Medium":
            priority_icon = "🟡 "
        elif self.priority == "Low":
            priority_icon = "🟢 "

        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        due_str = f" 📅 {self.due_date}" if self.due_date else ""

        return f"[{self.id}] {priority_icon}{status} {self.title}{tags_str}{due_str}"

    def colored_str(self):
        """Return colorized string representation of Task."""
        color = self.get_color()
        status = "✓" if self.completed else "✗"
        priority_icon = ""

        if self.priority == "High":
            priority_icon = "🔴 "
        elif self.priority == "Medium":
            priority_icon = "🟡 "
        elif self.priority == "Low":
            priority_icon = "🟢 "

        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        due_str = f" 📅 {self.due_date}" if self.due_date else ""

        return f"{color}[{self.id}] {priority_icon}{status} {self.title}{tags_str}{due_str}{Style.RESET_ALL}"