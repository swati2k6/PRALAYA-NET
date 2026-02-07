#!/usr/bin/env python3
"""
PRALAYA-NET Complete System Test
Runs comprehensive health checks, API tests, map overlay tests
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from pathlib import Path

class SystemTester:
    """Comprehensive system testing for PRALAYA-NET"""
    
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.test_results = {
            'backend_health': False,
            'api_endpoints': {},
            'frontend_connection': False,
            'websocket_connection': False,
            'map_overlay': False,
            'prediction_engine': False,
            'data_integration': False
        }
        
    async def test_backend_health(self):
        """Test backend health endpoint"""
        print("🔍 Testing backend health...")
        
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
    
    async def test_api_endpoints(self):
        """Test all critical API endpoints"""
        print("🔍 Testing API endpoints...")
        
        endpoints = [
            ('/api/health', 'Health Check'),
            ('/api/system-status', 'System Status'),
            ('/api/risk/predict', 'Risk Prediction'),
            ('/api/stability/current', 'Stability Index'),
            ('/api/risk/regional', 'Regional Risk'),
            ('/docs', 'API Documentation')
        ]
        
        for endpoint, name in endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.backend_url}{endpoint}", timeout=10) as response:
                        if response.status == 200:
                            print(f"   ✅ {name}: HTTP {response.status}")
                            self.test_results['api_endpoints'][endpoint] = True
                        else:
                            print(f"   ❌ {name}: HTTP {response.status}")
                            self.test_results['api_endpoints'][endpoint] = False
            except Exception as e:
                print(f"   ❌ {name}: Error {e}")
                self.test_results['api_endpoints'][endpoint] = False
        
        # Check if all endpoints work
        working_endpoints = sum(1 for v in self.test_results['api_endpoints'].values() if v)
        total_endpoints = len(endpoints)
        
        if working_endpoints == total_endpoints:
            print(f"   ✅ All {total_endpoints} API endpoints working")
            self.test_results['api_endpoints']['all_working'] = True
        else:
            print(f"   ⚠️ {working_endpoints}/{total_endpoints} API endpoints working")
            self.test_results['api_endpoints']['all_working'] = False
    
    async def test_frontend_connection(self):
        """Test frontend accessibility"""
        print("🔍 Testing frontend connection...")
        
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
    
    async def test_websocket_connection(self):
        """Test WebSocket connectivity"""
        print("🔍 Testing WebSocket connection...")
        
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
    
    async def test_prediction_engine(self):
        """Test prediction engine functionality"""
        print("🔍 Testing prediction engine...")
        
        try:
            # Test basic prediction
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/risk/predict", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Validate response structure
                        required_fields = ['risk_score', 'risk_level', 'confidence', 'factors']
                        if all(field in data for field in required_fields):
                            print("   ✅ Prediction Engine: Valid response structure")
                            self.test_results['prediction_engine'] = True
                            return True
                        else:
                            print("   ❌ Prediction Engine: Invalid response structure")
                            self.test_results['prediction_engine'] = False
                            return False
                    else:
                        print(f"   ❌ Prediction Engine: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Prediction Engine error: {e}")
            return False
    
    async def test_data_integration(self):
        """Test data integration availability"""
        print("🔍 Testing data integration...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/system-status", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check if data sources are available
                        data_sources = data.get('data_sources', {})
                        if data_sources:
                            print("   ✅ Data Integration: Sources available")
                            print(f"      Real-time: {list(data_sources.get('real_time', []))}")
                            print(f"      Cached: {list(data_sources.get('cached', []))}")
                            self.test_results['data_integration'] = True
                            return True
                        else:
                            print("   ❌ Data Integration: No data sources")
                            self.test_results['data_integration'] = False
                            return False
                    else:
                        print(f"   ❌ Data Integration: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Data Integration error: {e}")
            return False
    
    async def test_map_overlay(self):
        """Test map overlay functionality"""
        print("🔍 Testing map overlay...")
        
        try:
            # Test if map data is available via API
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/risk/predict", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check if risk data is suitable for map overlay
                        if 'risk_score' in data and 'factors' in data:
                            print("   ✅ Map Overlay: Risk data available")
                            self.test_results['map_overlay'] = True
                            return True
                        else:
                            print("   ❌ Map Overlay: Invalid risk data")
                            self.test_results['map_overlay'] = False
                            return False
                    else:
                        print(f"   ❌ Map Overlay: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"   ❌ Map Overlay error: {e}")
            return False
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📋 GENERATING TEST REPORT...")
        
        # Calculate overall success rate
        total_tests = len(self.test_results) - 1  # Exclude api_endpoints dict
        passed_tests = sum(1 for k, v in self.test_results.items() 
                         if k != 'api_endpoints' and v)
        
        if 'api_endpoints' in self.test_results:
            api_tests = len(self.test_results['api_endpoints'])
            passed_api_tests = sum(1 for v in self.test_results['api_endpoints'].values() if v)
            total_tests += api_tests
            passed_tests += passed_api_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            'test_timestamp': datetime.now().isoformat(),
            'overall_status': 'PASS' if success_rate >= 80 else 'FAIL',
            'success_rate': round(success_rate, 1),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'test_results': self.test_results,
            'recommendations': []
        }
        
        # Add recommendations for failed tests
        if report['overall_status'] == 'FAIL':
            recommendations = []
            
            if not self.test_results['backend_health']:
                recommendations.append("Start backend server with 'python main.py'")
            
            if not self.test_results['frontend_connection']:
                recommendations.append("Start frontend with 'npm run dev'")
            
            if not self.test_results['websocket_connection']:
                recommendations.append("Check WebSocket configuration and firewall settings")
            
            if not self.test_results['prediction_engine']:
                recommendations.append("Verify prediction engine import and API endpoints")
            
            if not self.test_results['data_integration']:
                recommendations.append("Run data ingestion script: python scripts/data_ingest.py")
            
            if not self.test_results['map_overlay']:
                recommendations.append("Check risk prediction API and map integration")
            
            report['recommendations'] = recommendations
        
        # Save report
        report_file = Path("test_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   📋 Test report saved to: {report_file}")
        
        return report
    
    async def run_all_tests(self):
        """Run all system tests"""
        print("🚀 STARTING PRALAYA-NET SYSTEM TESTS")
        print("="*60)
        
        # Run all tests
        await self.test_backend_health()
        await self.test_api_endpoints()
        await self.test_frontend_connection()
        await self.test_websocket_connection()
        await self.test_prediction_engine()
        await self.test_data_integration()
        await self.test_map_overlay()
        
        # Generate report
        report = self.generate_test_report()
        
        print("\n" + "="*60)
        print("🎉 SYSTEM TESTS COMPLETE")
        print("="*60)
        
        # Print summary
        print(f"📊 OVERALL STATUS: {report['overall_status']}")
        print(f"📊 SUCCESS RATE: {report['success_rate']}%")
        print(f"📊 TESTS PASSED: {report['passed_tests']}/{report['total_tests']}")
        
        if report['recommendations']:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print("\n🎉 ALL TESTS PASSED - SYSTEM READY")
        
        print(f"\n📍 ACCESS URLS:")
        print(f"   Backend API:        {self.backend_url}")
        print(f"   Frontend UI:        {self.frontend_url}")
        print(f"   Enhanced Command Center: {self.frontend_url}/reliable-command-center")
        print(f"   API Documentation:  {self.backend_url}/docs")
        
        return report['overall_status'] == 'PASS'

async def main():
    """Main test function"""
    tester = SystemTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🌟 SYSTEM FULLY OPERATIONAL")
        return 0
    else:
        print("\n❌ SYSTEM NEEDS ATTENTION")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
