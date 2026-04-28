# System Architecture

## Repository components

### Firmware (MicroPython)
Located in `firmware/pico/spider_firmware.py`.

Responsibilities:
- Servo PWM generation @ 50 Hz
- Calibration via `NEUTRAL_OFFSETS`
- Orientation fixes via `DIRECTION_MAP`
- Gait playback via time-stepped joint commands

### Simulation (Isaac Sim)
Located in `sim/isaac/spider_isaac_sim.py`.

Responsibilities:
- Launch Isaac Sim
- Load robot USD stage
- Map joint names to DOF indices
- Apply PD gains and replay a keyframe gait

### Models and media
- `assets/urdf/` — URDF model
- `assets/images/` — photos and CAD renders
- `assets/demo/` — demo videos (use Git LFS for large files)

## Data flow

1. Design robot geometry (CAD) → export URDF/USD
2. Validate joints in simulation (mapping + PD gains)
3. Tune neutral offsets and direction mapping on hardware
4. Replay gait keyframes on the real robot
