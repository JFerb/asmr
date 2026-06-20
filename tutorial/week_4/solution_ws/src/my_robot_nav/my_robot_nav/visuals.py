"""Debug-only RViz visualization for the potential-field obstacle nav.

Publishes two debug topics in frame ``base_link``:

  - ``/obstacle_nav/field`` (MarkerArray): three thick arrows from the
    robot origin — f_rep (red), f_att (green), f_total (blue) — plus a
    9 × 5 faded grey grid of small arrows ahead of the robot showing the
    full field at offset positions.
  - ``/obstacle_nav/repulsion_heatmap`` (OccupancyGrid): a 5 m × 4 m
    heatmap of repulsion-force magnitude around the robot. Use RViz's
    Map display with the "costmap" colour scheme.

Not part of the navigation pipeline. Disable by setting ``VIZ_ENABLED =
False`` in obstacle_nav.py.
"""
from typing import Callable, Optional

from builtin_interfaces.msg import Time
from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid
import numpy as np
from std_msgs.msg import ColorRGBA, Header
from visualization_msgs.msg import Marker, MarkerArray


FRAME              = 'base_link'
ARROW_TOPIC        = 'obstacle_nav/field'
HEATMAP_TOPIC      = 'obstacle_nav/repulsion_heatmap'

ARROW_MAX_LEN      = 0.6     # m; clamp for the three big origin arrows
GRID_MAX_LEN       = 0.25    # m; clamp for the grid arrows
GRID_X             = np.linspace(0.2, 2.0, 9)
GRID_Y             = np.linspace(-1.5, 1.5, 5)

# Heatmap: covers x ∈ [-1, 4] m forward, y ∈ [-2, 2] m sideways in base_link.
HEATMAP_RES        = 0.1     # m per cell
HEATMAP_ORIGIN_X   = -1.0    # m; lower-left corner of the heatmap rect
HEATMAP_ORIGIN_Y   = -2.0
HEATMAP_WIDTH_M    = 5.0     # m extent in x
HEATMAP_HEIGHT_M   = 4.0     # m extent in y
HEATMAP_MAX_MAG    = 10.0    # repulsion magnitude that maps to 100 (saturated red)

COLOR_REP          = (1.0, 0.25, 0.25, 1.0)
COLOR_ATT          = (0.25, 0.85, 0.35, 1.0)
COLOR_TOTAL        = (0.30, 0.50, 1.00, 1.0)
COLOR_GRID         = (0.55, 0.55, 0.55, 0.55)


class PotentialFieldViz:
    """Publishes three live arrows + optional field grid + optional heatmap."""

    def __init__(self, node) -> None:
        self._node = node
        self._arrow_pub = node.create_publisher(MarkerArray, ARROW_TOPIC, 1)
        self._heatmap_pub = node.create_publisher(OccupancyGrid, HEATMAP_TOPIC, 1)
        self._heatmap_cells: Optional[np.ndarray] = None
        self._heatmap_w = 0
        self._heatmap_h = 0

    def publish(
        self,
        f_rep: np.ndarray,
        f_att: np.ndarray,
        f_total: np.ndarray,
        grid_eval: Optional[Callable[[float, float], np.ndarray]] = None,
        heatmap_eval: Optional[Callable[[np.ndarray], np.ndarray]] = None,
    ) -> None:
        # Zero stamp → RViz uses the latest available TF for base_link.
        # This avoids "transform at exact time not available" drops when the
        # Fixed Frame is odom (the odom→base_link TF is published a few ms
        # behind real time).
        stamp = Time()
        msg = MarkerArray()

        msg.markers.append(self._arrow('rep',   0, 0.0, 0.0, f_rep,   COLOR_REP,   ARROW_MAX_LEN, stamp, shaft=0.04, head_d=0.09, head_l=0.10))
        msg.markers.append(self._arrow('att',   1, 0.0, 0.0, f_att,   COLOR_ATT,   ARROW_MAX_LEN, stamp, shaft=0.04, head_d=0.09, head_l=0.10))
        msg.markers.append(self._arrow('total', 2, 0.0, 0.0, f_total, COLOR_TOTAL, ARROW_MAX_LEN, stamp, shaft=0.04, head_d=0.09, head_l=0.10))

        if grid_eval is not None:
            i = 3
            for gx in GRID_X:
                for gy in GRID_Y:
                    f = grid_eval(float(gx), float(gy))
                    msg.markers.append(self._arrow(
                        'grid', i, float(gx), float(gy), f, COLOR_GRID,
                        GRID_MAX_LEN, stamp,
                        shaft=0.012, head_d=0.03, head_l=0.04,
                    ))
                    i += 1

        self._arrow_pub.publish(msg)

        if heatmap_eval is not None:
            self._publish_heatmap(stamp, heatmap_eval)

    def _publish_heatmap(
        self,
        stamp,
        heatmap_eval: Callable[[np.ndarray], np.ndarray],
    ) -> None:
        cells, w, h = self._heatmap_grid()
        magnitudes = heatmap_eval(cells)            # (w*h,) float
        clipped = np.clip(magnitudes / HEATMAP_MAX_MAG, 0.0, 1.0)
        data = (clipped * 100.0).astype(np.int8)    # OccupancyGrid wants int8 in [-1, 100]

        msg = OccupancyGrid()
        msg.header.frame_id = FRAME
        msg.header.stamp = stamp
        msg.info.resolution = HEATMAP_RES
        msg.info.width = w
        msg.info.height = h
        msg.info.origin.position.x = HEATMAP_ORIGIN_X
        msg.info.origin.position.y = HEATMAP_ORIGIN_Y
        msg.info.origin.position.z = 0.0
        msg.info.origin.orientation.w = 1.0
        msg.data = data.tolist()
        self._heatmap_pub.publish(msg)

    def _heatmap_grid(self):
        """(N, 2) array of cell-centre xy in base_link, plus width/height."""
        if self._heatmap_cells is None:
            w = int(round(HEATMAP_WIDTH_M / HEATMAP_RES))
            h = int(round(HEATMAP_HEIGHT_M / HEATMAP_RES))
            ix = np.arange(w)
            iy = np.arange(h)
            xs = HEATMAP_ORIGIN_X + (ix + 0.5) * HEATMAP_RES        # (w,)
            ys = HEATMAP_ORIGIN_Y + (iy + 0.5) * HEATMAP_RES        # (h,)
            xx, yy = np.meshgrid(xs, ys)                            # (h, w) each
            self._heatmap_cells = np.column_stack([xx.ravel(), yy.ravel()])
            self._heatmap_w = w
            self._heatmap_h = h
        return self._heatmap_cells, self._heatmap_w, self._heatmap_h

    def _arrow(self, ns, marker_id, x, y, vec, color, max_len, stamp,
               shaft, head_d, head_l):
        m = Marker()
        m.header = Header(frame_id=FRAME, stamp=stamp)
        m.ns = ns
        m.id = marker_id
        m.type = Marker.ARROW
        m.action = Marker.ADD

        magnitude = float(np.hypot(vec[0], vec[1]))
        if magnitude < 1e-6:
            length = 0.0
            ux, uy = 0.0, 0.0
        else:
            length = min(magnitude, max_len)
            ux, uy = float(vec[0] / magnitude), float(vec[1] / magnitude)

        m.points = [
            Point(x=float(x),                y=float(y),                z=0.05),
            Point(x=float(x + ux * length),  y=float(y + uy * length),  z=0.05),
        ]
        m.scale.x = shaft
        m.scale.y = head_d
        m.scale.z = head_l
        m.color = ColorRGBA(r=color[0], g=color[1], b=color[2], a=color[3])
        return m
