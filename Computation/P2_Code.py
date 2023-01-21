## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.
import random
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)

## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)
## This Code shows peices of the final code as well so please be wary before reviewing code design

#Replace blank coordinates with autoclave specific coordinates
autoclaves = [1,2,3,4,5,6]
home = [0.4064, 0.0, 0.4826]
pickup = [0.5, 0.0, 0.007]
small_red_cage = [-0.6044,  0.2503, 0.426]
small_green_cage = [0.01,-0.672,0.426]
small_blue_cage = [0.015, 0.6526,0.426]
large_red_cage = [-0.3633, 0.1468, 0.482]
large_green_cage = [0.0, -0.3964, 0.482]
large_blue_cage = [0.0,0.4064,0.482]
random_autoclaves = random.shuffle(autoclaves)##Bonus marks were awarded for randomly generated autoclaves
thres = 0.5

def scanner(container):
    print("Scanner Activated")
    if container == 1: 
        dropoff_position = small_red_cage
    elif container == 2 :
        dropoff_position = small_green_cage 
    elif container == 3 :
        dropoff_position = small_blue_cage
    elif container == 4 :
        dropoff_position = large_red_cage
    elif container == 5 :
        dropoff_position = large_green_cage
    elif container == 6 :
        dropoff_position = large_blue_cage
    return dropoff_position


def move_end_effector(location):#Functions moves to any location
    ##print("Moving arm")
    arm.move_arm(location[0],location[1],location[2])
    time.sleep(2)
    ##print("Moved arm")
    return

"""
def gripper(control):
    if control == "open":
        ##print("Opened Gripper")
        arm.control_gripper(-45)
        time.sleep(2)
        return
    if control == "close":
        ##print("Closed Gripper")
        arm.control_gripper(45)
        time.sleep(2)
        return
"""

   
def control_autoclave_drawer(num):

    if num == 4 and autoclave_state == False:
        arm.open_red_autoclave(True)
        autoclave_state == True
        time.sleep(2)
        return

    elif num == 5 and autoclave_state == False:
        arm.open_green_autoclave(True)
        autoclave_state == True
        time.sleep(2)
        return

    elif num == 6 and autoclave_state == False:
        arm.open_blue_autoclave(True)
        autoclave_state == True
        time.sleep(2)
        return

    return

def control_autoclave_drawer_close(num):

    if num == 4:
        arm.open_red_autoclave(False)
        autoclave_state == False
        time.sleep(2)
        return

    elif num == 5:
        arm.open_green_autoclave(False)
        autoclave_state == False
        time.sleep(2)
        return

    elif num == 6:
        arm.open_blue_autoclave(False)
        autoclave_state == False
        time.sleep(2)
        return
    return



for i in autoclaves:

    check = False
    autoclave_state = False
    gripper_state = True

    arm.spawn_cage(i)

    time.sleep(2)
    
    move_end_effector(pickup)

    dropoff = scanner(i)

    print(i)

    while check == False:

        time.sleep(0.25)
        
        if arm.emg_left() > thres and arm.emg_right() == 0:

            arm.control_gripper(45)
            time.sleep(2)
            move_end_effector(home)

        elif arm.emg_left() > thres and arm.emg_right() > thres:

            move_end_effector(dropoff)

            time.sleep(2)

            control_autoclave_drawer(i)

            time.sleep(1)

            arm.control_gripper(-45)

            time.sleep(2)

        elif arm.emg_left() == 0 and arm.emg_right() > thres:

            control_autoclave_drawer_close(i)











