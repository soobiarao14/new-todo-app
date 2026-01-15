---
title: Todo App Backend
emoji: ✨
colorFrom: purple
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
---

# Todo App Backend - Phase II

Full-stack Todo Application RESTful API with JWT Authentication.

## Configuration

This Space requires the following environment variables/secrets to be set in Hugging Face Spaces settings:

### Required Secrets

1. **APP_ENV** (set to `production`)
2. **DATABASE_URL** - Your Neon PostgreSQL connection string
3. **BETTER_AUTH_SECRET** - JWT secret key (minimum 32 characters)
4. **BETTER_AUTH_JWKS_URL** - `https://sobiarao-todo-apps.hf.space/.well-known/jwks.json`
5. **BETTER_AUTH_BASE_URL** - `https://sobiarao-todo-apps.hf.space`
6. **ALLOWED_ORIGINS** - `https://new-todo-app-kappa.vercel.app,http://localhost:3000`
7. **ENVIRONMENT** - `production`

## API Endpoints

### Health Check
- `GET /` - Basic status check
- `GET /health` - Detailed health information

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user info

### Todos
- `GET /api/tasks` - Get all todos
- `POST /api/tasks` - Create new todo
- `GET /api/tasks/{id}` - Get specific todo
- `PUT /api/tasks/{id}` - Update todo
- `DELETE /api/tasks/{id}` - Delete todo

## API Documentation

- **Swagger UI**: https://sobiarao-todo-apps.hf.space/docs
- **ReDoc**: https://sobiarao-todo-apps.hf.space/redoc

## Technologies

- FastAPI
- PostgreSQL (Neon)
- JWT Authentication
- Docker

## Frontend

This backend connects to: https://new-todo-app-kappa.vercel.app
