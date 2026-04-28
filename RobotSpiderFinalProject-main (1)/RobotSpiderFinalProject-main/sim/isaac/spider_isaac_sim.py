"""
Simple keyframe-based crawl gait for a quadruped "spider" robot in NVIDIA Isaac Sim.

- Loads a USD asset (spdrstiff.usd)
- Sets up world, ground plane, and camera
- Maps DOFs by name to logical legs
- Uses incremental joint angles (keyframes) to define a repeating gait
- Interpolates between keyframes for smooth motion
"""

from isaacsim import SimulationApp

# Launch Isaac Sim in non-headless mode (with UI)
simulation_app = SimulationApp({"headless": False})

import numpy as np
import carb
import time

from isaacsim.core.api import World
from isaacsim.core.prims import Articulation
from isaacsim.core.utils.stage import add_reference_to_stage, get_stage_units
from isaacsim.core.utils.viewports import set_camera_view


# ==========================
# 1. WORLD AND CAMERA
# ==========================
my_world = World(stage_units_in_meters=1.0)
my_world.scene.add_default_ground_plane()

set_camera_view(
    eye=[2.5, 2.5, 1.5],
    target=[0.0, 0.0, 0.5],
    camera_prim_path="/OmniverseKit_Persp",
)

# ==========================
# 2. LOAD ROBOT
# ==========================
# Change this path to your local robot USD file
asset_path = r"C:/Users/user/Desktop/spider_bot (2)/spider_bot/spdrstiff.usd"

add_reference_to_stage(usd_path=asset_path, prim_path="/World/paukrobotFinished")
spider = Articulation(prim_paths_expr="/World/paukrobotFinished", name="my_spider")

# Place the robot at z = 0, physics will settle it on the ground plane
spider.set_world_poses(positions=np.array([[0.0, 0.0, 0.0]]) / get_stage_units())

# ==========================
# 3. KEYFRAMES — ΔANGLES (INCREMENTS)
#
# Logical leg naming:
#   FR = Front Right  (PP in original Russian comments)
#   FL = Front Left   (PL)
#   RR = Rear Right   (ZP)
#   RL = Rear Left    (ZL)
#
# Column order:
#   0  FR_H  – Front Right hip
#   1  FR_K  – Front Right knee
#   2  FR_L  – Front Right last joint
#   3  FL_H  – Front Left hip
#   4  FL_K  – Front Left knee
#   5  FL_L  – Front Left last joint
#   6  RR_H  – Rear Right hip
#   7  RR_K  – Rear Right knee
#   8  RR_L  – Rear Right last joint
#   9  RL_H  – Rear Left hip
#  10  RL_K  – Rear Left knee
#  11  RL_L  – Rear Left last joint
#
# Each row is an incremental angle added to the current joint configuration,
# defining a step of the gait cycle.
# ==========================
keyframe_sequence = np.array([
    #  FR_H   FR_K     FR_L       FL_H    FL_K     FL_L       RR_H    RR_K     RR_L       RL_H    RL_K     RL_L

    # 0: idle / pause
    [ 0.0,   0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0 ],

    # ===== 1) FRONT RIGHT LEG (FR) =====
    # 1: FR – lift (knee slightly up, last joint up)
    [ 0.0,  -0.14,   0.14,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0 ],

    # 2: FR – swing forward (hip forward)
    [ 0.5,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0 ],

    # 3: FR – landing (return in height)
    [ 0.0,   0.14,  -0.14,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0 ],

    # 4: pause
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,     0.0 ],

    # ===== 2) REAR LEFT LEG (RL) =====
    # 5: RL – lift
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,   -0.14,   0.14 ],

    # 6: RL – swing forward
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.945,  0.0,    0.0 ],

    # 7: RL – landing
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.14,  -0.14 ],

    # 8: pause
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,    0.0 ],

    # ===== 3) FRONT LEFT LEG (FL) =====
    # 9: FL – lift
    [ 0.0,   0.0,    0.0,        0.0,   -0.14,   0.14,       0.0,    0.0,     0.0,       0.0,    0.0,    0.0 ],

    # 10: FL – swing forward
    [ 0.0,   0.0,    0.0,       -0.4,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,    0.0 ],

    # 11: FL – landing
    [ 0.0,   0.0,    0.0,        0.0,    0.14,  -0.14,       0.0,    0.0,     0.0,       0.0,    0.0,    0.0 ],

    # 12: pause
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,       0.0,    0.0,    0.0 ],

    # ===== 4) REAR RIGHT LEG (RR) =====
    # 13: RR – lift
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,   -0.14,   0.14,      0.0,    0.0,    0.0 ],

    # 14: RR – swing forward
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,      -0.8,   0.0,     0.0,       0.0,    0.0,    0.0 ],

    # 15: RR – landing
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.14,  -0.14,      0.0,    0.0,    0.0 ],

    # 16: pause
    [ 0.0,   0.0,    0.0,        0.0,    0.0,     0.0,       0.0,    0.0,     0.0,      0.0,    0.0,    0.0 ],

    # 17: body pull / body advance
    [ -0.5,  0.0,    0.0,        0.4,   0.0,     0.0,       0.8,    0.0,     0.0,      -0.945,  0.0,    0.0 ],
], dtype=float)

num_keyframes = keyframe_sequence.shape[0]

# ==========================
# 4. WORLD AND ROBOT INITIALIZATION
# ==========================
my_world.reset()
my_world.step()
spider.initialize()

# ==========================
# 5. DOF NAME → INDEX MAPPING
# ==========================
try:
    dof_names = spider.get_dof_names()
except AttributeError:
    dof_names = spider.dof_names

print("===== DOF NAMES (index : name) =====")
name_to_index = {}
for i, name in enumerate(dof_names):
    print(f"{i:2d} : {name}")
    name_to_index[name] = i


def idx(joint_name: str) -> int:
    """Helper to get DOF index by joint name (raises if not found)."""
    if joint_name not in name_to_index:
        raise KeyError(f"Joint name '{joint_name}' not found in dof_names")
    return name_to_index[joint_name]


# Mapping your specific USD joint names to the logical legs.
# Adjust these if your USD joint naming changes.
FR_HIP  = idx("Revolute_10")
FR_KNEE = idx("Revolute_35")
FR_LAST = idx("Revolute_36")

FL_HIP  = idx("Revolute_4")
FL_KNEE = idx("Revolute_33")
FL_LAST = idx("Revolute_34")

RR_HIP  = idx("Revolute_7")
RR_KNEE = idx("Revolute_30")
RR_LAST = idx("Revolute_31")

RL_HIP  = idx("Revolute_1")
RL_KNEE = idx("Revolute_32")
RL_LAST = idx("Revolute_37")

print("\n===== MAPPING keyframe (Δ) -> joints =====")
print("Δ[:, 0]  -> FR_HIP  ->", FR_HIP,  dof_names[FR_HIP])
print("Δ[:, 1]  -> FR_KNEE ->", FR_KNEE, dof_names[FR_KNEE])
print("Δ[:, 2]  -> FR_LAST ->", FR_LAST, dof_names[FR_LAST])
print("Δ[:, 3]  -> FL_HIP  ->", FL_HIP,  dof_names[FL_HIP])
print("Δ[:, 4]  -> FL_KNEE ->", FL_KNEE, dof_names[FL_KNEE])
print("Δ[:, 5]  -> FL_LAST ->", FL_LAST, dof_names[FL_LAST])
print("Δ[:, 6]  -> RR_HIP  ->", RR_HIP,  dof_names[RR_HIP])
print("Δ[:, 7]  -> RR_KNEE ->", RR_KNEE, dof_names[RR_KNEE])
print("Δ[:, 8]  -> RR_LAST ->", RR_LAST, dof_names[RR_LAST])
print("Δ[:, 9]  -> RL_HIP  ->", RL_HIP,  dof_names[RL_HIP])
print("Δ[:, 10] -> RL_KNEE ->", RL_KNEE, dof_names[RL_KNEE])
print("Δ[:, 11] -> RL_LAST ->", RL_LAST, dof_names[RL_LAST])
print("======================================\n")

num_dofs = len(dof_names)

# ==========================
# 5.1. JOINT DRIVE (PD) SETTINGS
# ==========================
# Slightly softer stiffness and more damping → smoother motion
stiffness = np.full(num_dofs, 30.0, dtype=float)
damping   = np.full(num_dofs, 15.0, dtype=float)

try:
    spider.set_dof_stiffness(stiffness)
    spider.set_dof_damping(damping)
except AttributeError:
    print("Warning: set_dof_stiffness / set_dof_damping not available on this Articulation")

# ==========================
# 6. BASE POSE AND SMOOTH TRANSITION
# ==========================
# Neutral stance for each leg: [hip, knee, last]
base_leg = np.array([0.0, 0.3, -0.15], dtype=float)
base_targets = np.zeros(num_dofs, dtype=float)

# Front Right
base_targets[FR_HIP]  = base_leg[0]
base_targets[FR_KNEE] = base_leg[1]
base_targets[FR_LAST] = base_leg[2]
# Front Left
base_targets[FL_HIP]  = base_leg[0]
base_targets[FL_KNEE] = base_leg[1]
base_targets[FL_LAST] = base_leg[2]
# Rear Right
base_targets[RR_HIP]  = base_leg[0]
base_targets[RR_KNEE] = base_leg[1]
base_targets[RR_LAST] = base_leg[2]
# Rear Left
base_targets[RL_HIP]  = base_leg[0]
base_targets[RL_KNEE] = base_leg[1]
base_targets[RL_LAST] = base_leg[2]

current_positions = spider.get_joint_positions()
if isinstance(current_positions, np.ndarray) and current_positions.ndim == 2:
    current_positions = current_positions[0]
current_positions = np.array(current_positions, dtype=float)

try:
    physics_dt = my_world.get_physics_dt()
except Exception:
    physics_dt = 1.0 / 60.0  # fallback

blend_seconds = 1.5
blend_steps = max(1, int(blend_seconds / physics_dt))

print(f"Smoothly moving into base pose over {blend_seconds:.2f} s (~{blend_steps} steps)...")

# Kinematic blend into the base pose so the robot does not "snap"
for step in range(blend_steps):
    alpha = (step + 1) / blend_steps
    blended = (1.0 - alpha) * current_positions + alpha * base_targets
    spider.set_joint_positions([blended])
    my_world.step(render=True)

hold_seconds = 1.0
hold_steps = int(hold_seconds / physics_dt)
print(f"Holding base pose for another {hold_seconds:.2f} s...")

for _ in range(hold_steps):
    spider.set_joint_position_targets([base_targets])
    my_world.step(render=True)

# ==========================
# 7. PLAYBACK WITH DRIVES (INTERPOLATED GAIT)
# ==========================
cycles = 40                      # how many gait cycles to run
current_angles = base_targets.copy()

# Duration of one keyframe in seconds
keyframe_duration = 0.25
steps_per_keyframe = max(1, int(keyframe_duration / physics_dt))

for cycle in range(cycles):
    print(f"--- Starting gait cycle: {cycle + 1}/{cycles} ---")

    for j in range(num_keyframes):
        delta = keyframe_sequence[j]

        # Logical target pose for this keyframe (before interpolation)
        targets = current_angles.copy()

        # Front Right (FR)
        targets[FR_HIP]  += delta[0]
        targets[FR_KNEE] += delta[1]
        targets[FR_LAST] += delta[2]

        # Front Left (FL)
        targets[FL_HIP]  += delta[3]
        targets[FL_KNEE] += delta[4]
        targets[FL_LAST] += delta[5]

        # Rear Right (RR) – hip axis is inverted
        targets[RR_HIP]  += -delta[6]
        targets[RR_KNEE] +=  delta[7]
        targets[RR_LAST] +=  delta[8]

        # Rear Left (RL) – hip axis is also inverted
        targets[RL_HIP]  += -delta[9]
        targets[RL_KNEE] +=  delta[10]
        targets[RL_LAST] +=  delta[11]

        # ---- Smooth interpolation from current_angles to targets ----
        start_angles = current_angles.copy()
        for s in range(steps_per_keyframe):
            alpha = (s + 1) / steps_per_keyframe  # 0..1
            blended = (1.0 - alpha) * start_angles + alpha * targets
            spider.set_joint_position_targets([blended])
            my_world.step(render=True)

        current_angles = targets

        spider_joint_positions = spider.get_joint_positions()
        print(f"Cycle {cycle + 1}, Keyframe {j}: Joint positions: {spider_joint_positions}")
        time.sleep(0.01)

simulation_app.close()
