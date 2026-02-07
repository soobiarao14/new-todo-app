# Todo App - Phase II Full-Stack Web Application

A modern, full-stack todo management application with JWT authentication and strict user isolation.

## ✨ Features

- **User Authentication**: Secure signup/signin with JWT tokens
- **Todo Management**: Full CRUD operations (Create, Read, Update, Delete)
- **User Isolation**: Strict data segregation - users can only access their own todos
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Modern Stack**: FastAPI backend + Next.js frontend
- **Type Safety**: TypeScript frontend + Pydantic backend validation

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11+
- **Database**: SQLite (dev) / Neon PostgreSQL (production)
- **ORM**: SQLModel for type-safe database operations
- **Authentication**: JWT with HS256 (simplified) / RS256 with Better Auth (production)
- **Validation**: Pydantic schemas with field-level validation

### Frontend (Next.js)
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **API Client**: Fetch with automatic JWT handling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlmodel psycopg2-binary python-jose python-dotenv pydantic httpx passlib

# Environment is already configured in .env file (SQLite for local development)

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Environment is already configured in .env.local file

# Start the development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📝 Usage

1. **Sign Up**: Create a new account at http://localhost:3000/signup
2. **Sign In**: Login with your credentials at http://localhost:3000/signin
3. **Manage Todos**:
   - View all your todos on the dashboard
   - Click "Add Todo" to create new tasks
   - Click "Edit" to modify existing todos
   - Click "Delete" to remove todos
   - Click the checkbox to toggle completion status
4. **Sign Out**: Click "Sign Out" to end your session

## 🔒 Security Features

- **JWT Authentication**: All API requests require valid JWT tokens
- **User Isolation**: Database-level filtering ensures users can only access their own data
- **Password Hashing**: Passwords hashed with bcrypt (cost factor 12)
- **httpOnly Cookies**: JWT tokens stored in secure httpOnly cookies
- **CORS Protection**: Whitelist-based CORS configuration
- **Input Validation**: Server-side and client-side validation
- **Error Handling**: Secure error messages that don't expose internal details

## 📦 Project Structure

```
TODO-PHASE02/
├── backend/
│   ├── src/
│   │   ├── auth/           # Authentication logic (JWT, config)
│   │   ├── models/         # SQLModel entities (User, Todo)
│   │   ├── routes/         # API endpoints (auth, todos)
│   │   ├── services/       # Business logic (TodoService)
│   │   ├── middleware/     # Auth & error handling middleware
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── db.py           # Database configuration
│   │   └── main.py         # FastAPI application entry point
│   ├── .env                # Environment variables (configured)
│   └── pyproject.toml      # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages (signup, signin, todos)
│   │   ├── components/     # Reusable UI components
│   │   ├── contexts/       # React contexts (AuthContext)
│   │   ├── lib/            # API client utilities
│   │   └── types/          # TypeScript type definitions
│   ├── .env.local          # Frontend environment variables (configured)
│   └── package.json        # Node.js dependencies
│
├── specs/                  # Feature specifications and planning
├── history/                # Implementation history (PHRs)
├── QUICKSTART.md           # Detailed setup guide
└── README.md               # This file
```

## 🧪 Testing

### Manual Testing
1. **User Isolation**:
   - Create two users (User A and User B)
   - Create todos for each user
   - Verify User A cannot see or access User B's todos
   - Test by manually attempting to access other user's todo IDs

2. **Authentication Flow**:
   - Test signup with valid/invalid data
   - Test signin with correct/incorrect credentials
   - Test protected route access without authentication
   - Test token expiration

3. **CRUD Operations**:
   - Create todos with title only and with description
   - Update todos (title, description, or both)
   - Delete todos with confirmation
   - Toggle completion status

### API Testing
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
DATABASE_URL=sqlite:///./todo.db  # or PostgreSQL connection string
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_JWKS_URL=http://localhost:8000/.well-known/jwks.json
BETTER_AUTH_BASE_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### Frontend Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

## 📚 API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/signin` - Sign in with credentials
- `POST /auth/signout` - Sign out and clear session
- `GET /auth/session` - Get current session info

### Todos (Protected)
- `GET /api/tasks` - List all todos for authenticated user
- `GET /api/tasks/{id}` - Get single todo
- `POST /api/tasks` - Create new todo
- `PUT /api/tasks/{id}` - Update todo
- `DELETE /api/tasks/{id}` - Delete todo
- `PATCH /api/tasks/{id}/complete` - Toggle completion status

## 🎯 Phase II Scope

**Included**:
- ✅ User authentication (signup, signin, signout)
- ✅ JWT-based session management
- ✅ Full CRUD operations for todos
- ✅ User isolation at database level
- ✅ Responsive web interface
- ✅ Error handling and validation
- ✅ httpOnly cookie storage

**Not Included** (Future Phases):
- ❌ AI features or smart suggestions
- ❌ Real-time collaboration (WebSockets)
- ❌ Background jobs or scheduled tasks
- ❌ Advanced analytics or reporting
- ❌ Todo sharing or permissions
- ❌ Categories, tags, or priorities
- ❌ Search and filtering
- ❌ Email verification or password recovery

## 🐛 Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check that all dependencies are installed: `pip list`
- Verify .env file exists with correct values
- Check port 8000 is not already in use

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check .env.local file exists
- Verify port 3000 is not in use

### Cannot sign in
- Check backend is running on port 8000
- Verify CORS is configured correctly (check browser console)
- Ensure credentials are correct
- Check backend logs for errors

### User isolation not working
- This is a **CRITICAL SECURITY ISSUE**
- Check TodoService methods filter by user_id
- Verify user_id comes from JWT, not request body
- Review backend logs for errors

## 📄 License

This project is part of the "Evolution of Todo" hackathon series - Phase II.

## 🤝 Contributing

This is a hackathon project following strict Spec-Driven Development principles. All changes must:
1. Start with a written specification
2. Follow the project constitution
3. Include PHR documentation
4. Maintain user isolation security

For more details, see:
- `specs/001-phase-ii-full-stack-web/spec.md` - Feature specification
- `specs/001-phase-ii-full-stack-web/plan.md` - Technical plan
- `QUICKSTART.md` - Detailed setup guide
- `.specify/memory/constitution.md` - Project governance

---

**Built with**: FastAPI • Next.js • TypeScript • Tailwind CSS • SQLModel • PostgreSQL
