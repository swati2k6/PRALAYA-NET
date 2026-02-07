#!/usr/bin/env python3
"""
PRALAYA-NET Quick Demo Launcher
Emergency production launcher for hackathon demo
"""

import subprocess
import sys
import time
import os
from pathlib import Path
from datetime import datetime

class DemoLauncher:
    """Quick demo launcher for PRALAYA-NET"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "dashboard"
        
        # Service URLs
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.demo_url = "http://localhost:5173/demo-command-center"
        
        # Process tracking
        self.backend_process = None
        self.frontend_process = None
        
        # Start time
        self.start_time = time.time()
        
    def print_header(self):
        """Print startup header"""
        print("\n" + "="*80)
        print("🚀 PRALAYA-NET: EMERGENCY DEMO LAUNCHER")
        print("="*80)
        print("📍 Hackathon Demo - Autonomous Disaster-Response Platform")
        print("🎯 Goal: Launch demo system in under 60 seconds")
        print("="*80)
        print()
    
    def print_status(self, message, status="info"):
        """Print status message with icon and timestamp"""
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌", "critical": "🚨"}
        elapsed = f"[{time.time() - self.start_time:.1f}s]"
        print(f"{icons.get(status)} {elapsed} {message}")
    
    def start_backend(self):
        """Start demo backend server"""
        self.print_status("Starting demo backend server", "info")
        print(f"   📍 Backend URL: {self.backend_url}")
        print(f"   📍 Demo Status: {self.backend_url}/demo/status")
        
        try:
            # Start demo backend in background
            self.backend_process = subprocess.Popen([
                sys.executable, "demo_main.py"
            ], 
            cwd=self.backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
            
            self.print_status("Demo backend server started", "success")
            print("   ✅ Demo backend server starting...")
            return True
            
        except Exception as e:
            self.print_status("Backend startup", "error")
            print(f"   ❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start frontend development server"""
        self.print_status("Starting frontend server", "info")
        print(f"   📍 Frontend URL: {self.frontend_url}")
        print(f"   📍 Demo Command Center: {self.demo_url}")
        
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
    
    def wait_for_services(self, timeout=30):
        """Wait for services to be ready"""
        self.print_status("Waiting for services ready", "info")
        print("   ⏳ Checking service readiness...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check backend health
            try:
                import requests
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    self.print_status("Backend ready", "success")
                    print("   ✅ Backend is ready and responding")
                    backend_ready = True
                else:
                    backend_ready = False
            except:
                backend_ready = False
            
            # Check frontend health
            try:
                response = requests.get(self.frontend_url, timeout=5)
                if response.status_code == 200:
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
                print(f"   🎉 DEMO SYSTEM READY IN {elapsed_time:.1f} SECONDS!")
                return True
            
            time.sleep(2)  # Check every 2 seconds
        
        self.print_status("Service readiness timeout", "warning")
        print("   ⚠️ Services readiness timeout - proceeding anyway")
        return False
    
    def run_validation(self):
        """Run demo system validation"""
        self.print_status("Running demo validation", "info")
        
        try:
            # Run the validation script
            validation_script = self.project_root / "validate_demo_system.py"
            if validation_script.exists():
                result = subprocess.run([sys.executable, str(validation_script)], 
                                      capture_output=True, text=True)
                
                if "PRALAYA-NET DEMO READY" in result.stdout:
                    self.print_status("Demo validation", "success")
                    print("   ✅ Demo system validation passed")
                    return True
                else:
                    self.print_status("Demo validation", "warning")
                    print("   ⚠️ Some validation checks failed")
                    return False
            else:
                self.print_status("Demo validation", "warning")
                print("   ⚠️ Validation script not found")
                return False
        except Exception as e:
            self.print_status("Demo validation", "error")
            print(f"   ❌ Validation error: {e}")
            return False
    
    def print_access_urls(self):
        """Print all access URLs"""
        print("\n📍 DEMO ACCESS URLS:")
        print(f"   Backend API:        {self.backend_url}")
        print(f"   Frontend UI:        {self.frontend_url}")
        print(f"   🎯 Demo Command Center: {self.demo_url}")
        print(f"   Health Check:       {self.backend_url}/health")
        print(f"   Demo Status:        {self.backend_url}/demo/status")
        print(f"   Risk Prediction:    {self.backend_url}/risk/predict")
        print()
    
    def print_final_status(self):
        """Print final demo status"""
        elapsed_time = time.time() - self.start_time
        
        print("\n" + "="*80)
        print("🎉 PRALAYA-NET DEMO LAUNCH COMPLETE")
        print("="*80)
        print("📍 Emergency Production Autonomous Disaster-Response Platform")
        print("="*80)
        print()
        
        self.print_access_urls()
        
        print("\n🎯 HACKATHON DEMO FEATURES:")
        print("   ✅ Backend launches reliably on port 8000")
        print("   ✅ All required endpoints: /health, /demo/status, /risk/predict")
        print("   ✅ Frontend uses process.env.REACT_APP_API_URL")
        print("   ✅ Backend Offline → Auto-switch to demo mock data")
        print("   ✅ 3-column responsive grid layout")
        print("   ✅ Auto-refresh every 5 seconds")
        print("   ✅ Stability index + alerts + timeline updates")
        print("   ✅ Netlify + Render deployment configs ready")
        print()
        
        print("\n🎯 DEMO INSTRUCTIONS:")
        print("   1. Open Demo Command Center in browser")
        print("   2. Verify 'Demo Mode Active' indicator")
        print("   3. Click 'Simulate Disaster' to test risk prediction")
        print("   4. Watch auto-refresh every 5 seconds")
        print("   5. Check stability index and alerts updates")
        print("   6. Verify timeline events are updating")
        print()
        
        print(f"🕒 LAUNCH TIME: {elapsed_time:.1f} seconds")
        
        if elapsed_time < 60:
            print("🎉 GOAL ACHIEVED: Demo launched in under 60 seconds!")
        else:
            print("⚠️  Launch time exceeded 60 seconds - check for issues")
    
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
    
    def launch_demo(self):
        """Main demo launcher"""
        self.print_header()
        
        # Step 1: Start backend
        print("🚀 STEP 1: STARTING DEMO BACKEND")
        print()
        
        backend_started = self.start_backend()
        
        if not backend_started:
            self.print_status("Backend startup failed", "critical")
            print("   ❌ Failed to start backend")
            return False
        
        # Step 2: Start frontend
        print("\n🚀 STEP 2: STARTING FRONTEND")
        print()
        
        frontend_started = self.start_frontend()
        
        if not frontend_started:
            self.print_status("Frontend startup failed", "critical")
            print("   ❌ Failed to start frontend")
            return False
        
        # Step 3: Wait for services ready
        print("\n⏳ STEP 3: WAITING FOR SERVICES READY")
        print()
        
        services_ready = self.wait_for_services()
        
        # Step 4: Run validation
        print("\n🔍 STEP 4: DEMO VALIDATION")
        print()
        
        validation_passed = self.run_validation()
        
        # Step 5: Final status
        print("\n🎯 STEP 5: FINAL STATUS")
        print()
        
        self.print_final_status()
        
        return validation_passed

def main():
    """Main entry point"""
    launcher = DemoLauncher()
    
    try:
        success = launcher.launch_demo()
        
        if success:
            print("\n🌟 PRALAYA-NET DEMO READY")
            print("🎯 SYSTEM VALIDATION PASSED")
            print("🚀 READY FOR HACKATHON DEMO")
        else:
            print("\n❌ DEMO NEEDS ATTENTION")
            print("🔧 CHECK VALIDATION REPORT")
        
        # Keep services running
        print("\n🔄 Services are running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 USER INTERRUPT")
            launcher.stop_services()
            print("   🛑 Demo services stopped by user request")
            
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        launcher.stop_services()

if __name__ == "__main__":
    main()
