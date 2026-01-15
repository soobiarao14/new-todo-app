# Todo Application Backend

Phase II Full-Stack Todo Application - RESTful API with JWT Authentication

## Quick Start

### Local Development

**Windows:**
```bash
run-local.bat
```

**Mac/Linux:**
```bash
./run-local.sh
```

The backend will start on `http://localhost:8000`

### Testing Production Configuration Locally

**Windows:**
```bash
run-production.bat
```

**Mac/Linux:**
```bash
./run-production.sh
```

## Manual Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

The backend uses environment-specific configuration files:

- **`.env.local`** - For local development (default)
- **`.env.production`** - For production deployment

See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for detailed configuration instructions.

### 5. Run the Server

**Local Development:**
```bash
uvicorn src.main:app --reload --port 8000
```

**Production:**
```bash
APP_ENV=production uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── auth/              # Authentication modules
│   ├── middleware/        # Custom middleware
│   ├── models/           # Database models
│   ├── routes/           # API endpoints
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── config.py         # Environment configuration loader
│   ├── db.py             # Database connection
│   └── main.py           # FastAPI application
├── tests/                # Test files
├── .env.local            # Local environment config
├── .env.production       # Production environment config
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
├── ENVIRONMENT_SETUP.md  # Detailed setup guide
└── README.md            # This file
```

## Environment Variables

Required environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT tokens
- `BETTER_AUTH_JWKS_URL` - JWKS endpoint URL
- `BETTER_AUTH_BASE_URL` - Base URL for the backend
- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `ENVIRONMENT` - Environment name (development/production)

## Deployment

### Hugging Face Spaces

**Quick Start:**
1. Push your code to a Git repository
2. Create a new Hugging Face Space (Docker SDK)
3. Set environment secrets (see deployment guide)
4. The application will automatically use production configuration

**Deployment Files:**
- `Dockerfile` - Container build configuration
- `README_HF.md` - Space metadata (rename to README.md when deploying)
- `.dockerignore` - Build optimization
- `HUGGINGFACE_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist

**📖 See [HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md) for complete deployment instructions.**

**✅ Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) to ensure nothing is missed.**

## API Endpoints

### Authentication

- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (invalidate token)
- `GET /auth/me` - Get current user info

### Todos

- `GET /api/tasks` - Get all todos for the current user
- `POST /api/tasks` - Create a new todo
- `GET /api/tasks/{id}` - Get a specific todo
- `PUT /api/tasks/{id}` - Update a todo
- `DELETE /api/tasks/{id}` - Delete a todo

## Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "development"
}
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
pylint src/
```

## Technologies

- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database ORM
- **PostgreSQL** - Database (Neon)
- **JWT** - Token-based authentication
- **Uvicorn** - ASGI server

## Troubleshooting

See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for common issues and solutions.

## License

MIT
