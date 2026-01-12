# Environment Configuration Guide

This document explains how environment variables are configured for different environments (localhost and Vercel production).

## 📁 Environment Files

### `.env.development` (Localhost)
- **Purpose**: Automatically loaded when running `npm run dev`
- **Backend URL**: `http://localhost:8000`
- **Committed to Git**: ✅ Yes
- **Use Case**: Local development with local backend

### `.env.production` (Production)
- **Purpose**: Automatically loaded when running `npm run build`
- **Backend URL**: `https://sobiarao-todo-apps.hf.space`
- **Committed to Git**: ✅ Yes
- **Use Case**: Production builds and Vercel deployment

### `.env.local` (Personal Overrides)
- **Purpose**: Override any environment variables locally
- **Committed to Git**: ❌ No (kept private)
- **Use Case**: Personal local settings that differ from team defaults
- **Priority**: Highest (overrides all other env files)

### `.env.example` (Template)
- **Purpose**: Documentation and template for required variables
- **Committed to Git**: ✅ Yes
- **Use Case**: Reference for new developers

## 🔧 Environment Variables

### `NEXT_PUBLIC_API_URL`
The base URL for your backend API.

- **Development**: `http://localhost:8000`
- **Production**: `https://sobiarao-todo-apps.hf.space`

### `NEXT_PUBLIC_BETTER_AUTH_URL`
The URL for Better Auth (if using authentication).

- **Development**: `http://localhost:8000`
- **Production**: `https://sobiarao-todo-apps.hf.space`

### `NEXT_PUBLIC_ENVIRONMENT`
Identifier for the current environment.

- **Development**: `development`
- **Production**: `production`

## 🚀 Usage

### Local Development

1. Clone the repository
2. The `.env.development` file is already configured for localhost
3. Run the development server:
   ```bash
   npm run dev
   ```
4. The app will connect to `http://localhost:8000`

### Custom Local Settings

If you need to override environment variables locally:

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```
2. Modify values in `.env.local` as needed
3. `.env.local` is ignored by git and won't be committed

### Production Build (Local Testing)

To test the production build locally:

```bash
npm run build
npm start
```

This will use the production environment variables from `.env.production`.

## ☁️ Vercel Deployment

### Automatic Configuration

When you deploy to Vercel, it will automatically use the `.env.production` file for default values.

### Vercel Dashboard Configuration (Recommended)

For better security and flexibility, configure environment variables in the Vercel dashboard:

1. Go to your project on [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to: **Settings** → **Environment Variables**
3. Add the following variables:

   | Variable | Value | Environment |
   |----------|-------|-------------|
   | `NEXT_PUBLIC_API_URL` | `https://sobiarao-todo-apps.hf.space` | Production |
   | `NEXT_PUBLIC_BETTER_AUTH_URL` | `https://sobiarao-todo-apps.hf.space` | Production |
   | `NEXT_PUBLIC_ENVIRONMENT` | `production` | Production |

4. Save and redeploy your application

**Note**: Vercel environment variables override `.env.production` values.

## 🔄 Priority Order

Next.js loads environment variables in this priority (highest to lowest):

1. **Vercel Environment Variables** (in production only)
2. `.env.local` (local overrides, not committed)
3. `.env.production` or `.env.development` (based on NODE_ENV)
4. `.env` (if exists, general defaults)

## ✅ Verification

### Check Local Development
```bash
npm run dev
```
- Open browser DevTools → Network tab
- Verify API calls go to `http://localhost:8000`

### Check Production Build
```bash
npm run build
npm start
```
- Open browser DevTools → Network tab
- Verify API calls go to `https://sobiarao-todo-apps.hf.space`

### Check Vercel Deployment
1. Deploy to Vercel
2. Visit: https://new-todo-app-kappa.vercel.app/
3. Open browser DevTools → Network tab
4. Verify API calls go to `https://sobiarao-todo-apps.hf.space`
5. Test authentication and TODO operations

## ⚠️ Important Notes

### CORS Configuration
Ensure your backend at `https://sobiarao-todo-apps.hf.space` allows requests from:
- `https://new-todo-app-kappa.vercel.app` (production frontend)
- `http://localhost:3000` (local development)

### Cookies and Authentication
The app uses `credentials: "include"` for API calls, which requires proper CORS configuration on the backend:
- `Access-Control-Allow-Origin` must be set to the frontend URL
- `Access-Control-Allow-Credentials` must be `true`

### NEXT_PUBLIC_ Prefix
Variables with the `NEXT_PUBLIC_` prefix are exposed to the browser. Never store secrets or sensitive data in these variables.

## 🐛 Troubleshooting

### API calls failing in production
- Check Vercel environment variables are set correctly
- Verify backend CORS settings allow your frontend URL
- Check Network tab for exact error messages

### Environment variables not updating
- After changing Vercel environment variables, you must **redeploy**
- Clear browser cache if testing locally
- Verify you're not overriding with `.env.local`

### Backend URL has double slashes (e.g., `//auth/session`)
- Ensure backend URLs don't have trailing slashes in env files
- Or update API client to handle trailing slashes consistently

## 📚 Additional Resources

- [Next.js Environment Variables](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)
