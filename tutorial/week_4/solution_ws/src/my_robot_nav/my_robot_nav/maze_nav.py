"""Right-hand wall-follower with scan + odom fusion-based stuck detection.

Normal policy (right-hand rule): keep the right wall at WALL_TARGET via
sector_min on scan; turn left in place when the front is blocked; drift
right when the wall is too far.

Stuck check (scheme B): maintain rolling buffers of odom positions and
scan ranges over STUCK_WINDOW_SEC. On each scan callback, compare the
claimed odom displacement against the scan-array change. If odom claims
motion (d_odom > STUCK_D_ODOM_MIN) but the world looks static
(s_change < STUCK_SCAN_DELTA), execute a reverse-and-turn escape for
ESCAPE_DURATION_SEC, then resume normal policy.
"""
from collections import deque

from nav_msgs.msg import Odometry
import numpy as np
from rclpy.duration import Duration
from sensor_msgs.msg import LaserScan

from my_robot_nav.base import ReactiveNavBase, run
from my_robot_perception.odom_utils import get_position
from my_robot_perception.scan_utils import sector_min


class MazeNav(ReactiveNavBase):
    """Right-hand wall follower on scan with odomscan fusion stuck-escape."""

    # Wall-follower
    FRONT_BLOCKED       = 0.5
    WALL_TARGET         = 0.35
    WALL_TOLERANCE      = 0.15
    DRIVE_SPEED         = 0.25
    SEARCH_SPEED        = 0.18
    TURN_SPEED          = 0.5
    DRIFT_TURN_SPEED    = -0.3
    WALL_KP             = -0.5

    # Stuck detector (scheme B)
    STUCK_WINDOW_SEC    = 2.0
    STUCK_D_ODOM_MIN    = 0.4    # m
    STUCK_SCAN_DELTA    = 0.05   # m

    # Escape
    ESCAPE_DURATION_SEC = 1.5
    ESCAPE_REVERSE_VX   = -0.15
    ESCAPE_TURN_WZ      = -TURN_SPEED  # opposite of normal in-place turn

    def __init__(self) -> None:
        super().__init__('maze_nav')

        self._pose_buf: deque[tuple[float, float, float]] = deque()
        self._scan_buf: deque[tuple[float, np.ndarray]] = deque()
        self._escape_until = None  # rclpy.time.Time or None

        self.create_subscription(
            LaserScan, 'scan', self._scan_cb, 10,
            callback_group=self._cb_group,
        )
        self.create_subscription(
            Odometry, 'odom', self._odom_cb, 10,
            callback_group=self._cb_group,
        )

        self.get_logger().info(
            'maze_nav started: right-hand wall-follower + stuck detector'
        )

    def _now_sec(self) -> float:
        return self.get_clock().now().nanoseconds * 1e-9

    def _trim_buf(self, buf: deque, now: float) -> None:
        cutoff = now - self.STUCK_WINDOW_SEC
        while buf and buf[0][0] < cutoff:
            buf.popleft()

    def _odom_cb(self, msg: Odometry) -> None:
        x, y = get_position(msg)
        t = self._now_sec()
        self._pose_buf.append((t, x, y))
        self._trim_buf(self._pose_buf, t)

    def _scan_cb(self, msg: LaserScan) -> None:
        if self._stopped:
            return

        t = self._now_sec()
        ranges = np.asarray(msg.ranges, dtype=np.float64)
        self._scan_buf.append((t, ranges))
        self._trim_buf(self._scan_buf, t)

        # 1. Escape phase: hold the escape command until duration elapses.
        if self._escape_until is not None:
            if self.get_clock().now() < self._escape_until:
                self._send_velocity(self.ESCAPE_REVERSE_VX,
                                    self.ESCAPE_TURN_WZ)
                return
            self._escape_until = None

        # 2. Stuck check: only with a full window of history.
        if self._buffers_full(t) and self._is_stuck():
            self._escape_until = (
                self.get_clock().now()
                + Duration(seconds=self.ESCAPE_DURATION_SEC)
            )
            self._pose_buf.clear()
            self._scan_buf.clear()
            self.get_logger().warning('stuck detected — entering escape')
            self._send_velocity(self.ESCAPE_REVERSE_VX,
                                self.ESCAPE_TURN_WZ)
            return

        # 3. Normal right-hand rule.
        front = sector_min(msg, -30.0, 30.0)
        right = sector_min(msg, -90.0, -30.0)

        if front < self.FRONT_BLOCKED:
            vx, wz = 0.0, self.TURN_SPEED
        elif right > self.WALL_TARGET + self.WALL_TOLERANCE:
            vx, wz = self.SEARCH_SPEED, self.DRIFT_TURN_SPEED
        else:
            vx = self.DRIVE_SPEED
            wz = self.WALL_KP * (right - self.WALL_TARGET)

        self._send_velocity(vx, wz)

    def _buffers_full(self, now: float) -> bool:
        if not self._pose_buf or not self._scan_buf:
            return False
        return (now - self._pose_buf[0][0] >= self.STUCK_WINDOW_SEC
                and now - self._scan_buf[0][0] >= self.STUCK_WINDOW_SEC)

    def _is_stuck(self) -> bool:
        _, x0, y0 = self._pose_buf[0]
        _, x1, y1 = self._pose_buf[-1]
        d_odom = float(np.hypot(x1 - x0, y1 - y0))

        _, r0 = self._scan_buf[0]
        _, r1 = self._scan_buf[-1]
        if r0.shape != r1.shape:
            return False
        diff = np.abs(r1 - r0)
        diff = diff[np.isfinite(diff)]
        if diff.size == 0:
            return False
        s_change = float(diff.mean())

        return (d_odom > self.STUCK_D_ODOM_MIN
                and s_change < self.STUCK_SCAN_DELTA)


def main(args=None) -> None:
    run(MazeNav)
