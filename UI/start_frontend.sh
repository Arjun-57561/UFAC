#!/bin/bash

echo "========================================"
echo "Starting PM-KISAN UFAC Frontend UI"
echo "========================================"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo ""
fi

echo "Starting Next.js development server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
