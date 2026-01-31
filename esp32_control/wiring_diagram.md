# ESP32 Wiring Diagram

## Components Required

- ESP32 Development Board
- 3x LEDs (Red, Yellow, Green)
- 1x Buzzer (Piezo or Active)
- 1x I2C LCD (16x2) - Optional
- Resistors: 3x 220Ω (for LEDs), 1x 1kΩ (for buzzer if needed)
- Breadboard and jumper wires

## Pin Connections

### LEDs
- **Red LED**: GPIO 2 → LED → 220Ω resistor → GND
- **Yellow LED**: GPIO 4 → LED → 220Ω resistor → GND
- **Green LED**: GPIO 5 → LED → 220Ω resistor → GND

### Buzzer
- **Buzzer**: GPIO 18 → Buzzer (+) → Buzzer (-) → GND
  - Note: If using active buzzer, connect directly. For piezo, may need a transistor.

### LCD (I2C) - Optional
- **SDA**: GPIO 21
- **SCL**: GPIO 22
- **VCC**: 5V or 3.3V (check LCD module)
- **GND**: GND

## Circuit Layout

```
ESP32                    Components
------                   -----------
GPIO 2  ────[220Ω]───[LED Red]─── GND
GPIO 4  ────[220Ω]───[LED Yellow]─── GND
GPIO 5  ────[220Ω]───[LED Green]─── GND
GPIO 18 ────[Buzzer]─── GND
GPIO 21 ────[LCD SDA]
GPIO 22 ────[LCD SCL]
3.3V    ────[LCD VCC]
GND     ────[Common GND]
```

## Notes

1. **Power**: ESP32 can be powered via USB or external 5V supply
2. **Resistors**: Always use current-limiting resistors for LEDs (220Ω recommended)
3. **Buzzer**: Active buzzers are easier to use but check voltage requirements
4. **LCD**: I2C LCD modules simplify wiring - only 4 wires needed (VCC, GND, SDA, SCL)
5. **WiFi**: ESP32 has built-in WiFi - no additional components needed

## Testing

1. Upload `main.py` to ESP32
2. Update WiFi credentials in code
3. Update backend URL if needed
4. Power on and check serial monitor for connection status
5. LEDs should indicate system status:
   - Green: System ready, no alerts
   - Yellow: Medium/High alert
   - Red: Critical alert

## Troubleshooting

- **WiFi not connecting**: Check SSID and password
- **LEDs not working**: Check resistor values and connections
- **Buzzer not working**: Verify GPIO pin and buzzer polarity
- **No alerts received**: Check backend URL and network connectivity



