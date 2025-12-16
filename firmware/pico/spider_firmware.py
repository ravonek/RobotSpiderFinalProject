"""
Spider Robot (4-leg) — MicroPython firmware for 12 servos.

- PWM @ 50 Hz
- Per-joint neutral offsets and direction mapping
- Simple trot gait demo cycle

Target: Raspberry Pi Pico / compatible MicroPython board.
"""

import time
from machine import Pin, PWM

# === CONSTANTS ===
NUM_SERVOS = 12
FREQ = 50
PINS = list(range(12))

# --- Neutral offsets (deg) per servo ---
NEUTRAL_OFFSETS = [
    90, 90, 90,   # BL
    90, 90, 90,   # BR
    90, 90, 90,   # FL
    90, 90, 90,   # FR
]

# --- Direction map (+1 or -1 per joint) ---
DIRECTION_MAP = [
    -1, 1, 1,      # BL
    1,  1, 1,      # BR
    -1, 1, 1,      # FL
    1,  1, 1,      # FR
]

def degrees_to_duty(angle_deg):
    angle_deg = max(0, min(180, angle_deg))
    return int((angle_deg / 180.0) * 8000 + 1000)

class Servo:
    def __init__(self, pin_num, offset, direction):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(FREQ)
        self.offset = offset
        self.direction = direction
        self.current_angle = 0
        self.set_angle(0)

    def set_angle(self, angle):
        real_angle = self.offset + angle * self.direction
        self.current_angle = angle
        self.pwm.duty_u16(degrees_to_duty(real_angle))

class Robot12:
    def __init__(self):
        self.servos = []
        for i in range(NUM_SERVOS):
            self.servos.append(Servo(PINS[i], NEUTRAL_OFFSETS[i], DIRECTION_MAP[i]))

    def move_all(self, angles, duration=1.0, steps=50):
        if len(angles) != NUM_SERVOS:
            raise ValueError("angles must have length 12")

        start_angles = [s.current_angle for s in self.servos]

        for step in range(1, steps + 1):
            alpha = step / steps
            for i, servo in enumerate(self.servos):
                target = angles[i]
                interp = start_angles[i] + (target - start_angles[i]) * alpha
                servo.set_angle(interp)
            time.sleep(duration / steps)

    def init_position(self):
        self.move_all([0] * NUM_SERVOS, duration=1.0, steps=50)

    def stand_up(self):
        BACK_HIP_ANGLE  = -20
        FRONT_HIP_ANGLE = 5
        FEMUR_ANGLE = 55
        TIBIA_ANGLE = -15

        stand_angles = [
            BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE,   # BL
            BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE,   # BR
            FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE,   # FL
            FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE,   # FR
        ]
        self.move_all(stand_angles, duration=1.5, steps=60)

    def trot_cycle(self):
        """
        FULL cycle (как ты сказал):
        1) ПП (FR) вперед
        2) ЗЛ (BL) вперед
        3) Подтягивание (вперед)
        4) ПЛ (FL) вперед
        5) ЗП (BR) вперед
        6) Подтягивание (вперед)
        """

        PHASE_DURATION = 0.4
        PHASE_STEPS    = 35
        PHASE_PAUSE    = 0.5  # пауза между КРУПНЫМИ шагами

        # === BASE STANCE ===
        BACK_HIP_ANGLE  = -20
        FRONT_HIP_ANGLE = 5
        FEMUR_ANGLE     = 55
        TIBIA_ANGLE     = -15

        # текущие состояния
        BL_H, BL_F, BL_T = BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE
        BR_H, BR_F, BR_T = BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE
        FL_H, FL_F, FL_T = FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE
        FR_H, FR_F, FR_T = FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE

        def state():
            return [
                BL_H, BL_F, BL_T,
                BR_H, BR_F, BR_T,
                FL_H, FL_F, FL_T,
                FR_H, FR_F, FR_T,
            ]

        def move_and_pause():
            self.move_all(state(), duration=PHASE_DURATION, steps=PHASE_STEPS)
            time.sleep(PHASE_PAUSE)

        # -------- Step function (lift -> down) --------
        def step_FR():
            nonlocal FR_H, FR_F, FR_T
            # lift + forward
            FR_H = FRONT_HIP_ANGLE + 25
            FR_F = FEMUR_ANGLE - 18
            FR_T = TIBIA_ANGLE + 18
            move_and_pause()
            # down
            FR_F = FEMUR_ANGLE
            FR_T = TIBIA_ANGLE - 3
            move_and_pause()

        def step_BL():
            nonlocal BL_H, BL_F, BL_T
            BL_H = BACK_HIP_ANGLE + 15
            BL_F = FEMUR_ANGLE - 18
            BL_T = TIBIA_ANGLE + 18
            move_and_pause()
            BL_F = FEMUR_ANGLE
            BL_T = TIBIA_ANGLE - 2
            move_and_pause()

        def step_FL():
            nonlocal FL_H, FL_F, FL_T
            FL_H = FRONT_HIP_ANGLE + 25
            FL_F = FEMUR_ANGLE - 18
            FL_T = TIBIA_ANGLE + 18
            move_and_pause()
            FL_F = FEMUR_ANGLE
            FL_T = TIBIA_ANGLE - 3
            move_and_pause()

        def step_BR():
            nonlocal BR_H, BR_F, BR_T
            BR_H = BACK_HIP_ANGLE + 15
            BR_F = FEMUR_ANGLE - 18
            BR_T = TIBIA_ANGLE + 18
            move_and_pause()
            BR_F = FEMUR_ANGLE
            BR_T = TIBIA_ANGLE - 2
            move_and_pause()

        def pull_forward():
            nonlocal BL_H, BR_H, FL_H, FR_H
            HIP_SHIFT = 1.0  # подтягивание ВПЕРЁД
            BL_H += HIP_SHIFT
            BR_H += HIP_SHIFT
            FL_H += HIP_SHIFT
            FR_H += HIP_SHIFT
            move_and_pause()

        # ====== ТВОЙ ПОРЯДОК ЦИКЛА ======
        step_FR()        # ПП
        step_BL()        # ЗЛ
        pull_forward()   # подтягивание

        step_FL()        # ПЛ
        step_BR()        # ЗП
        pull_forward()   # подтягивание

        # (опционально) вернуть в базовую стойку, чтобы цикл не "уползал"
        stand_angles = [
            BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE,   # BL
            BACK_HIP_ANGLE,  FEMUR_ANGLE, TIBIA_ANGLE,   # BR
            FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE,   # FL
            FRONT_HIP_ANGLE, FEMUR_ANGLE, TIBIA_ANGLE,   # FR
        ]
        self.move_all(stand_angles, duration=0.6, steps=40)
        time.sleep(PHASE_PAUSE)

# === Main program ===
robot = Robot12()

print("Init (neutral) position...")
robot.init_position()
time.sleep(1.0)

print("Standing up...")
robot.stand_up()
time.sleep(1.0)

print("Gait...")
for i in range(5):
    robot.trot_cycle()
    time.sleep(0.2)

print("Back to neutral...")
robot.init_position()
