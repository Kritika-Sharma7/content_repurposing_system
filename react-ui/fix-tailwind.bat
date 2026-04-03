@echo off
echo Uninstalling incorrect TailwindCSS package...
npm uninstall @tailwindcss/postcss

echo Installing correct TailwindCSS dependencies...
npm install -D tailwindcss@^3.4.0 postcss@^8.4.31 autoprefixer@^10.4.16

echo Done! Restart your dev server with: npm run dev
pause