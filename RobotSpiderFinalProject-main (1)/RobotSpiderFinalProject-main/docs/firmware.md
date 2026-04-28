# Firmware (MicroPython)

File: `firmware/pico/spider_firmware.py`

## Key parameters
- `FREQ = 50` — standard servo PWM frequency
- `NEUTRAL_OFFSETS` — per-joint neutral (calibration)
- `DIRECTION_MAP` — +1 or -1 per joint to fix mirrored orientation
- `SERVO_PINS` — GPIO pins used for each servo signal

## Calibration workflow
1. Run a “neutral pose” command (all joints at 90° + offset).
2. Adjust `NEUTRAL_OFFSETS` so each leg is symmetric and the foot is placed correctly.
3. If a joint moves in the opposite direction, flip its sign in `DIRECTION_MAP`.
4. Repeat until all legs behave consistently.

## Safety
- Use an external servo power supply (5–6V) with enough current
- Share ground between MCU and servo PSU
- Keep initial tests slow and small-range
