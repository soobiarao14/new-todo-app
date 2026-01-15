# Hugging Face Spaces Deployment Guide

This guide will help you deploy your FastAPI backend to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (free)
2. Your backend code ready to deploy
3. A Neon PostgreSQL database (already configured)

## Step-by-Step Deployment

### 1. Create a New Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: `todo-apps` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free tier)
3. Click **Create Space**

### 2. Configure Space Settings

After creating your Space, go to **Settings** → **Variables and secrets**:

#### Add these secrets (click "New secret"):

| Name | Value | Description |
|------|-------|-------------|
| `APP_ENV` | `production` | Tells backend to use production config |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_ma7XvDi1rHRt@ep-calm-forest-ahx7y784-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require` | Your Neon DB connection string |
| `BETTER_AUTH_SECRET` | Generate a secure random string | JWT secret (min 32 chars) |
| `BETTER_AUTH_JWKS_URL` | `https://sobiarao-todo-apps.hf.space/.well-known/jwks.json` | JWKS endpoint URL |
| `BETTER_AUTH_BASE_URL` | `https://sobiarao-todo-apps.hf.space` | Your Space URL |
| `ALLOWED_ORIGINS` | `https://new-todo-app-kappa.vercel.app,http://localhost:3000` | Frontend URLs |
| `ENVIRONMENT` | `production` | Environment name |

**Important**: Replace `sobiarao-todo-apps` with your actual Space name if different.

#### Generate a secure BETTER_AUTH_SECRET:

Run this in your terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Deploy Your Code

You have two options:

#### Option A: Push to Git (Recommended)

1. **Initialize git in backend directory** (if not already done):
```bash
cd backend
git init
```

2. **Add Hugging Face Space as remote**:
```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/todo-apps
```

Replace `YOUR_USERNAME` with your Hugging Face username.

3. **Commit and push**:
```bash
git add .
git commit -m "Initial deployment to Hugging Face Spaces"
git push space main
```

#### Option B: Upload Files Directly

1. Go to your Space page on Hugging Face
2. Click **Files** → **Add file** → **Upload files**
3. Upload these essential files:
   - `Dockerfile`
   - `requirements.txt`
   - `README_HF.md` (rename to `README.md` before uploading)
   - `src/` (entire directory)
   - `.env.production` (optional, secrets are preferred)
   - `.dockerignore`

### 4. Monitor Deployment

1. Go to your Space page
2. Click on **Logs** to see build progress
3. Wait for the build to complete (5-10 minutes for first build)
4. Look for: `Application startup complete`

### 5. Verify Deployment

Test your deployed backend:

```bash
# Test health endpoint
curl https://sobiarao-todo-apps.hf.space/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "environment": "production"
# }
```

### 6. Update Frontend Configuration

Update your Vercel frontend environment variables:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update or add:
   - `NEXT_PUBLIC_API_URL` = `https://sobiarao-todo-apps.hf.space`
   - `NEXT_PUBLIC_BETTER_AUTH_URL` = `https://sobiarao-todo-apps.hf.space`
3. Redeploy your frontend

## Troubleshooting

### Issue: Space shows "Building" for a long time

**Possible causes:**
- Large build (first build takes longer)
- Network issues

**Solution:**
- Wait 10-15 minutes
- Check build logs for errors
- If stuck, restart the Space from Settings

### Issue: 503 Service Unavailable

**Possible causes:**
1. Application failed to start
2. Missing environment variables
3. Database connection issues
4. Port mismatch (Space expects port 7860)

**Solution:**
1. Check **Logs** for error messages
2. Verify all secrets are set correctly in Space settings
3. Ensure `Dockerfile` uses port 7860
4. Check database URL is accessible
5. Restart the Space

### Issue: CORS errors from frontend

**Possible causes:**
- Frontend URL not in `ALLOWED_ORIGINS`
- Trailing slashes in URLs

**Solution:**
1. Update `ALLOWED_ORIGINS` secret in Space settings
2. Format: `https://new-todo-app-kappa.vercel.app,http://localhost:3000` (no trailing slashes)
3. Restart Space after changing secrets

### Issue: Database connection timeout

**Possible causes:**
- Invalid `DATABASE_URL`
- Neon database sleeping (free tier)

**Solution:**
1. Verify database URL is correct
2. Wake up Neon database by accessing it
3. Consider upgrading Neon plan for always-on

### Issue: Authentication not working

**Possible causes:**
- Wrong `BETTER_AUTH_BASE_URL`
- Mismatched `BETTER_AUTH_SECRET`

**Solution:**
1. Verify `BETTER_AUTH_BASE_URL` matches your Space URL exactly
2. Ensure `BETTER_AUTH_SECRET` is at least 32 characters
3. Check frontend is using the same backend URL

## Accessing Your API

Once deployed successfully:

- **API Base**: https://sobiarao-todo-apps.hf.space
- **Health Check**: https://sobiarao-todo-apps.hf.space/health
- **API Docs**: https://sobiarao-todo-apps.hf.space/docs
- **ReDoc**: https://sobiarao-todo-apps.hf.space/redoc

## Files Required for Deployment

Make sure these files are in your backend directory:

- ✅ `Dockerfile` (defines how to build the container)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `README_HF.md` (Space metadata - rename to README.md)
- ✅ `.dockerignore` (excludes unnecessary files)
- ✅ `src/` directory (your application code)
- ✅ `.env.production` (optional if using Space secrets)

## Space Configuration (README.md frontmatter)

The `README_HF.md` file contains Space metadata. When uploading, rename it to `README.md`. It tells Hugging Face:

- This is a Docker-based Space
- App runs on port 7860
- Space title, emoji, colors

## Updating Your Deployment

To update your deployed backend:

1. Make changes to your code locally
2. Test locally first
3. Commit changes:
```bash
git add .
git commit -m "Update: description of changes"
git push space main
```
4. Hugging Face will automatically rebuild and redeploy

## Monitoring

- **Logs**: Check real-time logs in Space interface
- **Health**: Monitor `/health` endpoint
- **Metrics**: View Space metrics in HF dashboard

## Cost

- **Free tier**: CPU basic (sufficient for small apps)
- **Paid tiers**: Upgrade for better performance, GPU, or always-on

## Security Best Practices

1. ✅ Use Space secrets for sensitive data (not .env files)
2. ✅ Keep `BETTER_AUTH_SECRET` secure and random
3. ✅ Use HTTPS only (Hugging Face provides this)
4. ✅ Restrict `ALLOWED_ORIGINS` to your frontend only
5. ✅ Keep database credentials secure
6. ✅ Use separate databases for dev and production

## Next Steps

After successful deployment:

1. ✅ Test all API endpoints
2. ✅ Verify CORS with your frontend
3. ✅ Test authentication flow end-to-end
4. ✅ Create some test todos
5. ✅ Monitor logs for any issues
6. ✅ Update documentation with your Space URL

## Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Docker Spaces Guide: https://huggingface.co/docs/hub/spaces-sdks-docker

---

**Your backend should now be running on Hugging Face Spaces!** 🚀
