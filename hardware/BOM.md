# Bill of Materials (BOM)

| Item | Component | Manufacturer | Part Number | Purpose | Qty |
|------|-----------|--------------|--------------|---------|-----|
| MCU | ESP32-S3 Module (16MB Flash / 8MB PSRAM) | Espressif Systems | ESP32-S3-WROOM-1-N16R8 | Main Controller | 1 |
| Sensor | Temperature & Humidity Sensor | Sensirion | SHT41-AD1B | Temperature & Humidity Monitoring | 1 |
| Power | Resettable PTC Fuse (0.5A hold) | Littelfuse | 1210L050YR | Overcurrent Protection | 1 |
| Power | P-Channel MOSFET | Alpha & Omega Semiconductor | AO3407A | Reverse Polarity Protection | 1 |
| Power | TVS Diode (33V) | Littelfuse | SMBJ33A | Transient Voltage Protection | 1 |
| Power | Buck Converter (12V/24V → 5V) | Texas Instruments | LM2596HV | Step-Down Regulation | 1 |
| Power | 3.3V LDO Regulator | Diodes Incorporated | AP2112K-3.3TRG1 | 5V → 3.3V Regulation | 1 |
| Storage | SPI NOR Flash (64 Mbit) | Winbond | W25Q64JVSSIQ | Event Buffer | 1 |
| Storage | Industrial MicroSD Card (8 GB) | Kingston | SDCIT2/8GB | Historical Data Storage | 1 |
| Storage | MicroSD Card Socket (push-push, hinged) | Molex | 104031-0811 | Secure Card Mounting | 1 |
| Sensor | Magnetic Reed Switch | Standex-Meder Electronics | MK24-1A66C | Door Status Detection | 1 |
| Sensor | Ambient Light Sensor | Rohm Semiconductor | BH1750FVI-TR | Ambient Light Detection | 1 |
| Sensor | 3-Axis Accelerometer | STMicroelectronics | LIS3DH | Vibration & Shock Detection | 1 |
| Circuit | Precision Resistors (100 kΩ / 22 kΩ, 0603, 1%) | Yageo | RC0603FR-07100KL / RC0603FR-0722KL | Battery Voltage Divider (ADC Scaling) | 2 |

**Notes**

- Part numbers reflect a representative, sourceable option per component;
  final selection should be confirmed against current distributor stock
  (DigiKey/Mouser) and lead time before production ordering.
- `ESP32-S3-WROOM-1-N16R8` was selected over lower-memory variants
  (e.g. N4, N8) to leave comfortable headroom for FreeRTOS, the TLS stack
  needed for future cloud connectivity, and OTA update partitioning.
- The LDO alternate previously listed (AMS1117-3.3) was dropped in favor
  of a single specified part (AP2112K-3.3TRG1), which has a lower dropout
  voltage and better line/load regulation — relevant given the buck
  converter output tolerance feeding it.