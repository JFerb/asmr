from geometry_msgs.msg import Twist
import time


def drive(publisher, linear_x, angular_z, duration_s):
    msg = Twist()
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    
    publisher.publish(msg)
    time.sleep(duration_s)

def stop(publisher):
    msg = Twist()
    publisher.publish(msg)