# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A physical hardware display (the "usage cube") that shows Claude API usage statistics on an Arduino-driven screen. Two hardware variants exist — one using a 16x2 LCD, one using a 128x64 OLED — each implemented as a standalone Arduino sketch.

## Hardware Variants

### `lcd/main.ino`
- Display: 16x2 I2C LCD at address `0x27`
- Library: `LiquidCrystal_I2C`
- Shows two 10-block progress bars: `5H` (5-hour usage) and `7D` (7-day usage)
- Serial input format: `<5h_percent>,<7d_percent>\n` (e.g. `42,87`)

### `oled/oled_128x64.ino`
- Display: 128x64 I2C OLED at address `0x3C`
- Libraries: `Adafruit_SSD1306`, `Adafruit_GFX`
- Shows `5H` and `7D` metrics with fill bars and time-until-reset, plus a pixel-art Claude logo on the right
- Serial input format: `<5h_percent>,<7d_percent>,<5h_secs_remaining>,<7d_secs_remaining>\n` (e.g. `42,87,3600,86400`)
  - Seconds fields are optional; omit for "now" label
  - `formatTime()` renders seconds as `Xh00m` or `Xd00h`

## Development

These are Arduino sketches — there is no build system in this repo. Use the Arduino IDE or `arduino-cli` to compile and upload.

```bash
# Compile (example for oled sketch, adjust board/port as needed)
arduino-cli compile --fqbn arduino:avr:nano oled/

# Upload
arduino-cli upload -p COM3 --fqbn arduino:avr:nano oled/
```

Serial monitor at 9600 baud is used for both input and debug output (the OLED sketch echoes received lines back via `Serial.println`).
