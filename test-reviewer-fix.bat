@echo off
echo ================================================
echo CLEARING PYTHON CACHE AND TESTING REVIEWER
echo ================================================
echo.

echo Step 1: Clearing cache directories...
if exist "agents\__pycache__" rmdir /s /q "agents\__pycache__"
if exist "pipeline\__pycache__" rmdir /s /q "pipeline\__pycache__"
if exist "schemas\__pycache__" rmdir /s /q "schemas\__pycache__"
if exist "utils\__pycache__" rmdir /s /q "utils\__pycache__"
if exist "config\__pycache__" rmdir /s /q "config\__pycache__"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo   Done!
echo.

echo Step 2: Running hybrid reviewer test...
echo.
python -B test_hybrid_reviewer.py
echo.

echo ================================================
echo TEST COMPLETE
echo ================================================
echo.
pause
