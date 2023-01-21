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
#Global Variables of Autoclave bin locations, Home locations, Pickup Locations, Assigning autoclave values as well as randomizing their order, and Threshold.
home = (0.4064, 0.0, 0.4826)
pickup = (0.517, 0.0, 0.031)
small_red_cage = (-0.613,  0.245, 0.385)
small_green_cage = (0,-0.6666,0.39)
small_blue_cage = (0.0, 0.6666,0.385)
large_red_cage = (-0.39, 0.14, 0.29)
large_green_cage = (0.0, -0.41, 0.29)
large_blue_cage = (0.0,0.41,0.29)
autoclaves = [1,2,3,4,5,6]
random_autoclaves = random.shuffle(autoclaves)
thres = 0.6

#Yuvraj Sandhu
def move_end_effector(location):#Functions moves to any location
    if arm.emg_left() == 1.00 and arm.emg_right() == 1.00:
        print("Moving arm")
        arm.move_arm(location[0],location[1],location[2])
        time.sleep(2)
        print("Moved arm")
    return

def scanner(container): #Scanner function attaches a cage to the dropoff position that matches the autoclave.
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

def gripper(control):#When the muscle sensor is in the right position AND the gripper has an open state then the gripper will open,
                    #If the gripper is in the close state then it will close the gripper and set the "control" variable to closed
    if arm.emg_left() > thres and arm.emg_right() == 0: #Checks the muscle sensor reading and only runs if the conditons are met
        if control == "open":
            print("Opened Gripper")
            arm.control_gripper(-45)
            control = "open"
            return control
        elif control == "close":
            print("Closed Gripper")
            arm.control_gripper(45)
            control = "close"
            return control

def control_autoclave_drawer(num,autoclave_state):#Autoclave drawers will open only for the large autoclaves if the criteria is met.Then sets the state of the autoclave to true so it won't be called again.
    if arm.emg_left() == 0 and arm.emg_right() > thres:

        if num == 4 and autoclave_state == True:
            arm.open_red_autoclave(False)
            autoclave_state = False
            return autoclave_state

        elif num == 4:
            arm.open_red_autoclave(True)
            autoclave_state = True
            return autoclave_state

        elif num == 5 and autoclave_state == True:
            arm.open_green_autoclave(False)
            autoclave_state = False
            return autoclave_state

        elif num == 5:
            arm.open_green_autoclave(True)
            autoclave_state = True
            return autoclave_state
        
        elif num == 6 and autoclave_state == True:
            arm.open_blue_autoclave(False)
            autoclave_state = False
            return autoclave_state
        
        elif num == 6:
            arm.open_blue_autoclave(True)
            autoclave_state = True
            return autoclave_state
    
    

#Eric Hitsman
for i in autoclaves:
#The variable i is utilized so since we're not looking for a value but for when i isn't a value anymore I.E when there aren't anymore autoclaves in the list, this for loop will break
    arm.spawn_cage(i) #Will spawn a random arrangement of autoclaves

    #Intially setting variables to their preferred states so that it can be changed accordingly in the code
    x = True
    check = False
    autoclave_state = False
    gripper_state = True
    dropoff = scanner(i)
    time.sleep(2)
    control = "open"

    while x == True: #While loops setup a straight-forward path for the arm to follow for each autoclave. This while loop checks if the arm at pickup.
        if arm.effector_position() == pickup:
            break
        else:
            move_end_effector(pickup)

    while x == True: #While loop sets the gripper to close itself when at the pickup location
        if control == "close":
            break
        else:
            control = gripper("close")

    while x == True: #While loop will move to the dropoff location and if it is not there then it will move to the drop off location and open the door (if the autoclave is large)
        if arm.effector_position() == dropoff:
            break
        else:
            time.sleep(1.5)
            move_end_effector(home)
            time.sleep(1.5)
            move_end_effector(dropoff)

    if i == 4 or i == 5 or i == 6: #While loop opens the door in the scenerio when a large autoclave is being dropped-off
        while x == True:
            if autoclave_state == True:
                break
            else:
                autoclave_state = control_autoclave_drawer(i,autoclave_state)

    while x == True: #While loop will drop the autoclave into the opened drawer
        if control == "open":
            break
        else:
            control = gripper("open")

    if i == 4 or i == 5 or i == 6: #While loop closes the door in the scenerio when a large autoclave is being dropped-off
        while x == True:
            if autoclave_state == False:
                break
            else:
                autoclave_state = control_autoclave_drawer(i,autoclave_state)

    while x == True: #Returns home to restart the loop for another autoclave
        if arm.effector_position() == home:
            break
        else:
            move_end_effector(home)
