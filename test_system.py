#!/usr/bin/env python3
"""
Simple system test for PRALAYA-NET
"""

import asyncio
import aiohttp
import json
import time

async def test_system():
    """Test all system components"""
    print("🔍 Testing PRALAYA-NET System...")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    tests_passed = 0
    tests_total = 5
    
    # Test 1: Backend health
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/api/health", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Test 1/5 - Backend Health: {data.get('status', 'unknown')}")
                    tests_passed += 1
                else:
                    print(f"❌ Test 1/5 - Backend Health: HTTP {response.status}")
    except Exception as e:
        print(f"❌ Test 1/5 - Backend Health: Error {e}")
    
    await asyncio.sleep(1)
    
    # Test 2: System status
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/api/system-status", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Test 2/5 - System Status: {data.get('backend_status', 'unknown')}")
                    tests_passed += 1
                else:
                    print(f"❌ Test 2/5 - System Status: HTTP {response.status}")
    except Exception as e:
        print(f"❌ Test 2/5 - System Status: Error {e}")
    
    await asyncio.sleep(1)
    
    # Test 3: Stability index
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/api/stability/current", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    score = data.get('stability_index', {}).get('overall_score', 0)
                    print(f"✅ Test 3/5 - Stability Index: {score:.2f}")
                    tests_passed += 1
                else:
                    print(f"❌ Test 3/5 - Stability Index: HTTP {response.status}")
    except Exception as e:
        print(f"❌ Test 3/5 - Stability Index: Error {e}")
    
    await asyncio.sleep(1)
    
    # Test 4: Enhanced Command Center
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:5173/enhanced-command-center", timeout=10) as response:
                if response.status == 200:
                    print(f"✅ Test 4/5 - Enhanced Command Center: HTTP {response.status}")
                    tests_passed += 1
                else:
                    print(f"❌ Test 4/5 - Enhanced Command Center: HTTP {response.status}")
    except Exception as e:
        print(f"❌ Test 4/5 - Enhanced Command Center: Error {e}")
    
    await asyncio.sleep(1)
    
    # Test 5: WebSocket connectivity
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"ws://127.0.0.1:8000/ws") as ws:
                await ws.send(json.dumps({"type": "test", "message": "ping"}))
                response = await ws.receive(timeout=5)
                if response:
                    print(f"✅ Test 5/5 - WebSocket: Connected")
                    tests_passed += 1
                else:
                    print(f"❌ Test 5/5 - WebSocket: No response")
    except Exception as e:
        print(f"❌ Test 5/5 - WebSocket: Error {e}")
    
    # Results
    print("="*60)
    print(f"🎯 TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("🎉 ALL TESTS PASSED - SYSTEM READY")
        print("📍 Access URLs:")
        print(f"   Backend API:        {base_url}")
        print(f"   Enhanced Command Center: http://localhost:5173/enhanced-command-center")
        print(f"   API Documentation:  {base_url}/docs")
        return True
    else:
        print("⚠️ SOME TESTS FAILED")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_system())
    if result:
        print("\n🌟 SYSTEM IS READY FOR PRODUCTION")
    else:
        print("\n❌ SYSTEM NEEDS ATTENTION")
    
    print("\nPress Ctrl+C to exit...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Test completed")
