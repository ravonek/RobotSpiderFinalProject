# Project Abstract

This project presents a compact 4‑leg spider robot designed for basic locomotion experiments.
Each leg uses multiple hobby servos, allowing simple foot placement and body stabilization.
The robot is controlled using a MicroPython firmware running on a microcontroller board, and
a simulation workflow is provided using NVIDIA Isaac Sim for validating joint mappings and
testing keyframe gaits before running on hardware.

Key outcomes:
- Working servo mapping and per‑joint calibration (neutral offsets + direction inversion)
- A simple keyframe-based gait (trot-style stepping sequence)
- A simulation script that loads the robot and replays the gait with PD joint control
