# Gait

The project uses a simple keyframe gait intended for stable walking on flat surfaces.

## Idea
- Move one diagonal pair (or single legs) while the others support the body
- Use a “lift → swing → place → push” pattern

## Firmware gait
The MicroPython demo shows a trot-like stepping sequence by commanding joint angles
for each leg with small delays between steps.

## Simulation gait
The Isaac Sim script contains keyframes (joint position targets). Between frames, the
script interpolates targets to make motion smoother.

## Tuning tips
- Start with small step amplitude (short swing) and slow timing
- Ensure neutral offsets are correct before increasing speed
- If a leg moves backward, flip its sign in `DIRECTION_MAP`
