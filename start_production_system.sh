#!/bin/bash

echo ""
echo "═════════════════════════════════════════════════════"
echo "🚀 PRALAYA-NET: PRODUCTION SYSTEM LAUNCHER"
echo "═══════════════════════════════════════════════"
echo ""

echo "📍 Fully Functional Autonomous Disaster-Response Command Platform"
echo ""

# Function to check command exists
command_exists() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
}

# Function to print status with icon
print_status() {
    local status="$1"
    local message="$2"
    local icon="ℹ️"
    
    case "$status" in
        "info") icon="ℹ️" ;;
        "success") icon="✅" ;;
        "warning") icon="⚠️" ;;
        "error") icon="❌" ;;
        "critical") icon="🚨" ;;
    esac
    
    echo "$icon $message"
}

# Function to check Python version
check_python_version() {
    local version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>/dev/null)
    local major=$(echo "$version" | cut -d. -f1)
    
    if [ "$major" -lt 3 ]; then
        print_status "Python version check" "warning"
        echo "   Python $major detected"
        echo "   ⚠️  Python 3.9+ recommended for best compatibility"
        return 1
    else
        print_status "Python version check" "success"
        echo "   ✅ Python $version compatible"
        return 0
}

# Function to check Node.js version
check_node_version() {
    if command_exists node; then
        local version=$(node --version 2>/dev/null)
        print_status "Node.js version check" "success"
        echo "   ✅ $version"
        return 0
    else
        print_status "Node.js check" "warning"
        echo "   ⚠️  Node.js not installed"
        return 1
}

# Function to install Python dependencies
install_python_dependencies() {
    print_status "Installing Python dependencies" "info"
    
    if [ ! -f "requirements.txt" ]; then
        print_status "Requirements file check" "warning"
        echo "   ⚠️  requirements.txt not found, using basic dependencies"
        return 1
    fi
    
    # Upgrade pip first
    python3 -m pip install --upgrade pip
    
    # Install requirements
    python3 -m pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_status "Python dependencies installation" "success"
        echo "   ✅ All Python dependencies installed successfully"
        return 0
    else
        print_status "Python dependencies installation" "error"
        echo "   ❌ Failed to install some dependencies"
        echo "   💡 Try running: pip install -r requirements.txt manually"
        return 1
}

# Function to install frontend dependencies
install_frontend_dependencies() {
    print_status "Installing frontend dependencies" "info"
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies" "info"
        echo "   📦 Running npm install..."
        
        npm install
        
        if [ $? -eq 0 ]; then
            print_status "Frontend dependencies installation" "success"
            echo "   ✅ Frontend dependencies installed successfully"
            return 0
        else
            print_status "Frontend dependencies installation" "error"
            echo "   ❌ Failed to install frontend dependencies"
            return 1
    else
        print_status "Frontend dependencies check" "success"
        echo "   ✅ Frontend dependencies already installed"
        return 0
}

# Function to start backend
start_backend() {
    print_status "Starting backend server" "info"
    echo "   📍 Backend URL: http://127.0.0.1:8000"
    
    # Start backend in background
    python3 run.py &
    BACKEND_PID=$!
    
    if [ $? -eq 0 ]; then
        print_status "Backend server started" "success"
        echo "   ✅ Backend server starting..."
        return 0
    else
        print_status "Backend startup" "error"
        echo "   ❌ Failed to start backend"
        return 1
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server" "info"
    echo "   📍 Frontend URL: http://localhost:5173"
    echo "   📍 Enhanced Command Center: http://localhost:5173/enhanced-command-center"
    
    # Start frontend in background
    npm run dev &
    FRONTEND_PID=$!
    
    if [ $? -eq 0 ]; then
        print_status "Frontend server started" "success"
        echo "   ✅ Frontend development server starting..."
        return 0
    else
        print_status "Frontend startup" "error"
        echo "   ❌ Failed to start frontend"
        return 1
}

# Function to wait for backend readiness
wait_for_backend_ready() {
    print_status "Waiting for backend readiness" "info"
    echo "   ⏳ Checking backend health..."
    
    local timeout=30
    local count=0
    
    while [ $count -lt $timeout ]; do
        if curl -s http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
            print_status "Backend ready" "success"
            echo "   ✅ Backend is ready and responding"
            return 0
        else
            echo "   ⏳ Backend not ready yet"
        fi
        
        sleep 2
        count=$((count + 1))
    done
    
    print_status "Backend readiness timeout" "warning"
    echo "   ⚠️ Backend readiness timeout - proceeding anyway"
    return 1
}

# Function to wait for frontend readiness
wait_for_frontend_ready() {
    print_status "Waiting for frontend readiness" "info"
    echo "   ⏳ Checking frontend availability..."
    
    local timeout=20
    local count=0
    
    while [ $count -lt $timeout ]; do
        if curl -s http://localhost:5173 >/dev/null 2>&1; then
            print_status "Frontend ready" "success"
            echo "   ✅ Frontend is ready and serving"
            return 0
        else
            echo "   ⏳ Frontend not ready yet"
        fi
        
        sleep 1
        count=$((count + 1))
    done
    
    print_status "Frontend readiness timeout" "warning"
    echo "   ⚠️ Frontend readiness timeout - proceeding anyway"
    return 1
}

# Function to verify system health
verify_system_health() {
    print_status "Verifying system health" "info"
    echo "   🔍 Performing comprehensive health checks..."
    
    local backend_health=false
    local frontend_health=false
    local api_endpoints=false
    local websocket_connection=false
    local data_integration=false
    
    # Check backend health
    if curl -s http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
        backend_health=true
        print_status "Backend health check" "success"
        echo "   ✅ Backend health endpoint responding"
    fi
    
    # Check frontend health
    if curl -s http://localhost:5173 >/dev/null 2>&1; then
        frontend_health=true
        print_status "Frontend health check" "success"
        echo "   ✅ Frontend serving correctly"
    fi
    
    # Check API endpoints
    if curl -s http://127.0.0.1:8000/api/system-status >/dev/null 2>&1; then
        api_endpoints=true
        print_status "API endpoints check" "success"
        echo "   ✅ System status endpoint responding"
    fi
    
    # Check data integration
    if curl -s http://127.0.0.1:8000/api/system-status >/dev/null 2>&1; then
        if grep -q "cached" <<< "$(curl -s http://127.0.0.1:8000/api/system-status 2>/dev/null)"; then
            data_integration=true
            print_status "Data integration check" "success"
            echo "   ✅ Data integration active with cached fallback"
        else
            print_status "Data integration check" "warning"
            echo "   ⚠️ Data integration limited to real-time APIs"
        fi
    fi
    
    # Overall health assessment
    if [ "$backend_health" = true ] && [ "$frontend_health" = true ] && [ "$api_endpoints" = true ]; then
        print_status "System health verification" "success"
        echo "   🎉 ALL SYSTEMS HEALTHY AND READY"
        return 0
    else
        print_status "System health verification" "warning"
        echo "   ⚠️ Some systems not ready"
        return 1
}

# Function to print access URLs
print_access_urls() {
    echo ""
    echo "📍 ACCESS URLS:"
    echo "   Backend API:        http://127.0.0.1:8000"
    echo "   Frontend UI:        http://localhost:5173"
    echo "   Enhanced Command Center: http://localhost:5173/enhanced-command-center"
    echo "   API Documentation:  http://127.0.0.1:8000/docs"
    echo "   Health Check:       http://127.0.0.1:8000/api/health"
    echo "   System Status:      http://127.0.0.1:8000/api/system-status"
    echo ""
}

# Function to print final status
print_final_status() {
    echo ""
    echo "═════════════════════════════════════════════════"
    echo "🎉 PRALAYA-NET PRODUCTION SYSTEM READY"
    echo "═══════════════════════════════════════════"
    echo ""
    
    print_access_urls
    
    echo ""
    echo "🎯 NEXT STEPS:"
    echo "   1. Open Enhanced Command Center in your browser"
    echo "   2. Verify backend status shows '🟢 Online'"
    echo "   3. Click 'Simulate Disaster' to test autonomous response"
    echo "   4. Watch real-time stability index updates"
    echo "   5. Click 'Explain' on any action for detailed reasoning"
    echo "   6. Use 'Start Replay' for timeline analysis"
    echo ""
    
    echo "🔧 SYSTEM FEATURES:"
    echo "   ✅ Real-time WebSocket streaming"
    echo "   ✅ Dynamic stability index calculation"
    echo "   ✅ Enhanced prediction engine with real data"
    echo "   ✅ Historical data integration with fallback"
    echo "   ✅ Autonomous decision execution"
    echo "   ✅ Multi-agent coordination"
    echo "   ✅ Decision explainability"
    echo "   ✅ Complete event replay system"
    echo ""
}

# Function to stop services
stop_services() {
    print_status "Stopping services" "info"
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_status "Backend stopped" "success"
        echo "   ✅ Backend server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend stopped" "success"
        echo "   ✅ Frontend server stopped"
    fi
    
    echo ""
    echo "🛑 Services stopped"
    echo ""
}

# Main production system launcher
launch_production_system() {
    echo ""
    echo "🔍 STEP 1: ENVIRONMENT CHECKS"
    echo ""
    
    # Check Python and Node.js versions
    python_ok=$(check_python_version)
    node_ok=$(check_node_version)
    
    if [ $python_ok -ne 0 ] || [ $node_ok -ne 0 ]; then
        print_status "Environment check failed" "critical"
        echo "   ❌ Required dependencies not available"
        exit 1
    fi
    
    echo ""
    echo "📦 STEP 2: DEPENDENCY INSTALLATION"
    echo ""
    
    # Install dependencies
    python_deps_ok=$(install_python_dependencies)
    frontend_deps_ok=$(install_frontend_dependencies)
    
    if [ $python_deps_ok -ne 0 ] || [ $frontend_deps_ok -ne 0 ]; then
        print_status "Dependency installation failed" "critical"
        echo "   ❌ Failed to install required dependencies"
        exit 1
    fi
    
    echo ""
    echo "🚀 STEP 3: STARTING SERVICES"
    echo ""
    
    # Start services
    backend_started=$(start_backend)
    frontend_started=$(start_frontend)
    
    if [ $backend_started -ne 0 ] || [ $frontend_started -ne 0 ]; then
        print_status "Service startup failed" "critical"
        echo "   ❌ Failed to start required services"
        exit 1
    fi
    
    echo ""
    echo "⏳ STEP 4: WAITING FOR SERVICES READY"
    echo ""
    
    # Wait for services to be ready
    wait_for_backend_ready &
    BACKEND_WAIT_PID=$!
    
    wait_for_frontend_ready &
    FRONTEND_WAIT_PID=$!
    
    wait $BACKEND_WAIT_PID $FRONTEND_WAIT_PID
    
    echo ""
    echo "🔍 STEP 5: SYSTEM HEALTH VERIFICATION"
    echo ""
    
    # Verify system health
    system_healthy=$(verify_system_health)
    
    echo ""
    echo "🎯 STEP 6: FINAL STATUS"
    echo ""
    
    if [ $system_healthy -eq 0 ]; then
        print_final_status
        exit 0
    else
        print_status "System verification failed" "warning"
        echo "   ⚠️ System started but some components may not be fully functional"
        echo "   💡 Check individual service logs for troubleshooting"
        exit 1
}

# Handle Ctrl+C gracefully
trap 'echo ""; echo "🛑 USER INTERRUPT"; stop_services; exit 0' INT

# Main execution
if [ "$1" = "--interactive" ]; then
    echo "🔄 Running in interactive mode..."
    while true; do
        launch_production_system
        echo ""
        echo "🔄 Press Ctrl+C to restart..."
        sleep 5
    done
else
    launch_production_system
fi
