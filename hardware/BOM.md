# Bill of Materials (BOM)

| Item | Component | Manufacturer | Purpose | Qty |
|------|-----------|--------------|---------|----|
| MCU | ESP32-S3-WROOM-1 | Espressif | Main Controller | 1 |
| Sensor | SHT41-AD1B | Sensirion | Temperature & Humidity Monitoring | 1 |
| Power | Resettable PTC Fuse | Littelfuse (or equivalent) | Overcurrent Protection | 1 |
| Power | P-Channel MOSFET | AO3407A (or equivalent) | Reverse Polarity Protection | 1 |
| Power | SMBJ33A TVS Diode | Littelfuse | Transient Voltage Protection | 1 |
| Power | LM2596HV | Texas Instruments | Buck Converter (12V/24V → 5V) | 1 |
| Power | 3.3V LDO Regulator | AP2112K / AMS1117-3.3* | 5V → 3.3V Regulation | 1 |
| Storage | W25Q64JV SPI Flash | Winbond | Event Buffer | 1 |
| Storage | Industrial MicroSD 8 GB | Kingston | Historical Data Storage | 1 |
| Storage | Hinged MicroSD Socket | Generic Industrial | Secure Card Mounting | 1 |
| Sensor | Magnetic Reed Switch | Generic | Door Status Detection | 1 |
| Sensor | BH1750 | Rohm | Ambient Light Detection | 1 |
| Sensor | LIS3DH | STMicroelectronics | Vibration & Shock Detection | 1 |
| Circuit | Resistor Divider Network | Generic | Battery Voltage Monitoring | 2 Resistors |