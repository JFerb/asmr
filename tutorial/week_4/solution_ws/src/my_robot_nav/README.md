# my_robot_nav

Reactive navigation. Commands motion via the `SetVelocity` action client in
`ReactiveNavBase` and stops on the latched `goal_reached` signal.

- **obstacle_nav** — potential-field avoidance: repulsion from `scan_points`
  plus a constant goal-directed attractive force toward `goal_point`. Optional
  RViz field/heatmap visualisation (`visuals.py`).

Run inside the robot namespace (see the workspace README):
```bash
ros2 run my_robot_nav obstacle_nav --ros-args -r __ns:=/my_robot -r odom:=/odom
```
