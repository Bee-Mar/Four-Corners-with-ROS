#!/usr/bin/env python

import sys
import rospy
from geometry_msgs.msg import *
from math import *
from nav_msgs.msg import *
from nav_msgs.srv import *
from std_srvs.srv import *


'''
Name: Brandon Marlowe
Class: CIS 693
Project: 3
Date: 2/14/18
ID: 2693414
---------------------
Sends control signals to Turtlebot to navigate to four corners of engineering lab.
'''

# global variables for pose information
pose_x = 0.0
pose_y = 0.9
pose_theta = 0.0
pose_orient = 0.0
header_frame_id = ''


def odom_callback(info):
    global pose_x, pose_y, pose_theta, pose_orient, header_frame_id
    header_frame_id = info.header.frame_id
    pose_x = info.pose.pose.position.x
    pose_y = info.pose.pose.position.y
    pose_theta = info.pose.pose.position.z
    pose_orient = info.pose.pose.orientation.w


# calculates the Euclidean distance of the turtlebot from the goal destination
def dist_from_goal(goal_x, goal_y):
    return sqrt(pow((goal_x - pose_x), 2) + pow((goal_y - pose_y), 2))


# sends control signal to turtlebot
def go_to_goal(x_goal, y_goal, w_goal, seq):

    # mbs_pub is short for move_base_simple_publisher
    mbs_pub = rospy.Publisher('/move_base_simple/goal',
                              PoseStamped, queue_size=15)
    rospy.sleep(1.0)

    for index in range(len(test_goal_poses)):

        go_to_goal(test_goal_poses[index][0], test_goal_poses[index]
                   [1], test_goal_poses[index][2], index)

        while True:
            # ps_goal is short for PoseStamped_goal
    ps_goal = PoseStamped()

    # placing goal destination in PoseStamped publisher
    ps_goal.header.frame_id = 'map'
    ps_goal.header.seq = seq
    ps_goal.header.stamp = rospy.Time.now()
    ps_goal.pose.position.x = x_goal
    ps_goal.pose.position.y = y_goal
    ps_goal.pose.position.z = 0.0
    ps_goal.pose.orientation.x = 0.0
    ps_goal.pose.orientation.y = 0.0
    ps_goal.pose.orientation.w = w_goal

    mbs_pub.publish(ps_goal)
    rospy.sleep(1.0)


def visit_corners():

    # coordinates for the back left, back right, top left, and top right corners
    goal_coord = [[-2.48, 5.03, 1.05], [1.07, 4.81, -0.751],
                  [-2.19, 1.02, 0.681], [2.53, -0.81, 0.014]]

    # looping through coordinates and publishing each as a new goal destination
    for index in range(len(goal_coord)):

        # (x, y, orientation) -- the index is used as the sequence number
        go_to_goal(goal_coord[index][0], goal_coord[index]
                   [1], goal_coord[index][2], index)

        while True:

            # constantly retrieving current locale and calculating Euclidean distance from goal
            rospy.Subscriber('/odom', Odometry, odom_callback)

            rospy.sleep(0.1)

            if dist_from_goal(goal_coord[index][0], goal_coord[index][1]) < 1.0:
                rospy.sleep(10)
                break


def main():

    while not rospy.is_shutdown():
        visit_corners()
        sys.exit(0)


if __name__ == "__main__":

    try:
        # initializes node
        rospy.init_node('four_corners_node', anonymous=False)

        # run main method
        main()

    except rospy.ROSInterruptException or rospy.ROSException:
        pass
