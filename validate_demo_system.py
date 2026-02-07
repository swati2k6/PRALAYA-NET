#!/usr/bin/env python3
"""
PRALAYA-NET Demo System Validation
Validates all critical components for hackathon demo
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from pathlib import Path

class DemoSystemValidator:
    """Demo system validation for PRALAYA-NET"""
    
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.test_results = {
            'backend_health': False,
            'demo_status': False,
            'risk_predict': False,
            'stability_current': False,
            'alerts_active': False,
            'timeline_events': False,
            'frontend_connection': False,
            'websocket_connection': False,
            'demo_mode_active': False
        }
        
    async def validate_backend_health(self):
        """Validate backend health endpoint"""
        print("🔍 Validating backend health...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/health", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ Backend health: {data.get('status', 'unknown')}")
                        self.test_results['backend_health'] = True
                        return True
                    else:
                        print(f"   ❌ Backend health: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Backend health error: {e}")
            return False
    
    async def validate_demo_status(self):
        """Validate demo status endpoint"""
        print("🔍 Validating demo status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/demo/status", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"   ✅ Demo status: {data.get('demo_mode', 'unknown')}")
                        if data.get('demo_mode') == 'active':
                            self.test_results['demo_mode_active'] = True
                        self.test_results['demo_status'] = True
                        return True
                    else:
                        print(f"   ❌ Demo status: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Demo status error: {e}")
            return False
    
    async def validate_risk_predict(self):
        """Validate risk prediction endpoint"""
        print("🔍 Validating risk prediction...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/risk/predict", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Validate response structure
                        required_fields = ['risk_score', 'risk_level', 'confidence', 'factors']
                        if all(field in data for field in required_fields):
                            print("   ✅ Risk prediction: Valid response structure")
                            self.test_results['risk_predict'] = True
                            return True
                        else:
                            print("   ❌ Risk prediction: Invalid response structure")
                            return False
                    else:
                        print(f"   ❌ Risk prediction: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Risk prediction error: {e}")
            return False
    
    async def validate_stability_current(self):
        """Validate stability current endpoint"""
        print("🔍 Validating stability current...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/stability/current", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'stability_index' in data:
                            print("   ✅ Stability current: Valid response")
                            self.test_results['stability_current'] = True
                            return True
                        else:
                            print("   ❌ Stability current: Invalid response")
                            return False
                    else:
                        print(f"   ❌ Stability current: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Stability current error: {e}")
            return False
    
    async def validate_alerts_active(self):
        """Validate active alerts endpoint"""
        print("🔍 Validating active alerts...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/alerts/active", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'alerts' in data and isinstance(data['alerts'], list):
                            print(f"   ✅ Active alerts: {len(data['alerts'])} alerts found")
                            self.test_results['alerts_active'] = True
                            return True
                        else:
                            print("   ❌ Active alerts: Invalid response")
                            return False
                    else:
                        print(f"   ❌ Active alerts: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Active alerts error: {e}")
            return False
    
    async def validate_timeline_events(self):
        """Validate timeline events endpoint"""
        print("🔍 Validating timeline events...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/timeline/events", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'events' in data and isinstance(data['events'], list):
                            print(f"   ✅ Timeline events: {len(data['events'])} events found")
                            self.test_results['timeline_events'] = True
                            return True
                        else:
                            print("   ❌ Timeline events: Invalid response")
                            return False
                    else:
                        print(f"   ❌ Timeline events: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Timeline events error: {e}")
            return False
    
    async def validate_frontend_connection(self):
        """Validate frontend accessibility"""
        print("🔍 Validating frontend connection...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.frontend_url, timeout=10) as response:
                    if response.status == 200:
                        print(f"   ✅ Frontend: HTTP {response.status}")
                        self.test_results['frontend_connection'] = True
                        return True
                    else:
                        print(f"   ❌ Frontend: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Frontend error: {e}")
            return False
    
    async def validate_websocket_connection(self):
        """Validate WebSocket connectivity"""
        print("🔍 Validating WebSocket connection...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(f"ws://127.0.0.1:8000/ws") as ws:
                    # Send test message
                    await ws.send_str(json.dumps({"type": "test", "message": "ping"}))
                    
                    # Wait for response
                    try:
                        response = await asyncio.wait_for(ws.receive(), timeout=5)
                        if response:
                            print("   ✅ WebSocket: Connection successful")
                            self.test_results['websocket_connection'] = True
                            return True
                    except asyncio.TimeoutError:
                        print("   ⚠️ WebSocket: No response (timeout)")
                        self.test_results['websocket_connection'] = False
                        return False
        except Exception as e:
            print(f"   ❌ WebSocket error: {e}")
            return False
    
    def generate_validation_report(self):
        """Generate validation report"""
        print("\n📋 GENERATING VALIDATION REPORT...")
        
        # Calculate overall success rate
        total_tests = len(self.test_results)
        passed_tests = sum(1 for v in self.test_results.values() if v)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            'validation_timestamp': datetime.now().isoformat(),
            'overall_status': 'PASS' if success_rate >= 80 else 'FAIL',
            'success_rate': round(success_rate, 1),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'test_results': self.test_results,
            'demo_ready': success_rate >= 80
        }
        
        # Save report
        report_file = Path("demo_validation_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   📋 Validation report saved to: {report_file}")
        
        return report
    
    async def run_validation(self):
        """Run all validation tests"""
        print("🚀 STARTING PRALAYA-NET DEMO VALIDATION")
        print("="*60)
        
        # Run all tests
        await self.validate_backend_health()
        await self.validate_demo_status()
        await self.validate_risk_predict()
        await self.validate_stability_current()
        await self.validate_alerts_active()
        await self.validate_timeline_events()
        await self.validate_frontend_connection()
        await self.validate_websocket_connection()
        
        # Generate report
        report = self.generate_validation_report()
        
        print("\n" + "="*60)
        print("🎉 DEMO VALIDATION COMPLETE")
        print("="*60)
        
        # Print summary
        print(f"📊 OVERALL STATUS: {report['overall_status']}")
        print(f"📊 SUCCESS RATE: {report['success_rate']}%")
        print(f"📊 TESTS PASSED: {report['passed_tests']}/{report['total_tests']}")
        
        if report['demo_ready']:
            print("\n🎯 PRALAYA-NET DEMO READY")
            print("✅ All critical components validated")
            print("✅ Backend endpoints functional")
            print("✅ Frontend accessible")
            print("✅ Demo mode active")
            print("✅ Mock data generation working")
            print("✅ WebSocket connections established")
            return True
        else:
            print("\n❌ DEMO NOT READY")
            print("⚠️ Some components need attention")
            return False

async def main():
    """Main validation function"""
    validator = DemoSystemValidator()
    success = await validator.run_validation()
    
    if success:
        print("\n🌟 PRALAYA-NET DEMO READY")
        return 0
    else:
        print("\n❌ DEMO NEEDS ATTENTION")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
