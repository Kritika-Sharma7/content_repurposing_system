# Deployment Guide

## Overview
This guide covers deploying both the backend (Python FastAPI) and frontend (React) for production.

## Quick Start

### Local Development
```bash
# Backend
python api_server.py

# Frontend
cd react-ui
npm run dev
```

### Production Deployment

## Backend Deployment Options

### Option 1: Railway / Render / Heroku

1. **Set environment variables:**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `PORT` - Will be set automatically (usually 8000 or assigned by platform)

2. **Deploy backend:**
   ```bash
   # The backend will run on: https://your-backend.railway.app
   ```

3. **CORS Configuration:**
   The backend (`api_server.py` lines 70-82) already allows:
   - localhost:5173 (Vite dev)
   - localhost:3000 (React dev)
   - *.vercel.app (Vercel deployments)

   **Add your production frontend domain:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "http://127.0.0.1:5173",
           "http://localhost:3000",
           "http://127.0.0.1:3000",
           "https://your-frontend-domain.com",  # Add this
       ],
       ...
   )
   ```

### Option 2: Docker Deployment

Create `Dockerfile` in project root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["python", "api_server.py"]
```

Deploy with:
```bash
docker build -t content-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key content-api
```

## Frontend Deployment Options

### Option 1: Vercel (Recommended)

1. **Set environment variable in Vercel:**
   - `VITE_API_BASE_URL` = `https://your-backend.railway.app`

2. **Deploy:**
   ```bash
   cd react-ui
   npm run build
   # Connect to Vercel and deploy
   ```

3. **Vercel will automatically:**
   - Build the React app
   - Serve static files
   - Use the environment variable you set

### Option 2: Netlify

1. **Build settings:**
   - Build command: `cd react-ui && npm install && npm run build`
   - Publish directory: `react-ui/dist`

2. **Environment variables:**
   - `VITE_API_BASE_URL` = `https://your-backend.railway.app`

### Option 3: Static hosting (AWS S3, Cloudflare Pages, etc.)

1. **Build the frontend:**
   ```bash
   cd react-ui
   
   # Set production API URL
   echo "VITE_API_BASE_URL=https://your-backend.railway.app" > .env
   
   npm run build
   # Output will be in react-ui/dist/
   ```

2. **Upload `dist/` folder to your hosting service**

## Environment Configuration

### Development (.env)
```bash
# react-ui/.env
VITE_API_BASE_URL=http://localhost:8000
```

### Production
Set environment variables in your deployment platform:

**Vercel/Netlify:**
- Dashboard → Settings → Environment Variables
- Add: `VITE_API_BASE_URL` = `https://your-backend-url.com`

**Railway/Render (Backend):**
- Add: `OPENAI_API_KEY` = `your-openai-key`
- Add: `PORT` = `8000` (or let platform assign)

## Architecture Options

### Same Domain Deployment
If you want frontend and backend on the same domain:

**Frontend:** `https://yourdomain.com`  
**Backend:** `https://yourdomain.com/api`

Set up a reverse proxy (nginx, Cloudflare Workers, Vercel rewrites):

```json
// vercel.json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    }
  ]
}
```

Then set:
```bash
VITE_API_BASE_URL=""  # Empty = same domain
```

### Separate Domains (Current Setup)
**Frontend:** `https://your-frontend.vercel.app`  
**Backend:** `https://your-backend.railway.app`

Set:
```bash
VITE_API_BASE_URL=https://your-backend.railway.app
```

## Deployment Checklist

### Backend:
- [ ] Deploy to Railway/Render/Heroku
- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Update CORS to include frontend domain
- [ ] Test health endpoint: `https://your-backend.com/api/health`

### Frontend:
- [ ] Set `VITE_API_BASE_URL` to backend URL
- [ ] Build and deploy to Vercel/Netlify
- [ ] Test in production browser
- [ ] Check browser console for any API errors

## Testing Deployment

1. **Test backend health:**
   ```bash
   curl https://your-backend.railway.app/api/health
   # Should return: {"status":"ok","service":"multi-agent-content-api","version":"2.0.0"}
   ```

2. **Test frontend:**
   - Open `https://your-frontend.vercel.app`
   - Open browser DevTools (F12) → Network tab
   - Click "Transform Content"
   - Check that API calls go to correct backend URL
   - Should see: `POST https://your-backend.railway.app/api/pipeline-run`

## Common Issues

### Issue: API calls fail with CORS error
**Fix:** Add your frontend domain to CORS in `api_server.py`

### Issue: 404 on API routes
**Fix:** Make sure backend is deployed and `VITE_API_BASE_URL` is correct

### Issue: Environment variables not working
**Fix:** Rebuild frontend after changing environment variables (Vite bakes them in at build time)

### Issue: "undefined/api/pipeline-run"
**Fix:** Set `VITE_API_BASE_URL` environment variable in your deployment platform

## Recommended Stack

**Free tier deployment:**
- Backend: Railway (500 hours/month free) or Render (750 hours/month free)
- Frontend: Vercel (unlimited free for hobby projects)
- Total cost: $0/month (within free tiers)

**Production deployment:**
- Backend: Railway Pro ($5/month) or AWS/GCP
- Frontend: Vercel Pro ($20/month) or Cloudflare Pages (free)
- Database: If needed, add PostgreSQL (Railway $5/month)

## Need Help?

Check these files:
- `react-ui/.env.example` - Environment variable template
- `api_server.py` - Backend configuration (CORS, ports)
- `react-ui/src/pages/CleanDemoPage.jsx` - API_BASE configuration
