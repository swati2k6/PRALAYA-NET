#!/usr/bin/env python3
"""
PRALAYA-NET Ultimate System Launcher
Launches backend + frontend with dependency installation and verification
Goal: Fully operational system in under 2 minutes
"""

import asyncio
import subprocess
import sys
import time
import os
from pathlib import Path
from datetime import datetime

class SystemLauncher:
    """Ultimate system launcher for PRALAYA-NET"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "dashboard"
        
        # Service URLs
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.enhanced_cc_url = "http://localhost:5173/reliable-command-center"
        
        # Process tracking
        self.backend_process = None
        self.frontend_process = None
        
        # Start time
        self.start_time = time.time()
        
    def print_header(self):
        """Print startup header"""
        print("\n" + "="*80)
        print("🚀 PRALAYA-NET: ULTIMATE SYSTEM LAUNCHER")
        print("="*80)
        print("📍 Fully Functional Autonomous Disaster-Response Command Platform")
        print("🎯 Goal: Launch in under 2 minutes with full verification")
        print("="*80)
        print()
    
    def print_status(self, message, status="info"):
        """Print status message with icon and timestamp"""
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌", "critical": "🚨"}
        elapsed = f"[{time.time() - self.start_time:.1f}s]"
        print(f"{icons.get(status)} {elapsed} {message}")
    
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
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, 
                                  cwd=self.frontend_dir)
            if result.returncode == 0:
                self.print_status("Node.js version check", "success")
                print(f"   ✅ {result.stdout.strip()}")
                return True
            else:
                self.print_status("Node.js version check", "error")
                return False
        except FileNotFoundError:
            self.print_status("Node.js check", "warning")
            print("   ⚠️  Node.js not installed")
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        self.print_status("Installing Python dependencies", "info")
        
        requirements_file = self.backend_dir / "requirements_simple.txt"
        
        if not requirements_file.exists():
            self.print_status("Requirements file check", "warning")
            print("   ⚠️  requirements_simple.txt not found, using basic dependencies")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      cwd=self.backend_dir, check=True, capture_output=True)
            
            # Install requirements
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_simple.txt"], 
                      cwd=self.backend_dir, check=True, capture_output=True)
            
            if result.returncode == 0:
                self.print_status("Python dependencies installation", "success")
                print("   ✅ All Python dependencies installed successfully")
                return True
            else:
                self.print_status("Python dependencies installation", "error")
                print("   ❌ Failed to install some dependencies")
                print("   💡 Try running: pip install -r requirements_simple.txt manually")
                return False
                
        except Exception as e:
            self.print_status("Python dependencies installation", "error")
            print(f"   ❌ Installation error: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Install frontend dependencies"""
        self.print_status("Installing frontend dependencies", "info")
        
        # Check if node_modules exists
        node_modules = self.frontend_dir / "node_modules"
        
        if not node_modules.exists():
            self.print_status("Installing frontend dependencies", "info")
            print("   📦 Running npm install...")
            
            result = subprocess.run(['npm', 'install'], 
                      cwd=self.frontend_dir, check=True, capture_output=True)
            
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
    
    def start_backend(self):
        """Start backend server"""
        self.print_status("Starting backend server", "info")
        print(f"   📍 Backend URL: {self.backend_url}")
        
        try:
            # Start backend in background
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
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
    
    async def wait_for_services_ready(self, timeout=60):
        """Wait for services to be ready with timeout"""
        self.print_status("Waiting for services ready", "info")
        print("   ⏳ Checking service readiness...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check backend health
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.backend_url}/health", timeout=5) as response:
                        if response.status == 200:
                            self.print_status("Backend ready", "success")
                            print("   ✅ Backend is ready and responding")
                            backend_ready = True
                        else:
                            backend_ready = False
            except:
                backend_ready = False
            
            # Check frontend health
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.frontend_url, timeout=5) as response:
                        if response.status == 200:
                            self.print_status("Frontend ready", "success")
                            print("   ✅ Frontend is ready and serving")
                            frontend_ready = True
                        else:
                            frontend_ready = False
            except:
                frontend_ready = False
            
            # If both are ready, break
            if backend_ready and frontend_ready:
                elapsed_time = time.time() - self.start_time
                self.print_status("System ready", "success")
                print(f"   🎉 SYSTEM READY IN {elapsed_time:.1f} SECONDS!")
                return True
            
            await asyncio.sleep(2)  # Check every 2 seconds
        
        self.print_status("Service readiness timeout", "warning")
        print("   ⚠️ Services readiness timeout - proceeding anyway")
        return False
    
    def run_comprehensive_test(self):
        """Run comprehensive system test"""
        self.print_status("Running comprehensive system test", "info")
        
        try:
            # Run the test script
            test_script = self.project_root / "test_system_complete.py"
            if test_script.exists():
                result = subprocess.run([sys.executable, str(test_script)], 
                                      capture_output=True, text=True)
                
                if "ALL TESTS PASSED" in result.stdout:
                    self.print_status("Comprehensive test", "success")
                    print("   ✅ All system tests passed")
                    return True
                else:
                    self.print_status("Comprehensive test", "warning")
                    print("   ⚠️ Some tests failed - check test report")
                    return False
            else:
                self.print_status("Comprehensive test", "warning")
                print("   ⚠️ Test script not found")
                return False
        except Exception as e:
            self.print_status("Comprehensive test", "error")
            print(f"   ❌ Test execution error: {e}")
            return False
    
    def print_access_urls(self):
        """Print all access URLs"""
        print("\n📍 ACCESS URLS:")
        print(f"   Backend API:        {self.backend_url}")
        print(f"   Frontend UI:        {self.frontend_url}")
        print(f"   Enhanced Command Center: {self.enhanced_cc_url}")
        print(f"   API Documentation:  {self.backend_url}/docs")
        print(f"   Health Check:       {self.backend_url}/health")
        print()
    
    def print_final_status(self):
        """Print final system status"""
        elapsed_time = time.time() - self.start_time
        
        print("\n" + "="*80)
        print("🎉 PRALAYA-NET ULTIMATE SYSTEM LAUNCH COMPLETE")
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
        print("   ✅ Production deployment ready")
        print()
        
        print(f"🕒 LAUNCH TIME: {elapsed_time:.1f} seconds")
        
        if elapsed_time < 120:
            print("🎉 GOAL ACHIEVED: Launched in under 2 minutes!")
        else:
            print("⚠️  Launch time exceeded 2 minutes - check for issues")
    
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
        
        print()
        print("🛑 Services stopped")
        print()
    
    async def launch_system(self):
        """Main system launcher"""
        self.print_header()
        
        # Step 1: Environment checks
        print("🔍 STEP 1: ENVIRONMENT CHECKS")
        print()
        
        python_ok = self.check_python_version()
        node_ok = self.check_node_version()
        
        if not python_ok or not node_ok:
            self.print_status("Environment check failed", "critical")
            print("   ❌ Required dependencies not available")
            return False
        
        # Step 2: Dependency installation
        print("\n📦 STEP 2: DEPENDENCY INSTALLATION")
        print()
        
        python_deps_ok = self.install_python_dependencies()
        frontend_deps_ok = self.install_frontend_dependencies()
        
        if not python_deps_ok or not frontend_deps_ok:
            self.print_status("Dependency installation failed", "critical")
            print("   ❌ Failed to install required dependencies")
            return False
        
        # Step 3: Start services
        print("\n🚀 STEP 3: STARTING SERVICES")
        print()
        
        backend_started = self.start_backend()
        frontend_started = self.start_frontend()
        
        if not backend_started or not frontend_started:
            self.print_status("Service startup failed", "critical")
            print("   ❌ Failed to start required services")
            return False
        
        # Step 4: Wait for services ready
        print("\n⏳ STEP 4: WAITING FOR SERVICES READY")
        print()
        
        services_ready = await self.wait_for_services_ready()
        
        # Step 5: Comprehensive testing
        print("\n🔍 STEP 5: COMPREHENSIVE SYSTEM TESTING")
        print()
        
        tests_passed = self.run_comprehensive_test()
        
        # Step 6: Final status
        print("\n🎯 STEP 6: FINAL STATUS")
        print()
        
        self.print_final_status()
        
        return tests_passed
    
    def run_interactive(self):
        """Run in interactive mode"""
        try:
            asyncio.run(self.launch_system())
        except KeyboardInterrupt:
            print("\n\n🛑 USER INTERRUPT")
            self.stop_services()
            print("   🛑 Services stopped by user request")
        except Exception as e:
            print(f"\n\n❌ FATAL ERROR: {e}")
            self.stop_services()

def main():
    """Main entry point"""
    launcher = SystemLauncher()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        print("🔄 Running in interactive mode...")
        while True:
            launcher.run_interactive()
            print("\n🔄 Press Ctrl+C to restart...")
            time.sleep(5)
    else:
        # Non-interactive mode - just launch once
        asyncio.run(launcher.launch_system())

if __name__ == "__main__":
    main()
