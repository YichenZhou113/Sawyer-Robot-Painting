#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the dependencies as described in example_pub.py
import rospy
from std_msgs.msg import String
#from my_chatter.msg import TimestampString
from sensor_msgs.msg import Image
import cv2
import time
from cv_bridge import CvBridge, CvBridgeError

#Define the callback method which is called whenever this node receives a 
#message on its subscribed topic. The received message is passed as the 
#first argument to callback().
i = 0
bridge = CvBridge()

def callback(message):
    global i
    global bridge
    #Print the contents of the message to the console
    cv_image = bridge.imgmsg_to_cv2(message)
    # cur_time = time.time()
    # cur_img = cv_image.copy()
    # cur_img[:,:,0] = cv_image[:,:,2]
    # cur_img[:,:,2] = cv_image[:,:,0]
    if(i%100==1):
        print("enter")
        # cv2.imwrite('test'+str(time.time())+'.jpg', cv_image)
        cv2.imwrite('./src/planning/src/test.jpg', cv_image)
    i+=1
    # print(rospy.get_name() + " Message: " + message.UserInput + ", Sent at: " + str(message.Time) \
    #     + ", Received at: " + str(rospy.get_time()))

#Define the method which contains the node's main functionality
def listener():

    #Run this program as a new node in the ROS computation graph
    #called /listener_<id>, where <id> is a randomly generated numeric
    #string. This randomly generated name means we can start multiple
    #copies of this node without having multiple nodes with the same
    #name, which ROS doesn't allow.
    rospy.init_node('listener', anonymous=True)

    #Create a new instance of the rospy.Subscriber object which we can 
    #use to receive messages of type std_msgs/String from the topic /chatter_talk.
    #Whenever a new message is received, the method callback() will be called
    #with the received message as its first argument.
    rospy.Subscriber("usb_cam/image_raw", Image, callback)


    #Wait for messages to arrive on the subscribed topics, and exit the node
    #when it is killed with Ctrl+C
    rospy.spin()


#Python's syntax for a main() method
if __name__ == '__main__':
    listener()
