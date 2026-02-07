"""
MCP (Model Context Protocol) tools module for AI chatbot.
Phase III: Todo AI Chatbot - NEW MODULE (does not modify Phase II)

This module provides task operation tools that the AI agent can invoke.
All tools enforce user isolation and operate through Phase II TodoService.
"""
from src.mcp.tools import (
    ToolContext,
    ToolError,
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    get_all_tools,
    execute_tool,
)

__all__ = [
    "ToolContext",
    "ToolError",
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
    "get_all_tools",
    "execute_tool",
]
