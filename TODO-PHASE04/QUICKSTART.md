# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: Phase II Full-Stack Web Application
**Purpose**: Local development setup and getting started guide
**Last Updated**: 2026-01-11

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Git** installed
- **Neon account** (free tier) - https://neon.tech
- **Better Auth account** and configuration

## Project Structure

```
TODO-PHASE02/
├── backend/      # FastAPI application
├── frontend/     # Next.js application
├── specs/        # Design documents
└── history/      # PHRs and ADRs
```

---

## Part 1: Database Setup (Neon PostgreSQL)

### Step 1: Create Neon Database

1. Visit https://neon.tech and sign in
2. Create new project: "todo-phase-ii"
3. Copy connection string (looks like):
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```
4. Save connection string for backend configuration

### Step 2: Initialize Schema

Schema will be created automatically by SQLModel on first run via `SQLModel.metadata.create_all()`.

---

## Part 2: Better Auth Setup

### Step 1: Configure Better Auth

1. Create Better Auth project or configure existing
2. Set up email/password authentication
3. Configure JWT settings:
   - Algorithm: RS256
   - Expiration: 1 hour
   - Issuer: Your Better Auth domain
4. Note your Better Auth URLs:
   - Base URL: `https://auth.yourapp.com`
   - JWKS URL: `https://auth.yourapp.com/.well-known/jwks.json`

### Step 2: Save Credentials

Save Better Auth credentials for configuration:
- Better Auth Secret
- JWKS URL
- Public Base URL

---

## Part 3: Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd TODO-PHASE02/backend
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install fastapi uvicorn sqlmodel psycopg2-binary python-jose[cryptography] python-dotenv pydantic[email]
```

Or if using pyproject.toml:
```bash
pip install -e .
```

### Step 4: Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Better Auth
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_JWKS_URL=https://auth.yourapp.com/.well-known/jwks.json
BETTER_AUTH_BASE_URL=https://auth.yourapp.com

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**IMPORTANT**: Never commit `.env` file to git. Use `.env.example` as template.

### Step 5: Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

Backend should start at: http://localhost:8000

### Step 6: Verify Backend

Open browser to:
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/redoc - Alternative API documentation

---

## Part 4: Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd TODO-PHASE02/frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This installs Next.js, React, TypeScript, Tailwind CSS, and other dependencies.

### Step 3: Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
NEXT_PUBLIC_BETTER_AUTH_URL=https://auth.yourapp.com

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

**IMPORTANT**: Never commit `.env.local` to git. Use `.env.local.example` as template.

### Step 4: Start Frontend Dev Server

```bash
npm run dev
```

Frontend should start at: http://localhost:3000

### Step 5: Verify Frontend

Open browser to:
- http://localhost:3000 - Home page (should redirect to /signin)
- http://localhost:3000/signup - Sign up page
- http://localhost:3000/signin - Sign in page

---

## Part 5: Running the Application

### Start Both Services

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### Test the Application

1. **Sign Up**:
   - Navigate to http://localhost:3000/signup
   - Create account with email and password (min 8 chars)
   - Should redirect to /todos after signup

2. **Create Todo**:
   - Click "Add Todo" button
   - Enter title: "Test Todo"
   - Enter description: "This is a test"
   - Submit form
   - Todo should appear in list

3. **Mark Complete**:
   - Click checkbox on todo item
   - Todo should show as completed (strikethrough)

4. **Edit Todo**:
   - Click "Edit" button on todo
   - Modify title or description
   - Save changes
   - Updated todo should display

5. **Delete Todo**:
   - Click "Delete" button on todo
   - Confirm deletion
   - Todo should be removed from list

6. **Sign Out**:
   - Click "Sign Out" button
   - Should redirect to /signin
   - Verify cannot access /todos (redirected to /signin)

7. **Sign In Again**:
   - Enter email and password
   - Should redirect to /todos
   - Todos should persist (loaded from database)

---

## Part 6: Testing User Isolation

### Create Second User

1. Sign out from first account
2. Sign up with different email
3. Create some todos for second user
4. Verify second user ONLY sees their own todos

### Verify Isolation

1. Sign in as User A
2. Create todo, note the todo ID from browser DevTools
3. Sign out
4. Sign in as User B
5. Try to access User A's todo:
   - Open DevTools Console
   - Run: `fetch('/api/tasks/<user-a-todo-id>', {headers: {'Authorization': 'Bearer ' + getToken()}})`
   - Should return 404 Not Found (not 403)

---

## Part 7: Development Workflow

### Make Code Changes

**Backend Changes**:
- Edit files in `backend/src/`
- FastAPI auto-reloads on file save
- Check http://localhost:8000/docs for API changes

**Frontend Changes**:
- Edit files in `frontend/src/`
- Next.js hot-reloads on file save
- Changes visible immediately in browser

### Database Schema Changes

If data model changes:
1. Update SQLModel classes in `backend/src/models/`
2. Delete database tables (or use Alembic migrations in future)
3. Restart backend
4. SQLModel recreates tables with new schema

**CAUTION**: This deletes all data. Use migrations for production.

### View Logs

**Backend Logs**:
- Uvicorn logs in Terminal 1
- Print statements visible in console
- FastAPI request logs show all API calls

**Frontend Logs**:
- Next.js logs in Terminal 2
- Browser console (F12) for client-side logs
- Network tab shows API requests/responses

---

## Part 8: Common Issues & Troubleshooting

### Issue: Backend won't start

**Symptom**: `uvicorn: command not found` or `ModuleNotFoundError`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: Database connection error

**Symptom**: `FATAL: password authentication failed` or `could not connect to server`

**Solution**:
- Verify `DATABASE_URL` in `.env` is correct
- Ensure Neon database is running (check Neon dashboard)
- Verify `sslmode=require` is in connection string
- Test connection:
  ```bash
  psql "postgresql://user:password@host/db?sslmode=require"
  ```

---

### Issue: Frontend can't connect to backend

**Symptom**: `Failed to fetch` or `CORS error` in browser console

**Solution**:
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`
- Verify CORS allowed origins in backend `.env`:
  ```env
  ALLOWED_ORIGINS=http://localhost:3000
  ```
- Restart both services

---

### Issue: JWT verification fails

**Symptom**: `401 Unauthorized` on all protected routes

**Solution**:
- Verify `BETTER_AUTH_JWKS_URL` is correct in backend `.env`
- Check Better Auth is running and accessible
- Verify JWT token is included in requests:
  - Check Network tab in browser DevTools
  - Look for `Authorization: Bearer ...` header
- Clear cookies and sign in again

---

### Issue: User can see other users' todos

**Symptom**: Todos from multiple users visible in list

**Solution**:
- **CRITICAL SECURITY ISSUE**: User isolation broken
- Verify service layer filters by `user_id` from JWT
- Check queries include: `WHERE user_id = <authenticated_user_id>`
- Review `backend/src/services/task_service.py`
- Run two-user tests to verify isolation

---

### Issue: Port already in use

**Symptom**: `Address already in use` or `Port 3000/8000 is already in use`

**Solution**:
```bash
# Find process using port
# macOS/Linux:
lsof -i :8000
lsof -i :3000

# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process or use different port
uvicorn src.main:app --reload --port 8001
npm run dev -- -p 3001
```

---

## Part 9: Environment Variables Reference

### Backend `.env`

| Variable                 | Required | Description                          | Example                                     |
| ------------------------ | -------- | ------------------------------------ | ------------------------------------------- |
| DATABASE_URL             | Yes      | Neon PostgreSQL connection string    | `postgresql://user:pass@host/db?sslmode=require` |
| BETTER_AUTH_SECRET       | Yes      | Better Auth secret key               | `your-secret-key`                           |
| BETTER_AUTH_JWKS_URL     | Yes      | JWKS endpoint for JWT verification   | `https://auth.example.com/.well-known/jwks.json` |
| BETTER_AUTH_BASE_URL     | Yes      | Better Auth base URL                 | `https://auth.example.com`                  |
| ALLOWED_ORIGINS          | Yes      | CORS allowed origins (comma-separated) | `http://localhost:3000`                   |
| ENVIRONMENT              | No       | Environment name                     | `development`                               |

### Frontend `.env.local`

| Variable                      | Required | Description          | Example                        |
| ----------------------------- | -------- | -------------------- | ------------------------------ |
| NEXT_PUBLIC_API_URL           | Yes      | Backend API base URL | `http://localhost:8000`        |
| NEXT_PUBLIC_BETTER_AUTH_URL   | Yes      | Better Auth base URL | `https://auth.example.com`     |
| NEXT_PUBLIC_ENVIRONMENT       | No       | Environment name     | `development`                  |

---

## Part 10: Next Steps

Once local development is running:

1. **Review Architecture**:
   - Read `specs/001-phase-ii-full-stack-web/plan.md`
   - Understand backend layers (routes/services/models)
   - Understand frontend structure (pages/components/lib)

2. **Explore API Documentation**:
   - http://localhost:8000/docs - Interactive Swagger UI
   - Test endpoints directly from browser
   - Review request/response schemas

3. **Run Tests** (if implemented):
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

4. **Make Changes**:
   - Follow spec-driven development principles
   - Update specs before implementing
   - Create PHRs for significant changes
   - Run tests after changes

5. **Deploy** (when ready):
   - Backend: Docker container on Railway/Render/Fly.io
   - Frontend: Deploy to Vercel (optimized for Next.js)
   - Database: Already on Neon (no additional setup)

---

## Part 11: Development Best Practices

- **Never commit secrets**: Use `.env` and `.env.local` (in `.gitignore`)
- **Always verify JWT**: Never trust user_id from request body
- **Test user isolation**: Critical security requirement
- **Use type hints**: Python type hints and TypeScript types
- **Follow REST conventions**: Proper HTTP methods and status codes
- **Log appropriately**: Debug info in development, minimal in production
- **Handle errors gracefully**: User-friendly messages, never expose internals

---

## Getting Help

- **Documentation**: Read specs in `specs/001-phase-ii-full-stack-web/`
- **API Reference**: http://localhost:8000/docs
- **Constitution**: `.specify/memory/constitution.md`
- **CLAUDE.md**: Project-specific guidance

---

**Quickstart Status**: Complete. Follow steps above for local development setup.
