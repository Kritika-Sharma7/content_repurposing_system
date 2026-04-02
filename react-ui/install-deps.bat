@echo off
cd /d "%~dp0"
echo Installing Tailwind CSS and dependencies...
call npm install -D tailwindcss postcss autoprefixer
echo.
echo Installing lucide-react...
call npm install lucide-react
echo.
echo Installation complete!
pause
