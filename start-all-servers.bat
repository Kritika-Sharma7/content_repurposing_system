@echo off
echo ============================================
echo Starting Multi-Agent Content System
echo ============================================
echo.

echo [1/2] Starting Backend API Server...
start "Backend API" cmd /k "cd /d "%~dp0" && python api_server.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Dev Server...
start "Frontend UI" cmd /k "cd /d "%~dp0\react-ui" && npm run dev"

echo.
echo ============================================
echo Both servers are starting!
echo ============================================
echo.
echo Backend API:  http://localhost:8000
echo Frontend UI:  http://localhost:5173
echo.
echo Press any key to close this window (servers will keep running)
pause >nul
