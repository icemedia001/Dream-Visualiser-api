#!/bin/bash

# Production Stop Script for Dream Visualizer
# This script stops both the backend API and frontend servers

echo "🛑 Stopping Dream Visualizer servers..."

# Stop servers using saved PIDs
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✅ Backend stopped"
    else
        echo "ℹ️  Backend server was not running"
    fi
    rm -f .backend.pid
else
    echo "ℹ️  No backend PID file found"
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✅ Frontend stopped"
    else
        echo "ℹ️  Frontend server was not running"
    fi
    rm -f .frontend.pid
else
    echo "ℹ️  No frontend PID file found"
fi

# Fallback: kill any remaining processes
echo "🧹 Cleaning up any remaining processes..."
pkill -f "python.*run_production" 2>/dev/null || true
pkill -f "python.*http.server.*3000" 2>/dev/null || true

echo "🎉 All servers stopped!" 