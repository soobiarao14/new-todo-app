# Data Model: Todo AI Chatbot

**Feature**: 002-todo-ai-chatbot
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines the database schema additions for Phase III. All entities are **new additions** that do not modify existing Phase II tables.

---

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │  (Phase II - DO NOT MODIFY)
│─────────────────│
│ id (PK)         │◄─────────────────────────────────┐
│ email           │                                  │
│ ...             │                                  │
└─────────────────┘                                  │
         │                                           │
         │ 1:N                                       │ 1:N
         ▼                                           │
┌─────────────────┐                         ┌───────┴─────────┐
│     todos       │  (Phase II - DO NOT     │  conversations  │  (Phase III - NEW)
│─────────────────│   MODIFY)               │─────────────────│
│ id (PK)         │                         │ id (PK)         │
│ user_id (FK)    │                         │ user_id (FK)    │
│ title           │                         │ title           │
│ description     │                         │ created_at      │
│ completed       │                         │ updated_at      │
│ created_at      │                         └─────────────────┘
│ updated_at      │                                  │
└─────────────────┘                                  │ 1:N
                                                     ▼
                                            ┌─────────────────┐
                                            │    messages     │  (Phase III - NEW)
                                            │─────────────────│
                                            │ id (PK)         │
                                            │ user_id (FK)    │
                                            │ conversation_id │
                                            │ role            │
                                            │ content         │
                                            │ tool_calls      │
                                            │ created_at      │
                                            └─────────────────┘
```

---

## Phase III Entities (NEW)

### Conversation

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, default uuid4 | Unique conversation identifier |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEX | Owner of the conversation |
| `title` | VARCHAR(200) | NULLABLE | Optional title (auto-generated from first message) |
| `created_at` | TIMESTAMP | NOT NULL, default now() | Conversation creation time |
| `updated_at` | TIMESTAMP | NOT NULL, default now() | Last activity time |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (for listing user's conversations)
- `idx_conversations_updated_at` on `updated_at` (for sorting by recent activity)

**Relationships**:
- Belongs to one `User` (via `user_id`)
- Has many `Message` records

**SQLModel Definition**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### Message

Represents a single message in a conversation (user or assistant).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, default uuid4 | Unique message identifier |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEX | Message owner (for isolation) |
| `conversation_id` | UUID | FOREIGN KEY → conversations.id, NOT NULL, INDEX | Parent conversation |
| `role` | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender role |
| `content` | TEXT | NOT NULL | Message text content |
| `tool_calls` | JSONB | NULLABLE | MCP tool invocations (assistant only) |
| `created_at` | TIMESTAMP | NOT NULL, default now() | Message timestamp |

**Indexes**:
- `idx_messages_user_id` on `user_id` (for user isolation queries)
- `idx_messages_conversation_id` on `conversation_id` (for loading conversation)
- `idx_messages_created_at` on `created_at` (for chronological ordering)

**Relationships**:
- Belongs to one `User` (via `user_id`)
- Belongs to one `Conversation` (via `conversation_id`)

**SQLModel Definition**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Tool Call Structure (JSONB)

The `tool_calls` field stores MCP tool invocations for assistant messages.

**Schema**:
```json
{
  "calls": [
    {
      "tool": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread"
      },
      "result": {
        "task_id": "uuid-string",
        "status": "created",
        "title": "Buy groceries"
      },
      "success": true
    }
  ]
}
```

**Fields**:
- `tool`: MCP tool name (add_task, list_tasks, complete_task, delete_task, update_task)
- `parameters`: Input parameters passed to the tool
- `result`: Tool execution result
- `success`: Boolean indicating if tool succeeded

---

## Phase II Entities (PRESERVED - DO NOT MODIFY)

### User (Reference Only)

Managed by Better Auth. Phase III references but does not modify.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key, referenced by conversations and messages |
| `email` | VARCHAR | User identifier |
| `...` | ... | Other Better Auth managed fields |

### Todo (Reference Only)

Managed by Phase II. Phase III accesses via MCP tools only.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to users |
| `title` | VARCHAR(200) | Task title |
| `description` | TEXT | Optional description |
| `completed` | BOOLEAN | Completion status |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Last update time |

---

## Validation Rules

### Conversation Validation

| Rule | Constraint | Error |
|------|------------|-------|
| User must exist | FK constraint | 400 Bad Request |
| Title max length | 200 chars | 400 Bad Request |

### Message Validation

| Rule | Constraint | Error |
|------|------------|-------|
| User must exist | FK constraint | 400 Bad Request |
| Conversation must exist | FK constraint | 404 Not Found |
| Role must be valid | CHECK constraint | 400 Bad Request |
| Content must not be empty | NOT NULL + app check | 400 Bad Request |
| User must own conversation | App-level check | 404 Not Found |

---

## User Isolation Enforcement

**Critical**: All queries MUST enforce user isolation.

```python
# GOOD: User isolation enforced
def get_conversation(conversation_id: UUID, user_id: UUID):
    return session.exec(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)  # CRITICAL
    ).first()

# BAD: Never do this
def get_conversation_unsafe(conversation_id: UUID):
    return session.exec(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        # MISSING user_id filter = DATA LEAK
    ).first()
```

---

## Migration Strategy

**Approach**: SQLModel auto-creates tables on startup (consistent with Phase II).

**Steps**:
1. Add new model files: `backend/src/models/conversation.py`, `backend/src/models/message.py`
2. Import models in `backend/src/models/__init__.py`
3. Tables created automatically on FastAPI startup via `create_db_and_tables()`

**Rollback**: Drop `messages` table first (has FK), then `conversations` table.

---

## Query Patterns

### List User's Conversations (sorted by recent activity)
```python
select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
```

### Load Conversation Messages (chronological)
```python
select(Message)
    .where(Message.conversation_id == conversation_id)
    .where(Message.user_id == user_id)  # CRITICAL: isolation
    .order_by(Message.created_at.asc())
```

### Create New Conversation
```python
conversation = Conversation(
    user_id=user_id,
    title=None,  # Auto-generate later from first message
)
session.add(conversation)
session.commit()
```

### Add Message to Conversation
```python
message = Message(
    user_id=user_id,
    conversation_id=conversation_id,
    role="user",  # or "assistant"
    content=content,
    tool_calls=None,  # or JSON dict for assistant
)
session.add(message)
session.commit()
```
