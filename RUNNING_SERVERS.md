# 🚀 Starting the Multi-Agent Content System

## Quick Start

### Option 1: Start Both Servers at Once (Recommended)
Simply double-click:
```
start-all.bat
```

This will open two command windows:
- **Backend API Server** (Python/FastAPI) on port 8000
- **Frontend Dev Server** (React/Vite) on port 5173

---

## Manual Start

### Option 2: Start Individually

**Backend:**
```
start-backend.bat
```
or
```
python api_server.py
```

**Frontend:**
```
start-frontend.bat
```
or
```
cd react-ui
npm run dev
```

---

## Access URLs

Once both servers are running:

🔹 **Backend API:**
- Base URL: http://localhost:8000
- Health Check: http://localhost:8000/api/health
- API Docs: http://localhost:8000/docs (Swagger UI)

🔹 **Frontend UI:**
- Web App: http://localhost:5173

---

## Verification

### Test Backend is Running
Open browser to: http://localhost:8000/api/health

Expected response:
```json
{
  "status": "ok",
  "service": "multi-agent-content-api",
  "version": "2.0.0"
}
```

### Test Frontend is Running
Open browser to: http://localhost:5173

You should see the Multi-Agent Content UI.

---

## Troubleshooting

### Backend Issues

**Problem:** "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** "OPENAI_API_KEY not set"
**Solution:**
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=your-key-here`

### Frontend Issues

**Problem:** "npm not found"
**Solution:** Install Node.js from https://nodejs.org

**Problem:** "Dependencies not installed"
**Solution:**
```bash
cd react-ui
npm install
```

**Problem:** "Port 5173 already in use"
**Solution:** The frontend will automatically use the next available port (5174, 5175, etc.)

---

## Stopping the Servers

### If Started with start-all.bat
Simply close both command windows.

### If Running in Terminal
Press `Ctrl+C` in each terminal window.

---

## Next Steps

Once both servers are running:

1. Open http://localhost:5173 in your browser
2. Paste your long-form content
3. Customize preferences (tone, audience, platforms)
4. Click "Generate Content"
5. View your optimized LinkedIn, Twitter, and Newsletter content!

---

## Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │  HTTP   │  FastAPI Backend │
│  (Port 5173)    │ ───────>│  (Port 8000)     │
└─────────────────┘         └──────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  4-Agent        │
                            │  Pipeline       │
                            │  - Summarizer   │
                            │  - Formatter    │
                            │  - Reviewer     │
                            │  - Refiner      │
                            └─────────────────┘
```

---

## Environment Variables

Required in `.env` file:
```
OPENAI_API_KEY=your-key-here
```

Optional:
```
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
```

---

## Development Mode vs Production

**Current Setup: Development Mode**
- Backend: Python with auto-reload
- Frontend: Vite dev server with HMR (Hot Module Replacement)
- CORS: Enabled for localhost

**For Production:**
```bash
# Build frontend
cd react-ui
npm run build

# Serve with production server
# (configure nginx, gunicorn, etc.)
```

---

**Need Help?**
- Check logs in the command windows
- Review IMPLEMENTATION_SUMMARY.md for architecture details
- Test pipeline: `python test_pipeline.py`
