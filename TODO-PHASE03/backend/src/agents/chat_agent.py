"""
ChatAgent: AI-powered task management assistant.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)

Uses OpenAI function calling to detect intent and execute MCP tools.
The agent never accesses the database directly - all operations go through MCP tools.
"""
import os
import json
import logging
from typing import Optional
from uuid import UUID

from openai import OpenAI
from sqlmodel import Session

from src.mcp.tools import ToolContext, ToolError, get_all_tools, execute_tool

logger = logging.getLogger(__name__)

# System prompt that defines agent behavior
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list using natural language.

AVAILABLE TOOLS:
1. add_task(title, description?) - Create a new task
2. list_tasks(status?) - List tasks (status: "pending", "completed", or "all")
3. complete_task(task_id) - Mark a task as completed
4. delete_task(task_id) - Delete a task (REQUIRES USER CONFIRMATION)
5. update_task(task_id, title?, description?) - Update task details

RULES:
- For DELETE operations, ALWAYS ask the user to confirm first: "Are you sure you want to delete '<task title>'? This cannot be undone. Reply 'yes' to confirm."
- Only call delete_task AFTER the user has confirmed with "yes", "confirm", "sure", or similar affirmative response
- If a user's request is ambiguous, ask for clarification
- When listing tasks, present them in a clear, readable format
- When multiple tasks match a description, list them and ask the user to specify which one
- Always confirm what action was taken after a successful tool call
- Handle errors gracefully with user-friendly explanations
- Be concise but friendly in your responses

RESPONSE STYLE:
- Keep responses short and helpful
- Use bullet points for task lists
- Include task titles when confirming actions
- Don't repeat the user's request back to them

EXAMPLES:
User: "Add a task to buy groceries"
→ Call add_task(title="Buy groceries"), then respond: "Created task: Buy groceries"

User: "What are my tasks?"
→ Call list_tasks(), then format the response as a bulleted list

User: "Mark groceries as done"
→ First call list_tasks() to find the matching task, then call complete_task(task_id)

User: "Delete the meeting task"
→ First ask: "Are you sure you want to delete 'meeting task'? This cannot be undone."
→ Wait for user confirmation before calling delete_task()"""


class ChatAgent:
    """
    AI agent for conversational task management.

    Uses OpenAI's function calling to map natural language to MCP tools.
    All database operations go through TodoService via MCP tools.
    """

    def __init__(self, user_id: UUID, session: Session):
        """
        Initialize the chat agent.

        Args:
            user_id: Authenticated user's ID from JWT
            session: Database session for tool execution
        """
        self.user_id = user_id
        self.session = session
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.tool_context = ToolContext(user_id=user_id, session=session)

    async def process_message(
        self, user_message: str, conversation_history: list[dict]
    ) -> dict:
        """
        Process a user message and generate a response.

        Args:
            user_message: The user's natural language input
            conversation_history: Previous messages for context

        Returns:
            Dict containing:
                - content: The assistant's response text
                - tool_calls: List of tool invocations (if any)
        """
        # Build messages array for OpenAI
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Get tool definitions
        tools = get_all_tools()

        tool_calls_made = []
        max_iterations = 5  # Prevent infinite loops

        for _ in range(max_iterations):
            # Call OpenAI
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                )
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return {
                    "content": "I'm having trouble processing your request. Please try again.",
                    "tool_calls": [],
                }

            choice = response.choices[0]
            assistant_message = choice.message

            # If no tool calls, return the response
            if not assistant_message.tool_calls:
                return {
                    "content": assistant_message.content or "I'm not sure how to help with that.",
                    "tool_calls": tool_calls_made,
                }

            # Process tool calls
            messages.append(assistant_message.model_dump())

            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    parameters = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    parameters = {}

                logger.info(f"Executing tool: {tool_name} with params: {parameters}")

                # Execute the tool
                try:
                    result = await execute_tool(
                        self.tool_context, tool_name, parameters
                    )
                    tool_result = {"success": True, "result": result}
                except ToolError as e:
                    logger.warning(f"Tool error: {e.code} - {e.message}")
                    tool_result = {
                        "success": False,
                        "error": {"code": e.code, "message": e.message},
                    }
                except Exception as e:
                    logger.error(f"Unexpected tool error: {e}")
                    tool_result = {
                        "success": False,
                        "error": {"code": "INTERNAL_ERROR", "message": str(e)},
                    }

                # Record the tool call
                tool_calls_made.append(
                    {
                        "tool": tool_name,
                        "parameters": parameters,
                        "result": tool_result.get("result")
                        if tool_result["success"]
                        else tool_result.get("error"),
                        "success": tool_result["success"],
                    }
                )

                # Add tool result to messages for next iteration
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

        # Max iterations reached
        return {
            "content": "I processed your request. Is there anything else you'd like to do?",
            "tool_calls": tool_calls_made,
        }

    def format_task_list(self, tasks: list[dict]) -> str:
        """
        Format a list of tasks for display.

        Args:
            tasks: List of task dictionaries

        Returns:
            Formatted string representation
        """
        if not tasks:
            return "You don't have any tasks."

        lines = []
        for task in tasks:
            status = "✓" if task.get("completed") else "○"
            lines.append(f"{status} {task['title']}")
            if task.get("description"):
                lines.append(f"  {task['description']}")

        return "\n".join(lines)
