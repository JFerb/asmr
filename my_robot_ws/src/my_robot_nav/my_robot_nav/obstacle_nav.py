import time
import math
import rclpy
from rclpy.qos import qos_profile_sensor_data, QoSProfile, DurabilityPolicy
from rclpy.action import ActionClient
from rclpy.node import Node


from geometry_msgs.msg import PointStamped 
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool

from my_robot_interfaces.action import SetVelocity

from my_robot_perception.odom_utils import get_position, get_yaw
from my_robot_perception.scan_utils import sector_min, any_below


class ObstacleNavNode(Node):

    def __init__(self) -> None:
        super().__init__('obstacle_nav_node')
        self.goal_x = None
        self.goal_y = None
        self.latest_scan = None
        self.latest_odom = None
        self.current_state = None
        self.new_state = None
        self.goal_reached = False
        self.std_v = 0.2
        self.std_omega = 0.2

        # Subscribe to /goal_point to receive the goal
        latched = QoSProfile(
            depth=1,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        
        self.create_subscription(
            msg_type=PointStamped,
            topic='/goal_point',
            callback=self._goal_point_cb, 
            qos_profile=latched,
        )

        # Subscribe to /scan to get LiDAR scans
        self.create_subscription(
            msg_type=LaserScan, 
            topic='/scan',
            callback=self._scan_cb,
            qos_profile=qos_profile_sensor_data,
        )

        # Subscribe to /odom to get odometry info
        self.create_subscription(
            msg_type=Odometry,
            topic='/odom',
            callback=self._odom_cb,
            qos_profile=QoSProfile(depth=10)
        )

        self.create_subscription(
            msg_type=Bool, 
            topic='/goal_reached',
            callback=self._goal_reached_cb,
            qos_profile=latched
        )
        
        # Initialize ActionClient for /set_velocity
        self._velocity_client = ActionClient(self, SetVelocity, '/set_velocity')

        # Create timer for navigation
        self.create_timer(0.1, self.navigate)

    def _goal_point_cb(self, msg: PointStamped) -> None:
        self.goal_x = msg.point.x
        self.goal_y = msg.point.y
        
    def _scan_cb(self, msg: LaserScan) -> None:
        self.latest_scan = msg
        
    def _odom_cb(self, msg: Odometry) -> None:
        self.latest_odom = msg

    def _goal_reached_cb(self, msg: Bool) -> None:
        if msg.data:
            self.get_logger().info('Goal reached: stopping robot')
            self.goal_reached = True
            self.send_goal(0.0, 0.0)
            return

    def send_goal(self, linear_x: float, angular_z: float):
        goal = SetVelocity.Goal()kr
        goal.linear_x = linear_x
        goal.angular_z = angular_z

        if self.current_state != self.new_state:
            self.get_logger().info(
                f"{self.new_state}: "
                f"linear_x={goal.linear_x:.2f}, "
                f"angular_z={goal.angular_z:.2f}"
            )
            self.current_state = self.new_state
            
        if not self._velocity_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error(
                'Action server not available: /set_velocity'
            )
            return
        
        self._send_goal_future = self._velocity_client.send_goal_async(goal, feedback_callback=self._feedback_callback)

        self._send_goal_future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self._get_result_callback)

    def _get_result_callback(self, future):
        result = future.result().result

    def _feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        
    def navigate(self):
        if self.goal_reached:
            return
            
        if self.latest_scan is None or self.latest_odom is None:
            self.get_logger().info('Waiting for odom and lidar services...')
            return
        if self.goal_x is None or self.goal_y is None:
            self.get_logger().info('Waiting for goal point...')
            return
            
        front = sector_min(self.latest_scan, -30.0, 30.0)
        left = sector_min(self.latest_scan, 30, 90)
        right = sector_min(self.latest_scan, -90, -30)

        # Safety rule: if front < 0.3, then stop
        if front < 0.3:
            self.new_state = "Safety"
            self.send_goal(-self.std_v, self.std_omega)       

        # Avoidance rule: if front < 0.6, then turn wherever there is more space
        elif front < 0.6:
            self.new_state = "Avoidance front"
            if left < right:
                self.send_goal(0.0, -self.std_omega)
            else:
                self.send_goal(0.0, self.std_omega)
        elif right < 0.6:
            self.new_state = "Avoidance right"
            self.send_goal(self.std_v, self.std_omega)
        elif left < 0.6:
            self.new_state = "Avoidance left"
            self.send_goal(self.std_v, -self.std_omega)
                
        # Navigation: else: drive towards goal
        else:
            current_odom_x, current_odom_y = get_position(self.latest_odom)
            current_x = current_odom_x 
            current_y = current_odom_y
            current_yaw = get_yaw(self.latest_odom)
            dx = self.goal_x - current_x
            dy = self.goal_y - current_y
            desired_yaw = math.atan2(dy, dx)
            error_raw = desired_yaw - current_yaw
            error = math.atan2(math.sin(error_raw), math.cos(error_raw))
                
            if abs(error) > 0.25:
                self.new_state = "Turn to goal"
                self.send_goal(self.std_v, self.std_omega * self.sign(error))
            else:
                self.new_state = "Forward"
                self.send_goal(self.std_v, 0.0)

    def sign(self, x):
        return 1.0 if x > 0 else -1.0

def main(args=None) -> None:
    rclpy.init(args=args)
    node = ObstacleNavNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()