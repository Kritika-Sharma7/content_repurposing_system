@echo off
echo Starting API server in MOCK MODE (no API costs)...
echo.
echo This mode uses mock data instead of real OpenAI API calls
echo Perfect for UI development without burning credits!
echo.

REM Set mock mode environment variable
set USE_MOCK_DATA=true

REM Start the API server
python api_server.py