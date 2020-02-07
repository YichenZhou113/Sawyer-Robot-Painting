#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
from planning.msg import ChouChou

#Import the String message type from the /msg directory of
#the std_msgs package.
from std_msgs.msg import String
import numpy as np
from image_processor import imgProcess

def create_ChouChou(x,y,z,g,s,a):
	# print(x, y, z, g, s, a)
	return ChouChou(position_x=x,position_y=y,position_z=z,edge_grad=g,status_type=s,pen_type=a)

queue = [create_ChouChou(13333,4,0.2,0.4,"dummy",0),
					create_ChouChou(0.2,0.4,0.1,0.4,"dummy",0),
					create_ChouChou(0.10,0.4,0.6,0.2,"dummy",0),
					create_ChouChou(9,3,2,1,"dummy",0),
					create_ChouChou(3,2,1,3,"dummy",0)]  


center = (0.670, -0.149)
radius = 0.1

# rospy.sleep(2)
# count = 0
# for i in np.linspace(center[0] - radius, center[0] + radius, 20):
# 	count += 1
# 	t = np.abs(i - center[0])
# 	x = np.sqrt(radius ** 2 - t ** 2)
# 	if np.isnan(x):
# 			x = 0

# 	if i == center[0] - radius:
# 		queue.append(create_ChouChou(i, center[1]-x, -0.078, 0, "starting"))
# 	else:
# 		queue.append(create_ChouChou(i, center[1]+x, -0.078, 0, "next_point"))
# 		queue.append(create_ChouChou(i, center[1]-x, -0.078, 0, "next_point"))

# queue.append(create_ChouChou(0, 0, 0, 0, "ending"))

#Define the method which contains the main functionality of the node.
def talker():

	#Run this program as a new node in the ROS computation graph 
	#called /talker.
	rospy.init_node('point_sender', anonymous=True)

	#Create an instance of the rospy.Publisher object which we can 
	#use to publish messages to a topic. This publisher publishes 
	#messages of type std_msgs/String to the topic /chatter_talk
	pub = rospy.Publisher('position_messages', ChouChou, queue_size=10000)
	
	# Create a timer object that will sleep long enough to result in
	# a 10Hz publishing rate
	r = rospy.Rate(50) # 10hz

	# for q in queue:
	# 	pub_content = q

	# 	# Publish our string to the 'chatter_talk' topic
	# 	pub.publish(pub_content)
		
	# 	# Use our rate object to sleep until it is time to publish again
	# 	r.sleep()

	# Loop until the node is killed with Ctrl-C
	while not rospy.is_shutdown():
		# Construct a string that we want to publish
		# (In Python, the "%" operator functions similarly
		#  to sprintf in C or MATLAB)

		

		# user_enter = raw_input("Please enter a line of text and press <Enter>: ")
		# send_time = rospy.get_time()
		# pub_string = user_enter + " " + str(rospy.get_time())
		while len(queue)>0:
			cur = queue.pop(0)
			# print("cur_point !!!!!!!!!!!!!!!!!!!!             ", cur)
			
			pub_content = cur

			# Publish our string to the 'chatter_talk' topic
			pub.publish(pub_content)
			# print("currrrrrr  ", len(queue))
			
			# Use our rate object to sleep until it is time to publish again
			r.sleep()
			
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
	points = imgProcess.getPoints()  # {area number: [(starts in world frame, ends in world frame)]}
	for combined in points:
		pen, data = combined
		pen = pen - 1
		for i, stroke in enumerate(data):
<<<<<<< HEAD
=======
			if len(stroke) <= 3:
				continue
>>>>>>> origin/final
			first = True
			z = -0.015
			for (x, y) in stroke:
				if first:  # the start point of the whole area
					queue.append(create_ChouChou(x, y, z, 0, "starting", pen))
					first = False
				else:
					queue.append(create_ChouChou(x, y, z, 0, "next_point", pen))
					
			queue.append(create_ChouChou(x, y, z, 0, "ending", pen))
	print("end queue push", len(queue))


	# Check if the node has received a signal to shut down
	# If not, run the talker method
	try:
		talker()
	except rospy.ROSInterruptException: pass



	# points = imgProcess.getPoints()  # {area number: [(starts in world frame, ends in world frame)]}
	# for area in points:
	# 	first = True
	# 	z = -0.015
	# 	for (start, end) in points[area]:
	# 		if first:  # the start point of the whole area
	# 			# z = -0.078
				
	# 			queue.append(create_ChouChou(start[0], start[1], z, 0, "starting"))
	# 			queue.append(create_ChouChou(end[0], end[1], z, 0, "next_point"))

	# 			first = False
	# 		else:
	# 			queue.append(create_ChouChou(start[0], start[1], z, 0, "next_point"))
	# 			queue.append(create_ChouChou(end[0], end[1], z, 0, "next_point"))
	# 	queue.append(create_ChouChou(0, 0, 0, 0, "ending"))
	# print("end queue push", len(queue))


	# # Check if the node has received a signal to shut down
	# # If not, run the talker method
	# try:
	# 	talker()
	# except rospy.ROSInterruptException: pass