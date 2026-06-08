# Copyright 2026 Janosch Bajorath
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Draw a five-pointed star in turtlesim.

Demonstrates three ROS 2 communication patterns:
  - Topic   : geometry_msgs/Twist on /turtle1/cmd_vel  (Task 4)
  - Service : SetPen and TeleportAbsolute              (Task 5)
  - Action  : turtlesim/RotateAbsolute                 (Task 6)

All work runs sequentially inside __init__ before rclpy.spin() is called.
spin() in main() is a keepalive only — the star is already drawn by the time
it runs. This is safe because spin_until_future_complete and the edge-drawing
loop both work from __init__ precisely because no executor is running yet.
"""
from geometry_msgs.msg import Twist
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute
from turtlesim.srv import SetPen, TeleportAbsolute


# Absolute headings (rad, CCW from +x) for the five edges of a pentagram.
# Each consecutive edge turns 144 deg (= 2/5 * 360 deg), visiting every
# second vertex of the underlying regular pentagon in order.
_STAR_HEADINGS = [0.0, 2.5133, 5.0265, 1.2566, 3.7699]

_EDGE_SPEED = 1.0   # turtlesim units per second
_TICK_HZ = 10       # publish rate during an edge (Hz)
_TICK_SEC = 1.0 / _TICK_HZ
_EDGE_TICKS = 30    # 30 ticks * 0.1 s = 3.0 s = 3.0 turtlesim units


class StarNode(Node):
    """
    Drive turtlesim to draw a five-pointed star.

    The node teleports to a fixed starting position, then executes a loop of
    five (rotate → draw-edge) iterations. All of this happens inside __init__.
    """

    def __init__(self) -> None:
        """Set up clients and draw the star."""
        super().__init__('star_node')

        # --- Create publisher and clients ---
        # No timer is needed: edge drawing is handled by a direct publish loop
        # inside __init__ (see _draw_edge). A timer would only fire after
        # rclpy.spin() starts, which is after __init__ returns.
        #
        # Absolute topic/service/action names (/turtle1/...) are used
        # intentionally: turtlesim hard-codes its namespace, so there is no
        # relative name that resolves correctly. This is an exception to the
        # usual ROS 2 convention of preferring relative names.
        self._cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self._pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self._teleport_client = self.create_client(
            TeleportAbsolute, '/turtle1/teleport_absolute'
        )
        # ActionClient is not a service client — it uses a different wait call.
        self._rotate_client = ActionClient(
            self, RotateAbsolute, '/turtle1/rotate_absolute'
        )

        # --- Wait for all servers ---
        # wait_for_service returns False on timeout instead of raising, so we
        # check the return value and abort with a clear error rather than
        # crashing later with a cryptic future-related exception.
        for client, name in [
            (self._pen_client, '/turtle1/set_pen'),
            (self._teleport_client, '/turtle1/teleport_absolute'),
        ]:
            if not client.wait_for_service(timeout_sec=5.0):
                self.get_logger().error(f'Service not available: {name}')
                return

        if not self._rotate_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error(
                'Action server not available: /turtle1/rotate_absolute'
            )
            return

        # --- Setup: reposition the turtle without leaving a trail ---
        # Sequence matters: pen off first, then teleport, then pen on.
        # Each call blocks until the server replies (via spin_until_future_complete
        # inside _call_service), so the order is guaranteed.
        self._call_service(self._pen_client, SetPen.Request(off=1))
        self._call_service(
            self._teleport_client,
            TeleportAbsolute.Request(x=4.0, y=5.0, theta=0.0),
        )
        # Re-enable with a visible white pen (r/g/b are uint8, 0-255).
        self._call_service(
            self._pen_client,
            SetPen.Request(r=255, g=255, b=255, width=2, off=0),
        )

        # --- Draw the star ---
        for heading in _STAR_HEADINGS:
            self._rotate_to(heading)
            self._draw_edge()

        # turtlesim keeps moving at the last commanded velocity until a new
        # message arrives — send zero to stop the turtle immediately.
        self._cmd_pub.publish(Twist())
        # Lift the pen so the cleanup move leaves no trail.
        self._call_service(self._pen_client, SetPen.Request(off=1))
        # Move the turtle away from the star's start point so it does not
        # sit on top of the finished drawing.
        self._call_service(
            self._teleport_client,
            TeleportAbsolute.Request(x=1.0, y=1.0, theta=0.0),
        )
        self.get_logger().info('Star complete.')

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _call_service(self, client, request) -> None:
        """
        Send a service request and block until the response arrives.

        Uses spin_until_future_complete rather than future.result() because
        the ROS 2 event loop must process the response callback — simply
        checking the future in a tight loop would spin-lock without ever
        receiving the reply.
        """
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def _rotate_to(self, heading: float) -> None:
        """
        Send a RotateAbsolute goal and block until rotation is complete.

        The action uses a two-stage future:
          1. send_goal_async  → goal handle  (server accepted the goal)
          2. get_result_async → result       (turtle has finished rotating)

        Both stages require spin_until_future_complete. The second stage is
        the important one: starting the next edge before the rotation finishes
        would distort the star because the edge would begin at the wrong angle.
        """
        goal = RotateAbsolute.Goal(theta=heading)

        # Stage 1: confirm the server accepted the goal.
        goal_future = self._rotate_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, goal_future)

        handle = goal_future.result()
        if not handle.accepted:
            self.get_logger().warning(f'Goal rejected for heading {heading:.4f}')
            return

        # Stage 2: wait for the turtle to finish rotating.
        result_future = handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

    def _draw_edge(self) -> None:
        """
        Publish forward velocity for one edge of the star.

        Uses rclpy.spin_once between publishes instead of time.sleep.
        spin_once processes any pending ROS callbacks (e.g. action feedback)
        while pausing for the tick duration, keeping the event loop healthy.
        time.sleep would also work here (we are in __init__, not inside a
        running executor), but spin_once is the better habit.
        """
        twist = Twist()
        twist.linear.x = _EDGE_SPEED
        for _ in range(_EDGE_TICKS):
            self._cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=_TICK_SEC)


def main(args=None) -> None:
    """Initialise rclpy, run the node, and shut down cleanly."""
    rclpy.init(args=args)
    node = StarNode()
    try:
        # By the time spin() is called, the star is already drawn.
        # spin() keeps the node alive so turtlesim stays open and the
        # user can see the result. Press Ctrl+C to exit.
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
