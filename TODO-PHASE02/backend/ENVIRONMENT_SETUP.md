# Environment Setup Guide

This guide explains how to configure and run the backend in different environments (local development and production).

## Environment Files

The backend supports three environment configuration files:

1. **`.env.local`** - Local development configuration
2. **`.env.production`** - Production deployment configuration (Hugging Face Spaces)
3. **`.env`** - Fallback configuration (not tracked in git)

## Configuration Loading

The application automatically loads the correct environment file based on the `APP_ENV` environment variable:

- **Local Development** (default): Loads `.env.local`
- **Production**: Loads `.env.production` when `APP_ENV=production`

### Environment Variables

Each environment file contains:

```env
# Database Configuration
DATABASE_URL=postgresql://...

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_JWKS_URL=https://your-backend-url/.well-known/jwks.json
BETTER_AUTH_BASE_URL=https://your-backend-url

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-url,http://localhost:3000

# Environment
ENVIRONMENT=development|production
```

## Running Locally

### Option 1: Default (Automatic)

Simply run the application - it will automatically use `.env.local`:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
uvicorn src.main:app --reload --port 8000
```

### Option 2: Explicit Local Environment

Set the `APP_ENV` variable explicitly:

```bash
# On Unix/Mac
export APP_ENV=local
uvicorn src.main:app --reload --port 8000

# On Windows (PowerShell)
$env:APP_ENV="local"
uvicorn src.main:app --reload --port 8000

# On Windows (CMD)
set APP_ENV=local
uvicorn src.main:app --reload --port 8000
```

## Running in Production (Hugging Face Spaces)

### Set the Environment Variable

On Hugging Face Spaces, set the `APP_ENV` secret/environment variable:

1. Go to your Hugging Face Space settings
2. Add a new secret: `APP_ENV=production`
3. The application will automatically load `.env.production`

### Alternative: Using System Environment Variables

If you prefer not to commit `.env.production`, you can set all variables as Hugging Face Spaces secrets:

- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_JWKS_URL`
- `BETTER_AUTH_BASE_URL`
- `ALLOWED_ORIGINS`
- `ENVIRONMENT`

## Frontend Configuration

### Local Development

Your local frontend should connect to:
```
http://localhost:8000
```

### Production (Vercel)

Your Vercel frontend should connect to:
```
https://sobiarao-todo-apps.hf.space
```

Make sure your frontend environment variables are set correctly:

**.env.local** (for local development):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**.env.production** (for Vercel deployment):
```env
NEXT_PUBLIC_API_URL=https://sobiarao-todo-apps.hf.space
```

## CORS Configuration

The backend is configured to accept requests from:

### Local Environment (`.env.local`):
- `http://localhost:3000`
- `http://localhost:3001`

### Production Environment (`.env.production`):
- `https://new-todo-app-kappa.vercel.app` (your Vercel frontend)
- `http://localhost:3000` (for local testing against production)
- `http://localhost:3001` (for local testing against production)

## Testing the Setup

### 1. Test Local Backend

```bash
# Start the backend locally
uvicorn src.main:app --reload --port 8000

# In another terminal, test the health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "development"
}
```

### 2. Test Production Backend

```bash
curl https://sobiarao-todo-apps.hf.space/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "production"
}
```

### 3. Test CORS

From your frontend, make a request to the backend. The request should succeed without CORS errors.

## Troubleshooting

### Issue: "Missing required environment variables"

**Solution**: Ensure your environment file (`.env.local` or `.env.production`) contains all required variables:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_JWKS_URL`
- `BETTER_AUTH_BASE_URL`

### Issue: CORS errors in browser

**Solution**:
1. Check that your frontend URL is listed in `ALLOWED_ORIGINS`
2. Ensure the URLs don't have trailing slashes
3. Verify the backend is using the correct environment file

### Issue: Backend loads wrong environment

**Solution**:
1. Check the console output when the backend starts - it shows which file was loaded
2. Verify the `APP_ENV` environment variable is set correctly
3. Ensure the environment file exists and has correct permissions

## Security Notes

1. **Never commit** `.env` or `.env.local` to git (already in `.gitignore`)
2. **Keep secrets secure**: Use strong, unique values for `BETTER_AUTH_SECRET`
3. **Production secrets**: Use Hugging Face Spaces secrets for sensitive production values
4. **Database credentials**: Keep `DATABASE_URL` secure and use connection pooling

## Summary

- **Local Development**: Just run `uvicorn` - it uses `.env.local` automatically
- **Production**: Set `APP_ENV=production` on Hugging Face Spaces
- **Frontend**: Update frontend env vars to point to the correct backend URL
- **Testing**: Use `/health` endpoint to verify configuration
