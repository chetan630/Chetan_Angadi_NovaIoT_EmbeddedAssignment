# Pin Mapping

## GPIO Assignment (ESP32-S3-WROOM-1)

| GPIO | Peripheral | Direction |
|------|------------|-----------|
| GPIO8 | SHT41 SDA | I2C |
| GPIO9 | SHT41 SCL | I2C |
| GPIO8 | BH1750 SDA (shared I2C bus) | I2C |
| GPIO9 | BH1750 SCL (shared I2C bus) | I2C |
| GPIO8 | LIS3DH SDA (shared I2C bus) | I2C |
| GPIO9 | LIS3DH SCL (shared I2C bus) | I2C |
| GPIO4 | Reed Switch | Input |
| GPIO5 | RGB LED — Red | Output |
| GPIO6 | RGB LED — Green | Output |
| GPIO7 | RGB LED — Blue | Output |
| GPIO15 | Active Buzzer | Output |
| GPIO1 | Battery Monitor (ADC1_CH0) | Analog Input |
| GPIO12 | SPI SCK (shared bus) | SPI |
| GPIO11 | SPI MOSI (shared bus) | SPI |
| GPIO13 | SPI MISO (shared bus) | SPI |
| GPIO10 | SPI Flash — Chip Select | Output |
| GPIO14 | MicroSD — Chip Select | Output |
| GPIO19 | USB D- (native USB) | USB |
| GPIO20 | USB D+ (native USB) | USB |

**Notes**

- SHT41, BH1750, and LIS3DH share a single I2C bus (GPIO8/GPIO9) — each
  device has a distinct I2C address, so no separate bus is required.
- SPI Flash and the MicroSD card share one SPI bus (SCK/MOSI/MISO) and are
  selected individually via their own chip-select lines (GPIO10, GPIO14),
  which keeps pin usage low as more SPI peripherals are added.
- Reed switch input uses an internal pull-up; the switch pulls the line
  low when the door is closed.
- Strapping pins (GPIO0, GPIO3, GPIO45, GPIO46) are intentionally left
  unused for peripherals, since their state is sampled at boot and
  reserved for flash/PSRAM voltage and boot-mode selection on the
  ESP32-S3.
- Debug/programming uses the ESP32-S3's native USB (GPIO19/GPIO20)
  rather than a separate USB-UART bridge chip, reducing BOM cost.

## Interface Summary

| Peripheral | Interface | Notes |
|------------|-----------|-------|
| SHT41 | I²C | Temperature & Humidity |
| BH1750 | I²C | Ambient Light |
| LIS3DH | I²C | Vibration |
| Reed Switch | GPIO | Door Status |
| RGB LED | GPIO | Status Indicator |
| Active Buzzer | GPIO | Audible Alert |
| Battery Monitor | ADC | Voltage Divider |
| SPI Flash | SPI | Event Buffer |
| Industrial MicroSD | SPI | Historical Logs |
| USB Debug | USB | Programming & Diagnostics |
