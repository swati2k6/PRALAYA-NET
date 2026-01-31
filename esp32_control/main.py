"""
ESP32 Main Code - PRALAYA-NET Edge Unit
Controls LCD, LEDs, and buzzer for disaster alerts
"""

import network
import urequests
import time
from machine import Pin, PWM
import json

# Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
BACKEND_URL = "http://192.168.1.100:8000"  # Update with your backend IP
POLL_INTERVAL = 10  # seconds

# Hardware pins (adjust based on your wiring)
LED_RED_PIN = 2
LED_YELLOW_PIN = 4
LED_GREEN_PIN = 5
BUZZER_PIN = 18
LCD_SDA = 21
LCD_SCL = 22

class ESP32EdgeUnit:
    """
    ESP32 Edge Unit for PRALAYA-NET
    Polls backend for alerts and triggers hardware responses
    """
    
    def __init__(self):
        self.wifi_connected = False
        self.sta = network.WLAN(network.STA_IF)
        
        # Initialize hardware
        self.led_red = Pin(LED_RED_PIN, Pin.OUT)
        self.led_yellow = Pin(LED_YELLOW_PIN, Pin.OUT)
        self.led_green = Pin(LED_GREEN_PIN, Pin.OUT)
        self.buzzer = PWM(Pin(BUZZER_PIN))
        self.buzzer.freq(1000)
        self.buzzer.duty(0)
        
        # Initialize LCD (if using I2C LCD)
        # self.lcd = self._init_lcd()
        
    def connect_wifi(self):
        """Connect to WiFi network"""
        if not self.sta.isconnected():
            print("Connecting to WiFi...")
            self.sta.active(True)
            self.sta.connect(WIFI_SSID, WIFI_PASSWORD)
            
            # Wait for connection
            timeout = 20
            while not self.sta.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
                print(".", end="")
            
            if self.sta.isconnected():
                self.wifi_connected = True
                print("\nWiFi connected!")
                print(f"IP: {self.sta.ifconfig()[0]}")
                return True
            else:
                print("\nWiFi connection failed")
                return False
        else:
            self.wifi_connected = True
            return True
    
    def fetch_alerts(self):
        """Fetch alerts from backend"""
        try:
            url = f"{BACKEND_URL}/api/orchestration/alerts/esp32"
            response = urequests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                response.close()
                return data.get("alerts", [])
            else:
                response.close()
                return []
        except Exception as e:
            print(f"Error fetching alerts: {e}")
            return []
    
    def process_alert(self, alert):
        """
        Process an alert and trigger hardware responses
        
        Args:
            alert: Alert dictionary with type, severity, message
        """
        alert_type = alert.get("type", "unknown")
        severity = alert.get("severity", 0.5)
        message = alert.get("message", "Alert")
        
        print(f"Alert: {alert_type} - {message} (Severity: {severity})")
        
        # Determine alert level
        if severity >= 0.8:
            self._trigger_critical_alert(message)
        elif severity >= 0.6:
            self._trigger_high_alert(message)
        elif severity >= 0.3:
            self._trigger_medium_alert(message)
        else:
            self._trigger_low_alert(message)
    
    def _trigger_critical_alert(self, message):
        """Trigger critical alert (red LED, buzzer)"""
        self.led_red.on()
        self.led_yellow.off()
        self.led_green.off()
        
        # Buzzer pattern: rapid beeps
        for _ in range(5):
            self.buzzer.duty(512)  # 50% duty cycle
            time.sleep(0.2)
            self.buzzer.duty(0)
            time.sleep(0.1)
        
        # Display on LCD if available
        # self.lcd.clear()
        # self.lcd.putstr("CRITICAL!")
        # self.lcd.putstr(message[:16], line=1)
    
    def _trigger_high_alert(self, message):
        """Trigger high alert (yellow LED, slow beeps)"""
        self.led_red.off()
        self.led_yellow.on()
        self.led_green.off()
        
        # Buzzer pattern: slow beeps
        for _ in range(3):
            self.buzzer.duty(512)
            time.sleep(0.3)
            self.buzzer.duty(0)
            time.sleep(0.2)
    
    def _trigger_medium_alert(self, message):
        """Trigger medium alert (yellow LED, single beep)"""
        self.led_red.off()
        self.led_yellow.on()
        self.led_green.off()
        
        # Single beep
        self.buzzer.duty(512)
        time.sleep(0.2)
        self.buzzer.duty(0)
    
    def _trigger_low_alert(self, message):
        """Trigger low alert (green LED, no sound)"""
        self.led_red.off()
        self.led_yellow.off()
        self.led_green.on()
        
        # No buzzer for low alerts
    
    def clear_alerts(self):
        """Clear all alerts (turn off LEDs and buzzer)"""
        self.led_red.off()
        self.led_yellow.off()
        self.led_green.off()
        self.buzzer.duty(0)
    
    def run(self):
        """Main loop"""
        print("PRALAYA-NET ESP32 Edge Unit Starting...")
        
        # Connect to WiFi
        if not self.connect_wifi():
            print("Failed to connect to WiFi. Running in offline mode.")
            # Blink red LED to indicate WiFi failure
            for _ in range(5):
                self.led_red.on()
                time.sleep(0.5)
                self.led_red.off()
                time.sleep(0.5)
            return
        
        # Initial status: green LED
        self.led_green.on()
        print("System ready. Polling for alerts...")
        
        last_alert_time = 0
        
        while True:
            try:
                # Fetch alerts
                alerts = self.fetch_alerts()
                
                if alerts:
                    for alert in alerts:
                        self.process_alert(alert)
                        last_alert_time = time.time()
                else:
                    # No alerts - clear after 30 seconds
                    if time.time() - last_alert_time > 30:
                        self.clear_alerts()
                        self.led_green.on()  # System ready indicator
                
                time.sleep(POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.clear_alerts()
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    unit = ESP32EdgeUnit()
    unit.run()
