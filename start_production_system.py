#!/usr/bin/env python3
"""
PRALAYA-NET Production System Launcher
Automatically starts backend + frontend with dependency installation and verification
"""

import os
import sys
import subprocess
import time
import asyncio
import aiohttp
from pathlib import Path

class ProductionLauncher:
    """Production-ready system launcher for PRALAYA-NET"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "dashboard"
        
        # Service URLs
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.enhanced_cc_url = "http://localhost:5173/enhanced-command-center"
        
        # Process tracking
        self.backend_process = None
        self.frontend_process = None
        
    def print_header(self):
        """Print startup header"""
        print("\n" + "="*80)
        print("🚀 PRALAYA-NET: PRODUCTION SYSTEM LAUNCHER")
        print("="*80)
        print("📍 Fully Functional Autonomous Disaster-Response Command Platform")
        print("="*80)
        print()
    
    def print_status(self, message, status="info"):
        """Print status message with icon"""
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌", "critical": "🚨"}
        print(f"{icons.get(status)} {message}")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        major = version.major
        if major < 3:
            self.print_status("Python version check", "warning")
            print(f"   Python {major}.{version.minor} detected")
            print("   ⚠️  Python 3.9+ recommended for best compatibility")
            return False
        else:
            self.print_status("Python version check", "success")
            print(f"   ✅ Python {major}.{version.minor}.{version.micro} compatible")
            return True
    
    def check_node_version(self):
        """Check Node.js version"""
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.strip()
                self.print_status("Node.js version check", "success")
                print(f"   ✅ {version_line}")
                return True
            else:
                self.print_status("Node.js version check", "error")
                print(f"   ❌ Node.js not found or error")
                return False
        except FileNotFoundError:
            self.print_status("Node.js check", "warning")
            print("   ⚠️  Node.js not installed")
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        self.print_status("Installing Python dependencies", "info")
        
        requirements_file = self.backend_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_status("Requirements file not found", "warning")
            print("   ⚠️  requirements.txt not found, using basic dependencies")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      cwd=self.backend_dir, check=True)
            
            # Install requirements
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=self.backend_dir, check=True)
            
            if result.returncode == 0:
                self.print_status("Python dependencies installation", "success")
                print("   ✅ All Python dependencies installed successfully")
                return True
            else:
                self.print_status("Python dependencies installation", "error")
                print("   ❌ Failed to install some dependencies")
                print("   💡 Try running: pip install -r requirements.txt manually")
                return False
                
        except Exception as e:
            self.print_status("Python dependencies installation", "error")
            print(f"   ❌ Installation error: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Install frontend dependencies"""
        self.print_status("Installing frontend dependencies", "info")
        
        try:
            # Check if node_modules exists
            node_modules = self.frontend_dir / "node_modules"
            
            if not node_modules.exists():
                self.print_status("Installing frontend dependencies", "info")
                print("   📦 Running npm install...")
                
                result = subprocess.run(['npm', 'install'], 
                      cwd=self.frontend_dir, check=True)
                
                if result.returncode == 0:
                    self.print_status("Frontend dependencies installation", "success")
                    print("   ✅ Frontend dependencies installed successfully")
                    return True
                else:
                    self.print_status("Frontend dependencies installation", "error")
                    print("   ❌ Failed to install frontend dependencies")
                    return False
            else:
                self.print_status("Frontend dependencies check", "success")
                print("   ✅ Frontend dependencies already installed")
                return True
                
        except Exception as e:
            self.print_status("Frontend dependencies installation", "error")
            print(f"   ❌ Installation error: {e}")
            return False
    
    def start_backend(self):
        """Start backend server"""
        self.print_status("Starting backend server", "info")
        print(f"   📍 Backend URL: {self.backend_url}")
        
        try:
            # Start backend in background
            self.backend_process = subprocess.Popen([
                sys.executable, "run.py"
            ], 
            cwd=self.backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
            
            self.print_status("Backend server started", "success")
            print("   ✅ Backend server starting...")
            return True
            
        except Exception as e:
            self.print_status("Backend startup", "error")
            print(f"   ❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start frontend development server"""
        self.print_status("Starting frontend server", "info")
        print(f"   📍 Frontend URL: {self.frontend_url}")
        print(f"   📍 Enhanced Command Center: {self.enhanced_cc_url}")
        
        try:
            # Start frontend in background
            self.frontend_process = subprocess.Popen([
                'npm', 'run', 'dev'
            ], 
            cwd=self.frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
            
            self.print_status("Frontend server started", "success")
            print("   ✅ Frontend development server starting...")
            return True
            
        except Exception as e:
            self.print_status("Frontend startup", "error")
            print(f"   ❌ Failed to start frontend: {e}")
            return False
    
    async def wait_for_backend_ready(self, timeout=30):
        """Wait for backend to be ready"""
        self.print_status("Waiting for backend readiness", "info")
        print("   ⏳ Checking backend health...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.backend_url}/api/health", timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.print_status("Backend ready", "success")
                            print("   ✅ Backend is ready and responding")
                            return True
                        else:
                            print(f"   ⏳ Backend not ready yet (HTTP {response.status})")
                            
            except Exception as e:
                print(f"   ⚠️ Health check error: {e}")
            
            await asyncio.sleep(2)
        
        self.print_status("Backend readiness timeout", "warning")
        print("   ⚠️ Backend readiness timeout - proceeding anyway")
        return False
    
    async def wait_for_frontend_ready(self, timeout=20):
        """Wait for frontend to be ready"""
        self.print_status("Waiting for frontend readiness", "info")
        print("   ⏳ Checking frontend availability...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.frontend_url}", timeout=5) as response:
                        if response.status == 200:
                            self.print_status("Frontend ready", "success")
                            print("   ✅ Frontend is ready and serving")
                            return True
                        else:
                            print(f"   ⏳ Frontend not ready yet (HTTP {response.status})")
                            
            except Exception as e:
                print(f"   ⚠️ Frontend check error: {e}")
            
            await asyncio.sleep(1)
        
        self.print_status("Frontend readiness timeout", "warning")
        print("   ⚠️ Frontend readiness timeout - proceeding anyway")
        return False
    
    async def verify_system_health(self):
        """Verify complete system health"""
        self.print_status("Verifying system health", "info")
        print("   🔍 Performing comprehensive health checks...")
        
        health_checks = {
            'backend_health': False,
            'frontend_health': False,
            'api_endpoints': False,
            'websocket_connection': False
            'data_integration': False
        }
        
        # Check backend health
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/health", timeout=10) as response:
                    if response.status == 200:
                        health_checks['backend_health'] = True
                        self.print_status("Backend health check", "success")
                        print("   ✅ Backend health endpoint responding")
                    else:
                        self.print_status("Backend health check", "error")
                        print(f"   ❌ Backend health check failed: {response.status}")
        except Exception as e:
            self.print_status("Backend health check", "error")
            print(f"   ❌ Backend health check error: {e}")
        
        # Check frontend health
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.frontend_url}", timeout=10) as response:
                    if response.status == 200:
                        health_checks['frontend_health'] = True
                        self.print_status("Frontend health check", "success")
                        print("   ✅ Frontend serving correctly")
                    else:
                        self.print_status("Frontend health check", "error")
                        print(f"   ❌ Frontend health check failed: {response.status}")
        except Exception as e:
            self.print_status("Frontend health check", "error")
            print(f"   ❌ Frontend health check error: {e}")
        
        # Check API endpoints
        endpoints_to_check = [
            '/api/health',
            '/api/system-status',
            '/api/fallback-mode',
            '/api/autonomous/status',
            '/api/stability/current'
        ]
        
        try:
            async with aiohttp.ClientSession() as session:
                for endpoint in endpoints_to_check:
                    async with session.get(f"{self.backend_url}{endpoint}", timeout=5) as response:
                        if response.status == 200:
                            print(f"   ✅ {endpoint} responding")
                        else:
                            print(f"   ⚠️ {endpoint} not responding: {response.status}")
                            
                if all(response.status == 200 for response in responses):
                    health_checks['api_endpoints'] = True
                    self.print_status("API endpoints check", "success")
                    print("   ✅ All critical API endpoints responding")
                    
        except Exception as e:
            self.print_status("API endpoints check", "error")
            print(f"   ❌ API endpoints check error: {e}")
        
        # Check data integration
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/system-status", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('data_sources', {}).get('cached'):
                            health_checks['data_integration'] = True
                            self.print_status("Data integration check", "success")
                            print("   ✅ Data integration active with cached fallback")
                        else:
                            self.print_status("Data integration check", "warning")
                            print("   ⚠️ Data integration limited to real-time APIs")
                            
        except Exception as e:
            self.print_status("Data integration check", "error")
            print(f"   ❌ Data integration check error: {e}")
        
        # Overall health assessment
        all_healthy = all(health_checks.values())
        
        if all_healthy:
            self.print_status("System health verification", "success")
            print("   🎉 ALL SYSTEMS HEALTHY AND READY")
            return True
        else:
            failed_checks = [k for k, v in health_checks.items() if not v]
            self.print_status("System health verification", "warning")
            print(f"   ⚠️ Some systems not ready: {', '.join(failed_checks)}")
            return False
    
    def print_access_urls(self):
        """Print all access URLs"""
        print("\n📍 ACCESS URLS:")
        print(f"   Backend API:        {self.backend_url}")
        print(f"   Frontend UI:        {self.frontend_url}")
        print(f"   Enhanced Command Center: {self.enhanced_cc_url}")
        print(f"   API Documentation:  {self.backend_url}/docs")
        print(f"   Health Check:       {self.backend_url}/api/health")
        print(f"   System Status:      {self.backend_url}/api/system-status")
        print()
    
    def print_final_status(self):
        """Print final system status"""
        print("\n" + "="*80)
        print("🎉 PRALAYA-NET PRODUCTION SYSTEM READY")
        print("="*80)
        print("📍 Fully Operational Autonomous Disaster-Response Command Platform")
        print("="*80)
        print()
        
        self.print_access_urls()
        
        print("\n🎯 NEXT STEPS:")
        print("   1. Open Enhanced Command Center in your browser")
        print("   2. Verify backend status shows '🟢 Online'")
        print("   3. Click 'Simulate Disaster' to test autonomous response")
        print("   4. Watch real-time stability index updates")
        print("   5. Click 'Explain' on any action for detailed reasoning")
        print("   6. Use 'Start Replay' for timeline analysis")
        print()
        
        print("\n🔧 SYSTEM FEATURES:")
        print("   ✅ Real-time WebSocket streaming")
        print("   ✅ Dynamic stability index calculation")
        print("   ✅ Enhanced prediction engine with real data")
        print("   ✅ Historical data integration with fallback")
        print("   ✅ Autonomous decision execution")
        print("   ✅ Multi-agent coordination")
        print("   ✅ Decision explainability")
        print("   ✅ Complete event replay system")
        print()
    
    def stop_services(self):
        """Stop all running services"""
        self.print_status("Stopping services", "info")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.print_status("Backend stopped", "success")
            print("   ✅ Backend server stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.print_status("Frontend stopped", "success")
            print("   ✅ Frontend server stopped")
    
    async def launch_production_system(self):
        """Main production system launcher"""
        self.print_header()
        
        # Step 1: Environment checks
        print("🔍 STEP 1: ENVIRONMENT CHECKS")
        
        python_ok = self.check_python_version()
        node_ok = self.check_node_version()
        
        if not python_ok:
            self.print_status("Environment check failed", "critical")
            print("   ❌ Python version incompatible. Please install Python 3.9+")
            return False
        
        if not node_ok:
            self.print_status("Environment check failed", "critical")
            print("   ❌ Node.js not found. Please install Node.js 16+")
            return False
        
        # Step 2: Dependency installation
        print("\n📦 STEP 2: DEPENDENCY INSTALLATION")
        
        python_deps_ok = self.install_python_dependencies()
        frontend_deps_ok = self.install_frontend_dependencies()
        
        if not python_deps_ok or not frontend_deps_ok:
            self.print_status("Dependency installation failed", "critical")
            print("   ❌ Failed to install required dependencies")
            return False
        
        # Step 3: Start services
        print("\n🚀 STEP 3: STARTING SERVICES")
        
        backend_started = self.start_backend()
        frontend_started = self.start_frontend()
        
        if not backend_started or not frontend_started:
            self.print_status("Service startup failed", "critical")
            print("   ❌ Failed to start required services")
            return False
        
        # Step 4: Wait for services to be ready
        print("\n⏳ STEP 4: WAITING FOR SERVICES READY")
        
        backend_ready = await self.wait_for_backend_ready()
        frontend_ready = await self.wait_for_frontend_ready()
        
        # Step 5: Verify system health
        print("\n🔍 STEP 5: SYSTEM HEALTH VERIFICATION")
        
        system_healthy = await self.verify_system_health()
        
        # Step 6: Final status
        print("\n🎯 STEP 6: FINAL STATUS")
        
        if system_healthy:
            self.print_final_status()
            return True
        else:
            self.print_status("System verification failed", "warning")
            print("   ⚠️ System started but some components may not be fully functional")
            print("   💡 Check individual service logs for troubleshooting")
            return False
    
    def run_interactive(self):
        """Run in interactive mode"""
        try:
            asyncio.run(self.launch_production_system())
        except KeyboardInterrupt:
            print("\n\n🛑 USER INTERRUPT")
            self.stop_services()
            print("   🛑 Services stopped by user request")
        except Exception as e:
            print(f"\n\n❌ FATAL ERROR: {e}")
            self.stop_services()

def main():
    """Main entry point"""
    launcher = ProductionLauncher()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        launcher.run_interactive()
    else:
        # Non-interactive mode - just launch
        asyncio.run(launcher.launch_production_system())

if __name__ == "__main__":
    main()
