# Hardware

## Mechanical design
- 4 legs (front-left, front-right, back-left, back-right)
- Each leg is built from laser-cut / 3D-printed plates (depending on your build)
- Rubber / spherical foot tip for traction and smoother contact

## Actuation
- Hobby servos (multiple per leg; typical total: **12 servos**)
- Standard PWM control (50 Hz)

## Control electronics (typical)
- Microcontroller board: Raspberry Pi Pico / Pico W (MicroPython)
- External 5–6V power supply for servos (high current required)
- Common ground between MCU and servo power supply

## Wiring notes
- Keep servo power lines short and thick enough for current
- Use a stable power supply; sudden drops can reboot the MCU
- Test each joint individually before running gaits

## Bill of materials (example)
- 12× hobby servos
- 1× Raspberry Pi Pico (or compatible)
- 1× 5–6V power supply (adequate current for 12 servos)
- Frame + screws/spacers
