#Import the python libraries 
import cv2 # type: ignore

#Import ROS2 package modules and libraries 
import rclpy 
from sensor_msgs.msg import Image 
from rclpy.node import Node 
from cv_bridge import CvBridge 

# ROS2 class node, publishernodeclass inherits (or is a child of) the class called Node. 
class PublisherNodeClass(Node):
       #constructor 
     def __init__(self):
          #Initialize the attributes of parent class 
          super().__init__('publisher_node')
          #Create an instance of OpenCV VideoCapture object
          self.cameraDeviceNumber=0
          self.camera=cv2.VideoCapture(self.cameraDeviceNumber)
          #CvBridge: to convert OpenCV images to ROS2 message, to be sent through topcis
          self.bridgeObject = CvBridge()
          #Topic Name to transfer camera images
          self.topicNameFrames='topic_camera_image'
          #Queue size for messages 
          self.queueSize=20
          #Fuction that creates a publisher for image messages, over the topic with queue size stated above
          self.publisher = self.create_publisher (Image, self.topicNameFrames, self.queueSize)
          #communication period in seconds 
          self.periodCommunication = 0.02
          #Create timer that calls the function self.timer_callback every communication period 
          self.timer = self.create_timer(self.periodCommunication, self.timer_callbackFunction)
          #Counter tracking how many images are published 
          self.i =0 
               
     def timer_callbackFunction(self):
     #Read the frame of camera 
          success, frame = self.camera.read()
     #Resize the image 
          frame = cv2.resize(frame, (820,640), interpolation=cv2.INTER_CUBIC)

          if success == True:
               #Convert OpenvCV frame to
               ROS2ImageMessage=self.bridgeObject.cv2_to_imgmsg(frame)
               #Publish the image 
               self.publisher.publish(ROS2ImageMessage)

               #Use the logger to display the message on the screen 
               self.get_logger().info('Publishing image number %d' %self.i)
               #Update the img counter 
          self.i += 1 
               
# Main function entry point of the code 
def main(args=None):
     #Initialize rclpy
     rclpy.init(args=args)
     #Create publisher object 
     publisherObject = PublisherNodeClass()
     #Spin the callback timer recursively 
     rclpy.spin(publisherObject)
     #Destroy
     publisherObject.destroy_node()
     #Shutdown
rclpy.shutdown()

if __name__ == '__main__':
     main()

          




