import time
import rclpy
from my_robot_control.movement import drive, stop
from geometry_msgs.msg import Twist

def main():
    rclpy.init()
    node = rclpy.create_node("move_square")
    publisher = node.create_publisher(Twist, "/cmd_vel", 10)
    time.sleep(2.0)

    forward_speed = 0.2
    forward_time = 3.0

    turn_speed = 0.5
    turn_time = 3.14

    for _ in range(4):
        drive(publisher, forward_speed, 0.0, forward_time)
        drive(publisher, 0.0, turn_speed, turn_time)

    stop(publisher)
    time.sleep(0.1)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()