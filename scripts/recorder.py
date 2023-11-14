#!/usr/bin/env python
"""
Waypoint Node Recorder
- CTRL+C for exiting and saving waypoint node data (csv)

"""
import numpy as np
import os
import atexit
import pandas as pd
from datetime import datetime

import roslib
import rospy
import math
import tf
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry

# Params
NODE_RESOLUTION = 0.5 # [m]

# Waypoint node csv data
now = datetime.now()
filename = 'waypoint_node_' + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + ".csv"
WPT_NODE_CSV_PATH = "~/" + filename

node_csv_data = np.array([[]])
if os.path.isfile(WPT_NODE_CSV_PATH):
    node_csv_data = pd.read_csv(WPT_NODE_CSV_PATH, sep=',', header=None)

# Waypoint node data
node_data = []

# Varialbes
node_id = 0
last_ego_pose = []

# Node
class Node:
    def __init__(self, x, y, id, score):
        self.x = x
        self.y = y
        self.id = id
        self.score = score

def calc_dist(tx, ty, ix, iy):
    return math.sqrt( (tx-ix)**2 + (ty-iy)**2 )

def save_waypoint(data):
    global node_id, node_csv_data, last_ego_pose
    quaternion = np.array([data.pose.pose.orientation.x, 
                           data.pose.pose.orientation.y, 
                           data.pose.pose.orientation.z, 
                           data.pose.pose.orientation.w])

    euler = tf.transformations.euler_from_quaternion(quaternion)

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    yaw = euler[2] # roll pitch yaw
    
    print("x: {}, y: {}, yaw: {}".format(round(x, 3), round(y, 3), round(np.rad2deg(yaw), 3)))

    # for waypoint recorder
    curr_wpt_node_data = np.array([[x, y, node_id]])

    # for waypoint node management
    node = Node(x, y, node_id, 0)
    
    # init last pose
    if len(last_ego_pose) == 0:
        last_ego_pose = [x, y] # update data

    if node_csv_data.shape[1] == 0:
        # if csv data is empty
        node_csv_data = np.append(node_csv_data, curr_wpt_node_data, axis=1) # for csv
        node_data.append(node) # for node

        last_ego_pose = [x, y] # update data
        node_id += 1
    else:
        # if csv data is not empty,
        dist_driven = calc_dist(last_ego_pose[0], last_ego_pose[1], x, y)
        print("dist_driven :", dist_driven)
        # Append wpt data whenever agent has driven NODE_RESOLUTION from before
        if dist_driven > NODE_RESOLUTION:
            node_csv_data = np.append(node_csv_data, curr_wpt_node_data, axis=0) # for csv
            node_data.append(node) # for node
            # update data
            last_ego_pose = [x, y]
            node_id += 1

def main():
    # ROS init
    rospy.init_node('node_recorder')
    listener = tf.TransformListener()
    rospy.Subscriber('odom', Odometry, save_waypoint)
    rospy.spin()

def shutdown():
    # Save as csv
    dataframe = pd.DataFrame(node_csv_data)
    dataframe.to_csv(WPT_NODE_CSV_PATH, header=False, index=False)
    print('Goodbye')

if __name__ == '__main__':
    atexit.register(shutdown)
    print('Saving waypoints...')
    try:
        main()
    except rospy.ROSInterruptException:
        pass
