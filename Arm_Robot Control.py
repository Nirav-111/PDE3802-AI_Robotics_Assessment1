"""
DOFBOT Arm Control Robot - it will perform a grab_from_pick_and_place function (target_pose, label)
integrated with an AI vision 

Classes:
    apple, banana, orange, lemon, pomegranate, tomato
"""

import time
from Arm_Lib import Arm_Device

# INITIALISE DOFBOT

Arm = Arm_Device()
time.sleep(0.3)
print("[DOFBOT] Arm initialised.")

# ARM MOVEMENT 

def arm_clamp_block(enable: int):
    """Open (0) or close (1) the gripper."""
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 135, 400)
    time.sleep(0.4)


def arm_move(poses, t=700):
    """Moves servos 1–5 to the given positions."""
    for i in range(5):
        servo = i + 1
        angle = poses[i]
        move_time = int(t * 1.2) if servo == 5 else t
        Arm.Arm_serial_servo_write(servo, angle, move_time)
        time.sleep(0.01)

    time.sleep(t / 1000.0)


def arm_move_up():
    """Lift the arm to a safe height."""
    Arm.Arm_serial_servo_write(2, 90, 1500)
    Arm.Arm_serial_servo_write(3, 90, 1500)
    Arm.Arm_serial_servo_write(4, 90, 1500)
    time.sleep(0.3)

# ARM POSITION PRESETS

p_home = [90, 130, 0, 0, 90]
p_pick_top = [90, 80, 50, 50, 270]
p_pick = [90, 53, 33, 36, 270]

# Basket positions
p_basket_yellow = [65, 22, 64, 56, 270]
p_basket_red    = [117, 19, 66, 56, 270]
p_basket_green  = [136, 66, 20, 29, 270]
p_basket_blue   = [44, 66, 20, 28, 270]


# FRUIT → BASKET MAPPING

FRUIT_TO_BASKET = {
    "apple":        p_basket_green,
    "banana":       p_basket_yellow,
    "orange":       p_basket_red,
    "lemon":        p_basket_blue,
    "pomegranate":  p_basket_red,
    "tomato":       p_basket_green,
}

# MAIN PICK-AND-PLACE FUNCTION

def grab_from_pick_and_place(target_pose, label=""):
    """Complete pick + lift + move + drop sequence."""
    
    print(f"[DOFBOT] Sorting fruit: {label}")

    # Home
    arm_clamp_block(0)
    arm_move(p_home, 1000)

    # Approach pickup
    arm_move(p_pick_top, 1000)
    arm_move(p_pick, 1000)

    # Grab
    arm_clamp_block(1)

    # Lift
    arm_move(p_pick_top, 1000)

    # Move to basket
    arm_move(target_pose, 1100)

    # Drop
    arm_clamp_block(0)

    # Back home
    arm_move_up()
    arm_move(p_home, 1100)

    print("[DOFBOT] Sorting completed.")
