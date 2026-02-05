/**
 * PRALAYA-NET ESP32 Hardware Controller
 * 
 * Hardware Setup:
 * - GPIO 23: Buzzer (piezo sounder)
 * - GPIO 22: Red LED (HIGH RISK alert)
 * - GPIO 21: Green LED (SAFE status)
 * - WiFi: Connects to backend for alert polling
 * 
 * Operation:
 * - Polls backend API every 10 seconds for risk status
 * - HIGH RISK (>0.8): Activates buzzer + red LED (pulsing)
 * - MEDIUM RISK (0.6-0.8): Red LED steady
 * - LOW RISK (<0.6): Green LED ON
 * - ERROR: All LEDs blink
 * 
 * Author: PRALAYA-NET
 * Version: 1.0
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ============ CONFIGURATION ============
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* BACKEND_URL = "http://192.168.1.100:8000";  // Update with your backend IP
const int POLL_INTERVAL = 10000;  // 10 seconds
const int BUZZER_FREQ = 2000;     // 2kHz buzzer frequency
const int BUZZER_DUTY = 180;      // PWM duty cycle (0-255)

// ============ GPIO PINS ============
const int PIN_BUZZER = 23;        // Buzzer
const int PIN_LED_RED = 22;       // Red LED (HIGH RISK)
const int PIN_LED_GREEN = 21;     // Green LED (SAFE)

// ============ PWM CHANNELS ============
const int PWM_CHANNEL_BUZZER = 0;
const int PWM_CHANNEL_RED = 1;
const int PWM_CHANNEL_GREEN = 2;
const int PWM_FREQ = 5000;        // 5kHz PWM frequency
const int PWM_RESOLUTION = 8;     // 8-bit resolution (0-255)

// ============ RISK THRESHOLDS ============
const float HIGH_RISK_THRESHOLD = 0.8;
const float MEDIUM_RISK_THRESHOLD = 0.6;
const float LOW_RISK_THRESHOLD = 0.3;

// ============ STATE VARIABLES ============
unsigned long last_poll = 0;
String current_status = "initializing";
float current_risk = 0.0;
bool wifi_connected = false;
bool buzzer_active = false;
unsigned long buzzer_pulse_start = 0;
const int BUZZER_PULSE_DURATION = 500;  // 500ms pulses

// ============ SETUP ============
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n======================================");
  Serial.println("PRALAYA-NET ESP32 Hardware Controller");
  Serial.println("======================================");
  
  // Initialize GPIO pins
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  
  // Configure PWM for buzzer and LEDs
  ledcSetup(PWM_CHANNEL_BUZZER, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_RED, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_GREEN, PWM_FREQ, PWM_RESOLUTION);
  
  // Attach pins to PWM channels
  ledcAttachPin(PIN_BUZZER, PWM_CHANNEL_BUZZER);
  ledcAttachPin(PIN_LED_RED, PWM_CHANNEL_RED);
  ledcAttachPin(PIN_LED_GREEN, PWM_CHANNEL_GREEN);
  
  // All OFF initially
  all_leds_off();
  
  Serial.println("Hardware initialized");
  Serial.print("Buzzer GPIO: "); Serial.println(PIN_BUZZER);
  Serial.print("Red LED GPIO: "); Serial.println(PIN_LED_RED);
  Serial.print("Green LED GPIO: "); Serial.println(PIN_LED_GREEN);
  
  // Self-test: Blink all LEDs
  self_test();
  
  // Connect to WiFi
  connect_to_wifi();
}

// ============ MAIN LOOP ============
void loop() {
  // Check WiFi connection
  if (!WiFi.isConnected()) {
    if (wifi_connected) {
      Serial.println("WiFi disconnected!");
      wifi_connected = false;
    }
    blink_error_leds();
    delay(1000);
    return;
  }
  
  wifi_connected = true;
  
  // Poll backend at regular intervals
  unsigned long now = millis();
  if (now - last_poll >= POLL_INTERVAL) {
    poll_backend();
    last_poll = now;
  }
  
  // Update buzzer state (pulsing effect)
  if (buzzer_active) {
    update_buzzer_pulse();
  }
  
  delay(100);  // Small delay to prevent watchdog timeout
}

// ============ WiFi CONNECTION ============
void connect_to_wifi() {
  Serial.print("\nConnecting to WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.isConnected()) {
    Serial.println();
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.print("RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
    wifi_connected = true;
  } else {
    Serial.println();
    Serial.println("Failed to connect to WiFi!");
    wifi_connected = false;
  }
}

// ============ BACKEND POLLING ============
void poll_backend() {
  if (!WiFi.isConnected()) {
    Serial.println("WiFi not connected");
    return;
  }
  
  String api_url = String(BACKEND_URL) + "/api/risk-alert";
  
  HTTPClient http;
  http.setTimeout(5000);  // 5 second timeout
  http.begin(api_url);
  
  int http_response = http.GET();
  
  if (http_response == HTTP_CODE_OK) {
    String payload = http.getString();
    parse_backend_response(payload);
  } else if (http_response > 0) {
    Serial.print("HTTP Error: ");
    Serial.println(http_response);
  } else {
    Serial.print("HTTP Error: ");
    Serial.println(http.errorToString(http_response));
  }
  
  http.end();
}

// ============ PARSE BACKEND RESPONSE ============
void parse_backend_response(String payload) {
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, payload);
  
  if (error) {
    Serial.print("JSON parse error: ");
    Serial.println(error.f_str());
    blink_error_leds();
    return;
  }
  
  // Extract risk data
  float risk_score = doc["risk_score"] | 0.0;
  String risk_level = doc["risk_level"] | "unknown";
  String hardware_action = doc["hardware_action"] | "none";
  
  current_risk = risk_score;
  current_status = risk_level;
  
  Serial.print("Risk Score: ");
  Serial.print(risk_score, 2);
  Serial.print(" | Level: ");
  Serial.print(risk_level);
  Serial.print(" | Action: ");
  Serial.println(hardware_action);
  
  // Execute hardware action based on risk level
  execute_hardware_action(risk_score, risk_level, hardware_action);
}

// ============ EXECUTE HARDWARE ACTIONS ============
void execute_hardware_action(float risk_score, String risk_level, String action) {
  // Clear all previous states
  all_leds_off();
  buzzer_active = false;
  
  if (risk_score >= HIGH_RISK_THRESHOLD) {
    // HIGH RISK: Activate buzzer + red LED pulsing
    Serial.println(">>> ACTIVATING HIGH RISK ALERT <<<");
    activate_high_risk_alert();
  } 
  else if (risk_score >= MEDIUM_RISK_THRESHOLD) {
    // MEDIUM RISK: Red LED steady
    Serial.println(">>> MEDIUM RISK - Red LED ON <<<");
    ledcWrite(PWM_CHANNEL_RED, 255);  // Full brightness
  }
  else if (risk_score >= LOW_RISK_THRESHOLD) {
    // LOW RISK: Green LED ON
    Serial.println(">>> LOW RISK - Green LED ON <<<");
    ledcWrite(PWM_CHANNEL_GREEN, 255);  // Full brightness
  }
  else {
    // SAFE: Green LED ON
    Serial.println(">>> SAFE - Green LED ON <<<");
    ledcWrite(PWM_CHANNEL_GREEN, 255);  // Full brightness
  }
}

// ============ HIGH RISK ALERT ============
void activate_high_risk_alert() {
  // Buzzer activation (pulsing)
  buzzer_active = true;
  buzzer_pulse_start = millis();
  
  // Red LED pulsing effect
  ledcWrite(PWM_CHANNEL_RED, 200);
}

// ============ UPDATE BUZZER PULSE ============
void update_buzzer_pulse() {
  unsigned long elapsed = millis() - buzzer_pulse_start;
  
  // Pulsing pattern: 200ms ON, 200ms OFF
  if ((elapsed % 400) < 200) {
    ledcWrite(PWM_CHANNEL_BUZZER, BUZZER_DUTY);  // Buzzer ON
  } else {
    ledcWrite(PWM_CHANNEL_BUZZER, 0);             // Buzzer OFF
  }
}

// ============ ERROR HANDLING ============
void blink_error_leds() {
  // All LEDs blinking (error state)
  static unsigned long last_blink = 0;
  static bool blink_state = false;
  
  if (millis() - last_blink > 300) {
    blink_state = !blink_state;
    last_blink = millis();
    
    if (blink_state) {
      ledcWrite(PWM_CHANNEL_RED, 255);
      ledcWrite(PWM_CHANNEL_GREEN, 255);
    } else {
      all_leds_off();
    }
  }
}

// ============ UTILITY FUNCTIONS ============
void all_leds_off() {
  ledcWrite(PWM_CHANNEL_BUZZER, 0);
  ledcWrite(PWM_CHANNEL_RED, 0);
  ledcWrite(PWM_CHANNEL_GREEN, 0);
}

void self_test() {
  Serial.println("\nRunning self-test...");
  
  // Green LED
  Serial.println("Testing GREEN LED...");
  ledcWrite(PWM_CHANNEL_GREEN, 255);
  delay(500);
  ledcWrite(PWM_CHANNEL_GREEN, 0);
  
  // Red LED
  Serial.println("Testing RED LED...");
  ledcWrite(PWM_CHANNEL_RED, 255);
  delay(500);
  ledcWrite(PWM_CHANNEL_RED, 0);
  
  // Buzzer
  Serial.println("Testing BUZZER...");
  ledcWrite(PWM_CHANNEL_BUZZER, BUZZER_DUTY);
  delay(300);
  ledcWrite(PWM_CHANNEL_BUZZER, 0);
  
  Serial.println("Self-test complete!\n");
}
