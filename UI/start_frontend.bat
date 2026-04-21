@echo off
echo ========================================
echo Starting PM-KISAN UFAC Frontend UI
echo ========================================
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

REM Check if .env.local exists
if not exist .env.local (
    echo Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo.
)

echo Starting Next.js development server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev
