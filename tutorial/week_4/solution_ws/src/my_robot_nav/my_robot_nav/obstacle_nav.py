"""Potential-field obstacle avoidance on scan_points.

Each cartesian scan point exerts a repulsive force with quadratic falloff;
a constant-magnitude attractive force points from the robot toward the
goal coordinate (in world frame), which is delivered on goal_point by
goal_checker_node (latched).

Sends velocity commands through the SetVelocity action client to
my_robot_control's velocity_controller_node. On goal_reached, the base
class sends a zero-velocity goal to halt cleanly.
"""
import math

from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry
import numpy as np
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import PointCloud2

from my_robot_nav.base import ReactiveNavBase, run
from my_robot_nav.visuals import PotentialFieldViz
from my_robot_perception.odom_utils import get_position, get_yaw
from my_robot_perception.scan_utils import pointcloud2_to_xy


class ObstacleNav(ReactiveNavBase):
    """Potential-field obstacle avoidance commanded via SetVelocity.

    Repulsion from scan_points plus a constant goal-directed attractive force.
    """

    F_REPULSE_GAIN   = 0.05    # per-point gain; summed across all LiDAR hits within range
    F_REPULSE_RANGE  = 1.0     # m; points farther than this contribute nothing
    F_REPULSE_RMIN   = 0.15    # m; floor in 1/r² so near-min returns don't dominate
    VORTEX_ALPHA_DEG = 45.0    # tangential mix: 0 = pure away, 90 = pure orbit
    TANGENT_USE_CCW  = True    # always deflect to the same side (avoids dynamic-flip oscillation)
    F_ATTRACT_MAG    = 1.0     # constant magnitude of the attractive pull
    VX_GAIN          = 0.2     # forward force → linear velocity
    WZ_GAIN          = 0.6     # lateral force → angular velocity (linear, not atan2)
    MAX_VX           = 0.25
    MAX_WZ           = 0.8

    VIZ_ENABLED      = True

    def __init__(self) -> None:
        super().__init__('obstacle_nav')

        self._goal: tuple[float, float] | None = None     # (gx, gy) in world frame
        self._latest_x: float | None = None
        self._latest_y: float | None = None
        self._latest_yaw: float = 0.0

        self._viz = PotentialFieldViz(self) if self.VIZ_ENABLED else None

        # Goal coordinate delivered by goal_checker_node on a latched topic.
        latched_qos = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.create_subscription(
            PointStamped, 'goal_point', self._goal_point_cb, latched_qos,
            callback_group=self._cb_group,
        )

        self.create_subscription(
            PointCloud2, 'scan_points', self._points_cb, 10,
            callback_group=self._cb_group,
        )
        self.create_subscription(
            Odometry, 'odom', self._odom_cb, 10,
            callback_group=self._cb_group,
        )

        self.get_logger().info(
            'obstacle_nav started: potential field on scan_points + goal-directed attractive'
        )

    def _goal_point_cb(self, msg: PointStamped) -> None:
        gx, gy = float(msg.point.x), float(msg.point.y)
        prev = self._goal
        self._goal = (gx, gy)
        if prev is None or prev != self._goal:
            self.get_logger().info(f'goal received: ({gx:.2f}, {gy:.2f})')

    def _odom_cb(self, msg: Odometry) -> None:
        x, y = get_position(msg)
        self._latest_x = x
        self._latest_y = y
        self._latest_yaw = get_yaw(msg)

    def _points_cb(self, msg: PointCloud2) -> None:
        if self._stopped:
            return
        if (self._goal is None
                or self._latest_x is None
                or self._latest_y is None):
            self._send_velocity(0.0, 0.0)
            return

        xy = pointcloud2_to_xy(msg)

        # Attractive (world frame): unit vector from robot to goal, scaled
        # by F_ATTRACT_MAG. Constant magnitude regardless of distance so the
        # repulsive force can balance it sensibly at every range.
        gx, gy = self._goal
        dx = gx - self._latest_x
        dy = gy - self._latest_y
        dist = math.hypot(dx, dy)
        if dist < 1e-3:
            f_att_world = np.zeros(2, dtype=np.float64)
        else:
            f_att_world = np.array([
                self.F_ATTRACT_MAG * dx / dist,
                self.F_ATTRACT_MAG * dy / dist,
            ], dtype=np.float64)

        # Rotate the world-frame attractive into base_link.
        c, s = math.cos(self._latest_yaw), math.sin(self._latest_yaw)
        f_att = np.array([
             c * f_att_world[0] + s * f_att_world[1],
            -s * f_att_world[0] + c * f_att_world[1],
        ], dtype=np.float64)

        # Vortex tangent: hard-coded handedness. Dynamic decision-making
        # tends to flip when the robot rotates (attractive direction shifts
        # in base_link), causing oscillation. Always-CCW commits the robot
        # to passing every obstacle on the same side.
        f_rep = self._repulsive_force(xy, self.TANGENT_USE_CCW)

        f = f_rep + f_att

        # Decoupled force-to-twist mapping (avoids the atan2 discontinuity at
        # F.x ≈ 0): forward speed from F.x, angular rate proportional to F.y.
        vx = float(np.clip(f[0] * self.VX_GAIN, 0.0, self.MAX_VX))
        wz = float(np.clip(f[1] * self.WZ_GAIN, -self.MAX_WZ, self.MAX_WZ))

        self._send_velocity(vx, wz)

        if self._viz is not None:
            self._viz.publish(
                f_rep, f_att, f,
                grid_eval=self._make_grid_eval(xy, self.TANGENT_USE_CCW),
                heatmap_eval=self._make_heatmap_eval(xy, self.TANGENT_USE_CCW),
            )

    def _repulsive_force(self, xy: np.ndarray, use_ccw: bool) -> np.ndarray:
        """Vortex-modified repulsion from obstacle points in base_link.

        Stateless. Direction per point is a blend of radial (away) and
        tangential (radial rotated 90° with the sign given by ``use_ccw``).
        """
        f_rep = np.zeros(2, dtype=np.float64)
        if xy.shape[0] == 0:
            return f_rep
        r = np.hypot(xy[:, 0], xy[:, 1])
        mask = (r > 1e-3) & (r < self.F_REPULSE_RANGE)
        if not mask.any():
            return f_rep
        r_m = r[mask]
        unit = xy[mask] / r_m[:, None]
        r_eff = np.maximum(r_m, self.F_REPULSE_RMIN)
        strength = self.F_REPULSE_GAIN * (1.0 / r_m - 1.0 / self.F_REPULSE_RANGE) / (r_eff * r_eff)

        radial = -unit
        if use_ccw:
            tangent = np.column_stack([-radial[:, 1], radial[:, 0]])
        else:
            tangent = np.column_stack([ radial[:, 1], -radial[:, 0]])

        alpha = math.radians(self.VORTEX_ALPHA_DEG)
        ca, sa = math.cos(alpha), math.sin(alpha)
        direction = ca * radial + sa * tangent
        return np.sum(strength[:, None] * direction, axis=0)

    def _make_grid_eval(self, xy: np.ndarray, use_ccw: bool):
        """Closure that evaluates the field at offset (gx, gy) in base_link.

        BOTH components recompute per cell:
          - Repulsive: from the offset LiDAR points.
          - Attractive: convert the base_link cell to world coordinates,
            compute the unit vector from the cell's world position to the
            goal, scale by F_ATTRACT_MAG, rotate back into base_link.
        This shows the actual goal-directed field at every grid point.
        """
        if self._goal is None or self._latest_x is None or self._latest_y is None:
            return lambda gx, gy: np.zeros(2, dtype=np.float64)

        yaw = self._latest_yaw
        robot_x = float(self._latest_x)
        robot_y = float(self._latest_y)
        goal_x, goal_y = self._goal
        c, s = math.cos(yaw), math.sin(yaw)
        mag = self.F_ATTRACT_MAG

        def eval_at(gx: float, gy: float) -> np.ndarray:
            # base_link cell → world position
            world_x_cell = robot_x + c * gx - s * gy
            world_y_cell = robot_y + s * gx + c * gy
            dx = goal_x - world_x_cell
            dy = goal_y - world_y_cell
            dist = math.hypot(dx, dy)
            if dist < 1e-3:
                f_att_world = np.zeros(2, dtype=np.float64)
            else:
                f_att_world = np.array([mag * dx / dist, mag * dy / dist],
                                       dtype=np.float64)
            f_att_cell = np.array([
                 c * f_att_world[0] + s * f_att_world[1],
                -s * f_att_world[0] + c * f_att_world[1],
            ], dtype=np.float64)
            rel = xy - np.array([gx, gy]) if xy.shape[0] > 0 else xy
            return self._repulsive_force(rel, use_ccw) + f_att_cell
        return eval_at

    def _make_heatmap_eval(self, xy: np.ndarray, use_ccw: bool):
        """Closure: vectorised repulsion magnitude over a (G, 2) cell grid.

        Computes ``|f_rep|`` at every grid point in one numpy pass — the
        whole (cells × LiDAR-points) tensor is built and reduced at once.
        Cost is roughly O(G·N); for 50×40 cells and 50 LiDAR points that's
        100 k operations per frame, no Python loop.
        """
        gain = self.F_REPULSE_GAIN
        rng = self.F_REPULSE_RANGE
        rmin = self.F_REPULSE_RMIN
        alpha = math.radians(self.VORTEX_ALPHA_DEG)
        ca, sa = math.cos(alpha), math.sin(alpha)

        def eval_grid(cells: np.ndarray) -> np.ndarray:
            if xy.shape[0] == 0:
                return np.zeros(cells.shape[0], dtype=np.float64)
            # delta[g, l] = cells[g] − xy[l]: vector from each LiDAR point
            # to each grid cell (so "away from the obstacle" = +delta direction).
            delta = cells[:, None, :] - xy[None, :, :]              # (G, N, 2)
            r = np.hypot(delta[..., 0], delta[..., 1])              # (G, N)
            mask = (r > 1e-3) & (r < rng)
            if not mask.any():
                return np.zeros(cells.shape[0], dtype=np.float64)
            r_safe = np.where(mask, r, 1.0)
            radial = delta / r_safe[..., None]                      # already "away" direction
            if use_ccw:
                tangent = np.stack([-radial[..., 1],  radial[..., 0]], axis=-1)
            else:
                tangent = np.stack([ radial[..., 1], -radial[..., 0]], axis=-1)
            r_eff = np.maximum(r_safe, rmin)
            strength = gain * (1.0 / r_safe - 1.0 / rng) / (r_eff * r_eff)
            strength = np.where(mask, strength, 0.0)                # zero out out-of-range pairs
            direction = ca * radial + sa * tangent
            f = np.sum(strength[..., None] * direction, axis=1)     # (G, 2)
            return np.hypot(f[:, 0], f[:, 1])
        return eval_grid


def main(args=None) -> None:
    run(ObstacleNav)
