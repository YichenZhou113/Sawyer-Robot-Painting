#!/usr/bin/env python
import sys
import rospy
import numpy as np
import traceback
import time
import copy

from moveit_msgs.msg import OrientationConstraint
from geometry_msgs.msg import PoseStamped

from path_planner import PathPlanner
from controller import Controller
from intera_interface import Limb

from planning.msg import ChouChou
from collections import deque
queue = deque()
prev_msg = ""
sec_pre = ""

def get_points(message):
	"""
	We will add the point we received to queue
	"""
	global prev_msg
	global sec_pre
	
	#print("9999",message.status_type)
	if prev_msg != message and message.status_type != "dummy":
		queue.append(message)
		if message.status_type == "ending":
			sec_pre = prev_msg
		prev_msg = message
		

def main():
	global prev_msg
	global sec_pre

	plandraw = PathPlanner('right_arm')
	plandraw.gripper_open()
	plandraw.gripper_close()
	# plandraw.gripper_open()
	rospy.sleep(10)



if __name__ == '__main__':
	rospy.init_node('moveit_node')
	
	main()
	rospy.spin()
