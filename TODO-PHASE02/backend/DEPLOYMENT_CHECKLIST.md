# Hugging Face Spaces Deployment Checklist

Use this checklist to ensure successful deployment of your backend to Hugging Face Spaces.

## Pre-Deployment Checklist

- [ ] All code changes committed locally
- [ ] Backend tested and working on localhost
- [ ] Database (Neon) is accessible and has tables created
- [ ] All required files present in backend directory:
  - [ ] `Dockerfile`
  - [ ] `requirements.txt` (with email-validator)
  - [ ] `README_HF.md`
  - [ ] `.dockerignore`
  - [ ] `src/` directory with all code
  - [ ] `.env.production` (optional)

## Hugging Face Space Setup

- [ ] Hugging Face account created
- [ ] New Space created with Docker SDK
- [ ] Space name noted: `__________________`

## Environment Variables/Secrets Configuration

Go to Space Settings → Variables and secrets, and add:

- [ ] `APP_ENV` = `production`
- [ ] `DATABASE_URL` = Your Neon connection string
- [ ] `BETTER_AUTH_SECRET` = Generated secure random string (32+ chars)
- [ ] `BETTER_AUTH_JWKS_URL` = `https://YOUR-SPACE-NAME.hf.space/.well-known/jwks.json`
- [ ] `BETTER_AUTH_BASE_URL` = `https://YOUR-SPACE-NAME.hf.space`
- [ ] `ALLOWED_ORIGINS` = `https://new-todo-app-kappa.vercel.app,http://localhost:3000`
- [ ] `ENVIRONMENT` = `production`

**Remember to replace `YOUR-SPACE-NAME` with your actual Space name!**

## Code Deployment

Choose one method:

### Method A: Git Push
- [ ] Git initialized in backend directory
- [ ] Hugging Face Space added as remote
- [ ] Code committed
- [ ] Pushed to Space: `git push space main`

### Method B: Direct Upload
- [ ] Files uploaded via Hugging Face web interface
- [ ] README_HF.md renamed to README.md before uploading

## Post-Deployment Verification

- [ ] Build completed successfully (check Logs)
- [ ] Space status shows "Running"
- [ ] No error messages in logs

## Testing Deployed Backend

Test these endpoints (replace with your Space URL):

- [ ] Root endpoint: `curl https://YOUR-SPACE-NAME.hf.space/`
  - Expected: `{"status": "ok", "message": "Todo API is running", ...}`

- [ ] Health endpoint: `curl https://YOUR-SPACE-NAME.hf.space/health`
  - Expected: `{"status": "healthy", "database": "connected", "environment": "production"}`

- [ ] API Docs: Visit `https://YOUR-SPACE-NAME.hf.space/docs`
  - Expected: Interactive Swagger UI loads

## Frontend Integration

- [ ] Vercel environment variables updated:
  - [ ] `NEXT_PUBLIC_API_URL` = `https://YOUR-SPACE-NAME.hf.space`
  - [ ] `NEXT_PUBLIC_BETTER_AUTH_URL` = `https://YOUR-SPACE-NAME.hf.space`

- [ ] Frontend redeployed on Vercel

- [ ] Frontend can reach backend (no CORS errors)

## End-to-End Testing

- [ ] Can open frontend: https://new-todo-app-kappa.vercel.app
- [ ] Can sign up new user
- [ ] Can log in
- [ ] Can create a todo
- [ ] Can view todos
- [ ] Can update todo
- [ ] Can delete todo
- [ ] Can log out

## Common Issues Checklist

If something doesn't work, check:

- [ ] All environment secrets are set correctly in Space settings
- [ ] Space is showing "Running" status (not "Building" or "Error")
- [ ] Logs show "Application startup complete"
- [ ] Database URL is correct and accessible
- [ ] `ALLOWED_ORIGINS` includes your exact frontend URL
- [ ] `BETTER_AUTH_BASE_URL` matches your Space URL exactly
- [ ] No trailing slashes in URLs
- [ ] Port 7860 is used in Dockerfile

## Maintenance

- [ ] Bookmark your Space URL for easy access
- [ ] Save deployment configuration for future reference
- [ ] Document any custom changes made
- [ ] Set up monitoring/alerting if needed

## Troubleshooting Steps

If deployment fails:

1. [ ] Check build logs for specific errors
2. [ ] Verify all secrets are correctly set
3. [ ] Test database connection separately
4. [ ] Ensure Dockerfile uses correct port (7860)
5. [ ] Restart Space from Settings
6. [ ] Check Hugging Face status page for outages

## Success Criteria

Your deployment is successful when:

✅ Space status is "Running"
✅ Health endpoint returns 200 OK
✅ API docs are accessible
✅ Frontend can communicate with backend
✅ Authentication works end-to-end
✅ CRUD operations on todos work

---

**Deployment Date**: _______________
**Space URL**: https://_____________________.hf.space
**Status**: ⬜ In Progress | ⬜ Completed | ⬜ Failed

**Notes:**
_____________________________________________________________________
_____________________________________________________________________
_____________________________________________________________________
