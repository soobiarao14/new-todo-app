# Quickstart Guide: Todo AI Chatbot

**Feature**: 002-todo-ai-chatbot
**Date**: 2026-01-20

## Prerequisites

Before starting, ensure you have:

1. **Phase II Backend Running**: The existing FastAPI backend must be operational
2. **Phase II Frontend Running**: The existing Next.js frontend must be operational
3. **OpenAI API Key**: Required for AI agent functionality
4. **Node.js 18+**: For frontend development
5. **Python 3.11+**: For backend development

---

## Environment Setup

### 1. Backend Environment Variables

Add to `backend/.env`:

```env
# Existing Phase II variables (keep as-is)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...

# New Phase III variables
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o
```

### 2. Frontend Environment Variables

Add to `frontend/.env.local`:

```env
# Existing Phase II variables (keep as-is)
NEXT_PUBLIC_API_URL=http://localhost:8000

# No additional Phase III variables needed
```

---

## Running the Application

### Start Backend

```bash
cd backend
pip install openai mcp  # New Phase III dependencies
uvicorn src.main:app --reload --port 8000
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Testing the Chat Feature

### 1. Sign In

Navigate to `http://localhost:3000/signin` and log in with your credentials.

### 2. Open Chat

Navigate to `http://localhost:3000/chat` to access the AI chatbot.

### 3. Try These Commands

**Create a Task**:
```
Add a task to buy groceries
```

**List Tasks**:
```
What are my tasks?
Show me pending tasks
```

**Complete a Task**:
```
Mark the groceries task as done
```

**Delete a Task** (requires confirmation):
```
Delete the groceries task
```

**Update a Task**:
```
Rename the report task to Q4 Report
```

---

## API Endpoints

### Chat Endpoint

```bash
# Send a chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### List Conversations

```bash
curl http://localhost:8000/api/conversations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Conversation Details

```bash
curl http://localhost:8000/api/conversations/{conversation_id} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Dashboard Stats

```bash
curl http://localhost:8000/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Troubleshooting

### "OpenAI API Key not configured"

Ensure `OPENAI_API_KEY` is set in `backend/.env`.

### "Authentication required"

Ensure you're logged in and the JWT token is valid.

### "Conversation not found"

The conversation ID doesn't exist or belongs to another user.

### Chat responses are slow

AI responses may take 2-5 seconds depending on OpenAI API latency. This is normal.

---

## Project Structure (Phase III Additions)

```
backend/src/
├── agents/
│   ├── __init__.py
│   └── chat_agent.py       # OpenAI agent logic
├── mcp/
│   ├── __init__.py
│   └── tools.py            # MCP tool definitions
├── models/
│   ├── conversation.py     # NEW: Conversation model
│   └── message.py          # NEW: Message model
├── routes/
│   └── chat.py             # NEW: Chat endpoints
├── services/
│   └── chat_service.py     # NEW: Chat business logic
└── schemas/
    └── chat.py             # NEW: Chat request/response schemas

frontend/src/
├── app/
│   ├── chat/
│   │   └── page.tsx        # NEW: Chat page
│   └── dashboard/
│       └── page.tsx        # NEW: Dashboard page
├── components/
│   └── chat/
│       ├── ChatWindow.tsx  # NEW: Chat interface
│       ├── MessageInput.tsx
│       ├── MessageBubble.tsx
│       └── ConversationList.tsx
└── lib/
    └── chatApi.ts          # NEW: Chat API client
```

---

## Next Steps

1. Review the [API Contract](./contracts/chat-api.yaml) for full endpoint details
2. Review the [MCP Tools Contract](./contracts/mcp-tools.md) for tool specifications
3. Review the [Data Model](./data-model.md) for database schema details
4. Run `/sp.tasks` to generate implementation tasks
