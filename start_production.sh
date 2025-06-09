#!/bin/bash

# Production Startup Script for Dream Visualizer
# This script starts both the backend API and frontend in production mode

set -e  # Exit on any error

echo "🚀 Starting Dream Visualizer in Production Mode"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "backend/app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check environment file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Using default configuration."
fi

# Install dependencies
echo "📦 Installing dependencies..."

# Backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Frontend dependencies and build
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Start backend server
echo "🔧 Starting backend server..."
cd backend
python run_production.py &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"

# Serve frontend using a simple HTTP server
echo "🌐 Starting frontend server..."
cd frontend/dist
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ../..

echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Dream Visualizer is running!"
echo "   Backend API: http://localhost:8000"
echo "   Frontend:    http://localhost:3000"
echo "   API docs:    http://localhost:8000/docs"
echo ""
echo "To stop the servers, run: ./stop_production.sh"

# Save PIDs for cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for user input to stop
echo "Press Ctrl+C to stop all servers..."
trap 'echo "Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid; exit' INT

wait 