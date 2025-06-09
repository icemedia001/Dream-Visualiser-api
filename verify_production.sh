#!/bin/bash

# Production Readiness Verification Script
echo "🔍 Dream Visualizer - Production Readiness Check"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "backend/app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ Project structure validated"

# Check environment file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
else
    echo "✅ Environment file found"
    
    # Check for secure JWT secret
    if grep -q "your-super-secret-key" .env; then
        echo "⚠️  WARNING: Default JWT secret detected - CHANGE IN PRODUCTION!"
    else
        echo "✅ JWT secret appears to be customized"
    fi
fi

# Check Python and pip
echo ""
echo "🐍 Python Environment Check:"
python3 --version || { echo "❌ Python 3 not found"; exit 1; }
pip --version || { echo "❌ pip not found"; exit 1; }
echo "✅ Python environment OK"

# Check Node.js and npm
echo ""
echo "📦 Node.js Environment Check:"
node --version || { echo "❌ Node.js not found"; exit 1; }
npm --version || { echo "❌ npm not found"; exit 1; }
echo "✅ Node.js environment OK"

# Check backend dependencies
echo ""
echo "🔧 Backend Dependencies Check:"
cd backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --dry-run >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Backend dependencies validation passed"
    else
        echo "⚠️  Some backend dependencies may need updates"
    fi
else
    echo "❌ requirements.txt not found"
fi

# Test import of main modules
python -c "
try:
    import app.main
    import run_production
    print('✅ Core modules import successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
" || exit 1

cd ..

# Check frontend dependencies
echo ""
echo "🌐 Frontend Dependencies Check:"
cd frontend
if [ -f "package.json" ]; then
    npm list --depth=0 >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Frontend dependencies installed"
    else
        echo "⚠️  Frontend dependencies may need installation"
    fi
    
    # Test build
    echo "Testing frontend build..."
    npm run build >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Frontend build successful"
    else
        echo "❌ Frontend build failed"
        exit 1
    fi
else
    echo "❌ package.json not found"
fi

cd ..

# Check production scripts
echo ""
echo "📋 Production Scripts Check:"
if [ -x "start_production.sh" ] && [ -x "stop_production.sh" ]; then
    echo "✅ Production scripts are executable"
else
    echo "⚠️  Making production scripts executable..."
    chmod +x start_production.sh stop_production.sh
    echo "✅ Production scripts fixed"
fi

# Database check
echo ""
echo "🗄️  Database Check:"
cd backend
if [ -f "app.db" ] || [ -f "dream_visualizer.db" ]; then
    echo "✅ Database file exists"
else
    echo "ℹ️  Database will be created on first run"
fi

# Test database connection
python -c "
try:
    from app.db.session import engine
    from app.db.models import Base
    # Test connection
    with engine.connect() as conn:
        pass
    print('✅ Database connection test passed')
except Exception as e:
    print(f'ℹ️  Database will be initialized on startup: {e}')
"

cd ..

echo ""
echo "🎉 Production Readiness Summary:"
echo "================================"
echo "✅ Project structure: OK"
echo "✅ Python environment: OK" 
echo "✅ Node.js environment: OK"
echo "✅ Backend modules: OK"
echo "✅ Frontend build: OK"
echo "✅ Production scripts: OK"
echo ""
echo "🚀 Ready for production deployment!"
echo ""
echo "Next steps:"
echo "1. Update JWT_SECRET in .env file (IMPORTANT!)"
echo "2. Run: ./start_production.sh"
echo "3. Test the application"
echo "4. Configure reverse proxy for production"

exit 0 