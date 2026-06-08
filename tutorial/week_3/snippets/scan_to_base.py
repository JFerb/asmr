import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped
import tf2_ros
import tf2_geometry_msgs  # noqa: F401  (registers transform support for PointStamped)
import math


class ScanToBase(Node):

    def __init__(self):
        super().__init__('scan_to_base')
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)
        self.create_subscription(LaserScan, '/scan', self._scan_cb, 10)

    def _scan_cb(self, msg: LaserScan) -> None:
        # TODO 1: find the index of the minimum range value in msg.ranges
        #         (ignore inf and nan values — use math.isfinite())
        idx = ...

        # TODO 2: compute the angle of that beam
        #         angle = msg.angle_min + idx * msg.angle_increment
        angle = ...

        # TODO 3: convert polar (msg.ranges[idx], angle) to Cartesian (x, y)
        #         in the lidar_link frame  —  x = r*cos(θ),  y = r*sin(θ)
        x = ...
        y = ...

        # TODO 4: fill in the PointStamped message
        point_in_lidar = PointStamped()
        point_in_lidar.header.frame_id = ...   # which frame is this point in?
        point_in_lidar.header.stamp = ...       # use the scan message's timestamp
        point_in_lidar.point.x = x
        point_in_lidar.point.y = y
        point_in_lidar.point.z = 0.0

        # TODO 5: look up the transform from lidar_link to base_link
        #         use rclpy.time.Time() to request the latest available transform
        try:
            tf = self._tf_buffer.lookup_transform(
                ...,   # target frame
                ...,   # source frame
                ...,   # time
            )
        except tf2_ros.LookupException:
            return

        # TODO 6: apply the transform to obtain the point in base_link
        point_in_base = tf2_geometry_msgs.do_transform_point(point_in_lidar, tf)

        self.get_logger().info(
            f'Nearest obstacle — lidar_link: ({x:.3f}, {y:.3f}, 0.000)  '
            f'base_link: ({point_in_base.point.x:.3f}, '
            f'{point_in_base.point.y:.3f}, '
            f'{point_in_base.point.z:.3f})'
        )


def main():
    rclpy.init()
    rclpy.spin(ScanToBase())
    rclpy.shutdown()
