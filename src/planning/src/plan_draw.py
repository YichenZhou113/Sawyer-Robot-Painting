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
	# plandraw.gripper_close()
	# rospy.sleep(10)
	# plandraw.grip?per_op
	plandraw.start_position()

	## BOX
	box_size = np.array([2.4,2.4,0.1])
	box_pose = PoseStamped()
	box_pose.header.stamp = rospy.Time.now()
	box_pose.header.frame_id = "base"
	box_pose.pose.position.x = 0
	box_pose.pose.position.y = 0
	box_pose.pose.position.z = -0.4
	box_pose.pose.orientation.x = 0.00
	box_pose.pose.orientation.y = 0.00
	box_pose.pose.orientation.z = 0.00
	box_pose.pose.orientation.w = 1.00
	plandraw.add_box_obstacle(box_size,"box1",box_pose)

	box_size2 = np.array([2.4,2.4,0.1])
	box_pose2 = PoseStamped()
	box_pose2.header.stamp = rospy.Time.now()
	box_pose2.header.frame_id = "base"
	box_pose2.pose.position.x = 0
	box_pose2.pose.position.y = 0
	box_pose2.pose.position.z = 1
	box_pose2.pose.orientation.x = 0.00
	box_pose2.pose.orientation.y = 0.00
	box_pose2.pose.orientation.z = 0.00
	box_pose2.pose.orientation.w = 1.00
	plandraw.add_box_obstacle(box_size2,"box2",box_pose2)


	orien_const = OrientationConstraint()
	orien_const.link_name = "right_gripper_tip";
	orien_const.header.frame_id = "base";
	orien_const.orientation.y = -1.0;
	orien_const.absolute_x_axis_tolerance = 0.1;
	orien_const.absolute_y_axis_tolerance = 0.1;
	orien_const.absolute_z_axis_tolerance = 0.1;
	orien_const.weight = 1.0;

	def set_use_pen(pen_id, goal_1):
		if pen_id == 0: # Blue The innar one
			goal_1.pose.orientation.x = 0.0
			goal_1.pose.orientation.y = -0.9848078
			goal_1.pose.orientation.z = 0.0
			goal_1.pose.orientation.w = -0.1736482

			goal_1.pose.position.x -= 0.003
			goal_1.pose.position.y -= 0.013
			goal_1.pose.position.z -= 0.011


		if pen_id == 1:
			goal_1.pose.orientation.x = 0.0
			goal_1.pose.orientation.y = -1.0
			goal_1.pose.orientation.z = 0.0
			goal_1.pose.orientation.w = 0.0

			goal_1.pose.position.x -= 0.014
			goal_1.pose.position.y -= 0.002
			goal_1.pose.position.z -= 0.017

		if pen_id == 2:
			goal_1.pose.orientation.x = 0.0
			goal_1.pose.orientation.y = -0.9848078
			goal_1.pose.orientation.z = 0.0
			goal_1.pose.orientation.w = 0.1736482

			goal_1.pose.position.x -= 0.028
			goal_1.pose.position.y -= 0.003
			goal_1.pose.position.z -= 0.010

		# if pen_id == 0:
		# 	goal_1.pose.orientation.x = 0.0
		# 	goal_1.pose.orientation.y = -0.925877
		# 	goal_1.pose.orientation.z = 0.0
		# 	goal_1.pose.orientation.w = -0.360095
		# if pen_id == 1:
		# 	goal_1.pose.orientation.x = 0.0
		# 	goal_1.pose.orientation.y = -0.9994
		# 	goal_1.pose.orientation.z = 0.0
		# 	goal_1.pose.orientation.w = 0.005035
		# if pen_id == 2:
		# 	goal_1.pose.orientation.x = 0.0
		# 	goal_1.pose.orientation.y = -0.974507
		# 	goal_1.pose.orientation.z = 0.0
		# 	goal_1.pose.orientation.w = 0.222739
		


	waypoints = []
	while not rospy.is_shutdown():
		#raw_input("~~~~~~~~~~~~!!!!!!!!!!!!")
		while not rospy.is_shutdown():
			try:
				while len(queue):
					# print(len(queue))
					cur = queue.popleft()
					x,y,z = cur.position_x, cur.position_y, cur.position_z
					x += 0.002  # ada different coordinate
					z -= 0.103
					z += 0.037
					# z += 0.2
					x -= 0.013
					y += 0.010

					z += 0.005

					x += 0.12
					if cur.status_type != "edge_grad":
						# ti bi !!!!! luo bi !!!!
						if cur.status_type == "starting":
							print("start")
							# waypoints = []

							goal_1 = PoseStamped()
							goal_1.header.frame_id = "base"

							#x, y, and z position
							goal_1.pose.position.x = x
							goal_1.pose.position.y = y
							goal_1.pose.position.z = z + 0.12

							#Orientation as a quaternion
							# [0.766, -0.623, 0.139, -0.082]
							# [-0.077408, 0.99027, -0.024714, ]

							set_use_pen(cur.pen_type, goal_1)

							
							waypoints.append(copy.deepcopy(goal_1.pose))

							goal_1.pose.position.z -= 0.12

							waypoints.append(copy.deepcopy(goal_1.pose))

							# plan = plandraw.plan_to_pose(goal_1, [orien_const], waypoints)

							# if not plandraw.execute_plan(plan):
							# 	raise Exception("Starting execution failed")
							# else:
							# queue.pop(0)

						elif cur.status_type == "next_point":
							# print("next")
							goal_1 = PoseStamped()
							goal_1.header.frame_id = "base"

							#x, y, and z position
							goal_1.pose.position.x = x
							goal_1.pose.position.y = y
							goal_1.pose.position.z = z

		
							#Orientation as a quaternion

							# goal_1.pose.orientation.x = 0.459962
							# goal_1.pose.orientation.y = -0.7666033
							# goal_1.pose.orientation.z = 0.0
							# goal_1.pose.orientation.w = -0.4480562

							set_use_pen(cur.pen_type, goal_1)

							# waypoints = []
							waypoints.append(copy.deepcopy(goal_1.pose))

							# plan = plandraw.plan_to_pose(goal_1, [orien_const], waypoints)

							# if not plandraw.execute_plan(plan):
							# 	raise Exception("Execution failed, point is ", cur)
							# else:
							# queue.pop(0)
						elif cur.status_type == "ending":
							print("ppppppp      ",cur)
							# mmm = plandraw.get_cur_pos().pose
							
							goal_1 = PoseStamped()
							goal_1.header.frame_id = "base"

							#x, y, and z position
							goal_1.pose.position.x = x
							goal_1.pose.position.y = y
							goal_1.pose.position.z = z + 0.12

		
							#Orientation as a quaternion
							set_use_pen(1, goal_1)

							# waypoints = []
							waypoints.append(copy.deepcopy(goal_1.pose))
							plan = plandraw.plan_to_pose(goal_1, [], waypoints)
							waypoints = []
							# queue.pop(0)

							if not plandraw.execute_plan(plan):
								raise Exception("Execution failed")
							print("ti bi")
							# rospy.sleep(5)
				#raw_input("Press <Enter> to move next!!!")
			except Exception as e:
				print e
			else:
				#print("lllllllllllllllllllll")
				break



if __name__ == '__main__':
	rospy.init_node('moveit_node')
	rospy.Subscriber("position_messages", ChouChou, get_points, queue_size=10000)
	
	main()
	rospy.spin()
