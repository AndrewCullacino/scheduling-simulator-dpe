#!/bin/bash

echo "=================================================="
echo "   Scheduling Simulator - Professional Edition    "
echo "=================================================="

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "🐳 Docker found! Starting with Docker Compose..."
    docker-compose up --build
else
    echo "⚠️  Docker not found."
    echo "   Falling back to local execution (requires Python 3.9+ and Node.js 18+)"
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3."
        exit 1
    fi

    # Check for Node
    if ! command -v npm &> /dev/null; then
        echo "❌ Node.js/npm not found. Please install Node.js."
        exit 1
    fi

    echo "🚀 Starting Backend..."
    # Setup venv if not exists
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r backend/requirements.txt
    else
        source .venv/bin/activate
    fi
    
    # Start backend in background
    uvicorn backend.app.main:app --port 8000 &
    BACKEND_PID=$!
    
    echo "🚀 Starting Frontend..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run dev &
    FRONTEND_PID=$!
    
    # Trap cleanup
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
    
    wait
fi
