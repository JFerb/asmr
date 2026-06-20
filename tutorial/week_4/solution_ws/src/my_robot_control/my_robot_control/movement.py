"""Open-loop velocity primitives for the week-3 move_square demo.

drive() publishes a constant Twist for a fixed duration; stop() publishes
zero. Used only by move_square -- the MiniLab 1 architecture commands motion
through the SetVelocity action server instead.
"""
import time

from geometry_msgs.msg import Twist


def drive(publisher, linear_x: float, angular_z: float, duration_s: float) -> None:
    msg = Twist()
    msg.linear.x = float(linear_x)
    msg.angular.z = float(angular_z)
    publisher.publish(msg)
    time.sleep(duration_s)


def stop(publisher) -> None:
    publisher.publish(Twist())
