# my_robot_perception

Perception nodes and pure helpers for MiniLab 1.

- **goal_checker** — subscribes `odom`, publishes latched `goal_reached`,
  `goal_point`, and an RViz `goal_marker`. Params: `goal_x`, `goal_y`,
  `goal_threshold`.
- **scan_to_pointcloud** — subscribes `scan`, publishes `scan_points`
  (PointCloud2 in `base_link`). Opt-in; only started in the obstacle world.
- `odom_utils`, `scan_utils` — pure, unit-tested geometry helpers
  (position/yaw extraction, sector-min range, PointCloud2 → xy).
