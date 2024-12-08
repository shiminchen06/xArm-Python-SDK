#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move Circle with real-time joint data transmission via OSC
"""

import os
import sys
import time
from pythonosc import udp_client
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)

# OSC server details
OSC_IP = "192.168.1.155"  # Replace with the actual IP of the OSC server
OSC_PORT = 8000       # Replace with the actual port the OSC server is listening on

# Initialize OSC client
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

def send_joint_data_via_osc(joint_angles):
    """Send joint angles data via OSC"""
    osc_client.send_message("/xarm/joints", joint_angles)
    print(f"Sent joint angles via OSC: {joint_angles}")

def stream_joint_data(arm):
    """Continuously stream joint data in real-time"""
    while True:
        joint_data = arm.get_servo_angle()
        if joint_data and joint_data['code'] == 0:
            joint_angles = joint_data['data']  # Extract joint angles
            send_joint_data_via_osc(joint_angles)
        time.sleep(0.1)  # Adjust the interval as needed

########################################################

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# Start streaming joint data in a separate thread
joint_stream_thread = Thread(target=stream_joint_data, args=(arm,))
joint_stream_thread.daemon = True  # Make sure this thread exits when the program ends
joint_stream_thread.start()

# Move the arm
arm.move_gohome(wait=True)

poses = [
    [300,  0,   100, -180, 0, 0],
    [300,  100, 100, -180, 0, 0],
    [400,  100, 100, -180, 0, 0],
    [400, -100, 100, -180, 0, 0],
    [300,  0,   300, -180, 0, 0]
]

# Move to first position
ret = arm.set_position(*poses[0], speed=50, mvacc=100, wait=False)
print('set_position, ret: {}'.format(ret))

# Move in a circle
ret = arm.move_circle(pose1=poses[1], pose2=poses[2], percent=50, speed=200, mvacc=1000, wait=True)
print('move_circle, ret: {}'.format(ret))

# Another circle movement
ret = arm.move_circle(pose1=poses[3], pose2=poses[4], percent=200, speed=200, mvacc=1000, wait=True)
print('move_circle, ret: {}'.format(ret))

# Return to home position
arm.move_gohome(wait=True)

# Disconnect the arm
arm.disconnect()
