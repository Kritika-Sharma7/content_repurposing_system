@echo off
echo Starting Backend and Frontend...
cd /d "%~dp0"
start "Backend API" cmd /k python api_server.py
start "Frontend Dev" cmd /k "cd react-ui && npm run dev"
echo.
echo Both servers are starting in separate windows...
echo Backend: Python API Server
echo Frontend: React + Vite Dev Server
echo.
pause
