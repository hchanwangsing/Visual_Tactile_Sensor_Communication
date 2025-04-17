#Import the python libraries 
import cv2

#Import ROS2 package modules and libraries 
import rclpy 
from sensor_msgs.msg import Image 
from rclpy.node import Node 
from cv_bridge import CvBridge 

# ROS2 class node, subscribernodeclass inherits (or is a child of) the class called Node. 
class SubscriberNodeClass(Node):
            #constructor
            def __init__(self):
                #Initialize the attributes of parent class 
                super().__init__('subscriber_node')
                #CvBridge: to convert OpenCV images to ROS2 message, to be sent through topcis
                self.bridgeObject = CvBridge()
                #Topic Name to transfer camera images
                self.topicNameFrames='topic_camera_image'
                #Queue size for messages 
                self.queueSize=20
                #Fuction that creates a subscriber for image messages, over the topic with queue size stated above
                self.subscription = self.create_subscription (Image, self.topicNameFrames, self.listener_callbackFunction, self.queueSize)
                self.subscription#Prevent unused variable warning 

            #Callback function that displays the recieved image 
            def listener_callbackFunction(self, imageMessage):
                    #Display the message on the console
                    self.get_logger().info('The image frame is received')
                    #Convert ROS2 image message to openCV image
                    openCVImage = self.bridgeObject.imgmsg_to_cv2(imageMessage)
                    #Show image
                    cv2.imshow("Camera video", openCVImage)
                    cv2.waitKey(1)

# Main function entry point of the code 
def main(args=None):
     #Initialize rclpy
     rclpy.init(args=args)
     #Create subscriber object 
     subscriberNode = SubscriberNodeClass()
     #Spin the callback timer recursively 
     rclpy.spin(subscriberNode)
     #Destroy
     subscriberNode.destroy_node()
     #Shutdown
     rclpy.shutdown()

if __name__ == '__main__':
       main()