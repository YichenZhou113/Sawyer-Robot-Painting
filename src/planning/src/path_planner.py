#!/usr/bin/env python
"""
Path Planner Class for Lab 7
Author: Valmik Prabhu
"""

import sys
import rospy
import moveit_commander
from moveit_msgs.msg import OrientationConstraint, Constraints, CollisionObject
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive
from intera_interface import Limb
from intera_interface import gripper as robot_gripper

class PathPlanner(object):
	"""
	Path Planning Functionality for Baxter/Sawyer

	We make this a class rather than a script because it bundles up 
	all the code relating to planning in a nice way thus, we can
	easily use the code in different places. This is a staple of
	good object-oriented programming

	Fields:
	_robot: moveit_commander.RobotCommander; for interfacing with the robot
	_scene: moveit_commander.PlanningSceneInterface; the planning scene stores a representation of the environment
	_group: moveit_commander.MoveGroupCommander; the move group is moveit's primary planning class
	_planning_scene_publisher: ros publisher; publishes to the planning scene


	"""
	def __init__(self, group_name):
		"""
		Constructor.

		Inputs:
		group_name: the name of the move_group.
			For Baxter, this would be 'left_arm' or 'right_arm'
			For Sawyer, this would be 'right_arm'
		"""

		# If the node is shutdown, call this function    
		rospy.on_shutdown(self.shutdown)

		# Initialize moveit_commander
		moveit_commander.roscpp_initialize(sys.argv)

		# Initialize the robot
		self._robot = moveit_commander.RobotCommander()

		# Initialize the planning scene
		self._scene = moveit_commander.PlanningSceneInterface()

		# This publishes updates to the planning scene
		self._planning_scene_publisher = rospy.Publisher('/collision_object', CollisionObject, queue_size=10)

		# Instantiate a move group
		self._group = moveit_commander.MoveGroupCommander(group_name)

		# Set the maximum time MoveIt will try to plan before giving up
		self._group.set_planning_time(5)

		# Set the bounds of the workspace
		self._group.set_workspace([-2, -2, -2, 2, 2, 2])

		# Sleep for a bit to ensure that all inititialization has finished
		rospy.sleep(0.5)

	def shutdown(self):
		"""
		Code to run on shutdown. This is good practice for safety

		Currently deletes the object's MoveGroup, so that further commands will do nothing
		"""
		self._group = None
		rospy.loginfo("Stopping Path Planner")

	def get_cur_pos(self):
		return self._group.get_current_pose()

	def plan_to_pose(self, target, orientation_constraints,waypoints):
		"""
		Generates a plan given an end effector pose subject to orientation constraints

		Inputs:
		target: A geometry_msgs/PoseStamped message containing the end effector pose goal
		orientation_constraints: A list of moveit_msgs/OrientationConstraint messages

		Outputs:
		path: A moveit_msgs/RobotTrajectory path
		"""

		# self._group.set_pose_target(target)
		# self._group.set_start_state_to_current_state()

		# constraints = Constraints()
		# constraints.orientation_constraints = orientation_constraints
		# self._group.set_path_constraints(constraints)

		# plan = self._group.plan()
		plan, fraction = self._group.compute_cartesian_path(waypoints,0.01,0.0)
		return plan

	def execute_plan(self, plan):
		"""
		Uses the robot's built-in controllers to execute a plan

		Inputs:
		plan: a moveit_msgs/RobotTrajectory plan
		"""
		# print("llllllllllll", plan)
		return self._group.execute(plan, True)


	def add_box_obstacle(self, size, name, pose):
		"""
		Adds a rectangular prism obstacle to the planning scene

		Inputs:
		size: 3x' ndarray; (x, y, z) size of the box (in the box's body frame)
		name: unique name of the obstacle (used for adding and removing)
		pose: geometry_msgs/PoseStamped object for the CoM of the box in relation to some frame
		"""    

		# Create a CollisionObject, which will be added to the planning scene
		co = CollisionObject()
		co.operation = CollisionObject.ADD
		co.id = name
		co.header = pose.header

		# Create a box primitive, which will be inside the CollisionObject
		box = SolidPrimitive()
		box.type = SolidPrimitive.BOX
		box.dimensions = size

		# Fill the collision object with primitive(s)
		co.primitives = [box]
		co.primitive_poses = [pose.pose]

		# Publish the object
		self._planning_scene_publisher.publish(co)

	def remove_obstacle(self, name):
		"""
		Removes an obstacle from the planning scene

		Inputs:
		name: unique name of the obstacle
		"""

		co = CollisionObject()
		co.operation = CollisionObject.REMOVE
		co.id = name

		self._planning_scene_publisher.publish(co)

	def start_position(self):
		"""
		Start the Sawyer to the initial position
		"""
		joint_command = {}
		right = Limb('right')
		joint_command['right_j0'] = -0.20
		joint_command['right_j1'] = -0.58
		joint_command['right_j2'] = 0.13
		joint_command['right_j3'] = 1.36
		joint_command['right_j4'] = -0.2
		joint_command['right_j5'] = 2.24
		joint_command['right_j6'] = 1.80

		# joint_command['right_j0'] = -0.11
		# joint_command['right_j1'] = 0.58
		# joint_command['right_j2'] = -1.83
		# joint_command['right_j3'] = 1.50
		# joint_command['right_j4'] = 1.64
		# joint_command['right_j5'] = 2.94
		# joint_command['right_j6'] = -3.18

		# joint_command['right_j0'] = -0.013
		# joint_command['right_j1'] = 0.88
		# joint_command['right_j2'] = -0.045
		# joint_command['right_j3'] = -2.60
		# joint_command['right_j4'] = -2.98
		# joint_command['right_j5'] = -2.98
		# joint_command['right_j6'] = -4.64

		try:
			print("Initializing starting position....")
			right.move_to_joint_positions(joint_command)
		except Exception as e:
			print(e)

	def gripper_open(self):
		"""
		Open the gripper
		"""
		
		print('Opening...')
		right_gripper = robot_gripper.Gripper('right')
		right_gripper.calibrate()	
		rospy.sleep(5)
		right_gripper.close()	
		rospy.sleep(5)
		right_gripper.open()


	def gripper_close(self):
		"""S
		Close the gripper
		"""
		
		print('Closing...')
		right_gripper = robot_gripper.Gripper('right')	
		right_gripper.close()

		



		
		
