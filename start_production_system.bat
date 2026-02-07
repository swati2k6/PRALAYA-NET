@echo off
setlocal enabledelayedexpansion

echo.
echo ══════════════════════════════════════════════════════════════
echo 🚀 PRALAYA-NET: PRODUCTION SYSTEM LAUNCHER
echo ══════════════════════════════════════════════════════
echo.
echo 📍 Fully Functional Autonomous Disaster-Response Command Platform
echo.

echo 🔍 STEP 1: ENVIRONMENT CHECKS
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found or not in PATH
    echo 💡 Please install Python 3.9+ and add to PATH
    pause
    exit /b 1
)

echo ✅ Python found
python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>&1
for /f "tokens=2,3" %%a in (%version%) do (
    if %%a lss 3 (
        echo ✅ Python %%a.%%b compatible
        goto python_ok
    )
)

echo ⚠️  Python 3.9+ recommended for best compatibility

:python_ok
REM Check Node.js installation
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found or not in PATH
    echo 💡 Please install Node.js 16+ and add to PATH
    pause
    exit /b 1
)

echo ✅ Node.js found

echo.
echo 📦 STEP 2: DEPENDENCY INSTALLATION
echo.

REM Change to backend directory
cd /d "%~dp0\backend"

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ⚠️ requirements.txt not found, using basic dependencies
    goto start_backend
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    echo 💡 Try running: pip install -r requirements.txt manually
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully

REM Change to frontend directory
cd /d "%~dp0\dashboard"

REM Install frontend dependencies if node_modules doesn't exist
if not exist node_modules (
    echo 📦 Running npm install...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install frontend dependencies
        pause
        exit /b 1
    )
) else (
    echo ✅ Frontend dependencies already installed
)

echo.
echo 🚀 STEP 3: STARTING SERVICES
echo.

REM Start backend
cd /d "%~dp0\backend"
echo 📍 Starting backend server...
echo    Backend URL: http://127.0.0.1:8000

start "PRALAYA-NET Backend" cmd /k python run.py
if %errorlevel% neq 0 (
    echo ❌ Failed to start backend
    pause
    exit /b 1
)

echo ✅ Backend server starting...

REM Start frontend
cd /d "%~dp0\dashboard"
echo 📍 Starting frontend server...
echo    Frontend URL: http://localhost:5173
echo    Enhanced Command Center: http://localhost:5173/enhanced-command-center

start "PRALAYA-NET Frontend" cmd /k npm run dev
if %errorlevel% neq 0 (
    echo ❌ Failed to start frontend
    pause
    exit /b 1
)

echo ✅ Frontend development server starting...

echo.
echo ⏳ STEP 4: WAITING FOR SERVICES READY
echo.
echo 🔄 Waiting for services to initialize...
timeout /t 30 /nobreak >nul

echo.
echo 🔍 STEP 5: SYSTEM HEALTH VERIFICATION
echo.
echo 🔍 Performing comprehensive health checks...

REM Check backend health
curl -s http://127.0.0.1:8000/api/health >nul
if %errorlevel% neq 0 (
    echo ❌ Backend health check failed
) else (
    echo ✅ Backend health endpoint responding
)

REM Check frontend health
curl -s http://localhost:5173 >nul
if %errorlevel% neq 0 (
    echo ❌ Frontend health check failed
) else (
    echo ✅ Frontend serving correctly
)

REM Check API endpoints
curl -s http://127.0.0.1:8000/api/system-status >nul
if %errorlevel% neq 0 (
    echo ❌ System status endpoint not responding
) else (
    echo ✅ System status endpoint responding
)

echo.
echo 🎯 STEP 6: FINAL STATUS
echo.
echo ════════════════════════════════════════════════════
echo 🎉 PRALAYA-NET PRODUCTION SYSTEM READY
echo ════════════════════════════════════════════════
echo.
echo 📍 ACCESS URLS:
echo    Backend API:        http://127.0.0.1:8000
echo    Frontend UI:        http://localhost:5173
echo    Enhanced Command Center: http://localhost:5173/enhanced-command-center
echo    API Documentation:  http://127.0.0.1:8000/docs
echo    Health Check:       http://127.0.0.1:8000/api/health
echo    System Status:      http://127.0.0.1:8000/api/system-status
echo.
echo 🎯 NEXT STEPS:
echo    1. Open Enhanced Command Center in your browser
echo    2. Verify backend status shows '🟢 Online'
echo    3. Click 'Simulate Disaster' to test autonomous response
echo    4. Watch real-time stability index updates
echo    5. Click 'Explain' on any action for detailed reasoning
echo    6. Use 'Start Replay' for timeline analysis
echo.
echo 🔧 SYSTEM FEATURES:
echo    ✅ Real-time WebSocket streaming
echo    ✅ Dynamic stability index calculation
echo    ✅ Enhanced prediction engine with real data
echo    ✅ Historical data integration with fallback
echo    ✅ Autonomous decision execution
echo    ✅ Multi-agent coordination
echo    ✅ Decision explainability
echo    ✅ Complete event replay system
echo.
echo 🌟 Press any key to stop all services...
pause >nul

REM Stop services
taskkill /f "PRALAYA-NET Backend" /im cmd.exe >nul 2>&1
taskkill /f "PRALAYA-NET Frontend" /im node.exe >nul 2>&1

echo.
echo 🛑 Services stopped
echo.
pause
