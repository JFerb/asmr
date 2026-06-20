"""Shared scaffolding for reactive navigation nodes.

Provides the SetVelocity action client, goal_reached stop behaviour,
dead-zone-throttled goal sending, and a multi-threaded executor run helper.

Subclasses subscribe to whatever sensors their policy needs and call
self._send_velocity(vx, wz) from their own callbacks. The base does not
subscribe to scan, scan_points, or odom — sensor modality is a subclass
concern.
"""
import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import (
    DurabilityPolicy,
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
)

from std_msgs.msg import Bool

from my_robot_interfaces.action import SetVelocity


def in_deadzone(new_vx: float, new_wz: float,
                last_vx: float, last_wz: float,
                linear_tol: float = 0.02, angular_tol: float = 0.05) -> bool:
    """Return True if (vx, wz) is within tol of the last sent values."""
    return (abs(new_vx - last_vx) < linear_tol
            and abs(new_wz - last_wz) < angular_tol)


class ReactiveNavBase(Node):
    """Base class for reactive-nav nodes that command via SetVelocity.

    Subclasses must:
      - call ``super().__init__(node_name)``
      - create their own sensor subscriptions (using ``self._cb_group``)
      - call ``self._send_velocity(vx, wz)`` from those callbacks
    """

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name)

        self._stopped = False
        self._last_sent: tuple[float, float] | None = None
        self._current_goal_handle = None

        self._cb_group = ReentrantCallbackGroup()

        self._action_client = ActionClient(
            self, SetVelocity, 'set_velocity', callback_group=self._cb_group
        )

        latched_qos = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.create_subscription(
            Bool, 'goal_reached', self._goal_cb, latched_qos,
            callback_group=self._cb_group,
        )

    def _goal_cb(self, msg: Bool) -> None:
        if msg.data and not self._stopped:
            self._stopped = True
            # Bypass the dead-zone for the stop command — we must guarantee
            # the zero-velocity goal is sent even if we happened to be at rest.
            self._last_sent = None
            self._send_velocity(0.0, 0.0)
            self.get_logger().info('Goal reached signal received. Stopping.')

    def _send_velocity(self, vx: float, wz: float) -> None:
        if self._last_sent is not None:
            last_vx, last_wz = self._last_sent
            if in_deadzone(vx, wz, last_vx, last_wz):
                return

        if self._current_goal_handle is not None:
            try:
                self._current_goal_handle.cancel_goal_async()
            except Exception:
                pass
            self._current_goal_handle = None

        if not self._action_client.wait_for_server(timeout_sec=0.0):
            return

        goal = SetVelocity.Goal()
        goal.linear_x = float(vx)
        goal.angular_z = float(wz)
        send_future = self._action_client.send_goal_async(goal)
        send_future.add_done_callback(
            lambda fut: self._on_goal_response(fut, vx, wz)
        )

    def _on_goal_response(self, future, sent_vx: float, sent_wz: float) -> None:
        try:
            goal_handle = future.result()
        except Exception as exc:
            self.get_logger().warning(
                f'send_goal_async failed: {exc}',
                throttle_duration_sec=2.0,
            )
            return
        if goal_handle is None or not goal_handle.accepted:
            return
        self._last_sent = (sent_vx, sent_wz)
        self._current_goal_handle = goal_handle


def run(cls) -> None:
    """Run the node with a MultiThreadedExecutor until shutdown."""
    rclpy.init()
    node = cls()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
