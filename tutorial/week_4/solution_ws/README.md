# MiniLab 1 — Reference Solution

ROS 2 workspace for the reactive-navigation MiniLab. Build with colcon, then
launch the simulator and run one navigation node.

## Packages
- **my_robot_description** — URDF/xacro of the differential-drive robot.
- **my_robot_interfaces** — `SetVelocity` action (the motion command contract).
- **my_robot_control** — `velocity_controller` (SetVelocity server, sole owner
  of `cmd_vel`) and the standalone `move_square` open-loop demo.
- **my_robot_perception** — `goal_checker` (latches `goal_reached`) and
  `scan_to_pointcloud` (LaserScan → PointCloud2), plus pure odom/scan helpers.
- **my_robot_nav** — `obstacle_nav` (potential-field reactive avoidance),
  commanding via `SetVelocity`.
- **my_robot_bringup** — launch files, worlds, the ros_gz bridge config, RViz.

## Build
```bash
cd week_4/private/solution_pkg
colcon build --symlink-install
source install/setup.bash
```

## Run
The robot's first-party nodes run under the **`my_robot` namespace**. The Gazebo
bridge publishes the sensor/actuator topics at **global** names (`/cmd_vel`,
`/scan`, `/odom`); nodes that talk to the bridge remap their relative name back
onto the global one (see `launch/sim.launch.py`). Internal pipeline topics
(`set_velocity`, `goal_reached`, `goal_point`, `goal_marker`, `scan_points`,
`obstacle_nav/*`) stay namespaced under `/my_robot/`.

```bash
ros2 launch my_robot_bringup sim.launch.py world:=obstacle
```

Then, in a second sourced terminal, start a navigator **in the same namespace**,
remapping the bridge topics it consumes:

```bash
ros2 run my_robot_nav obstacle_nav --ros-args -r __ns:=/my_robot -r odom:=/odom
```

Running nav separately lets you restart your navigation logic without
restarting the simulator.

## Worlds
`obstacle_world` is the graded scenario. `wall_world` is used by
`robot_sim.launch.py` for sensor bring-up. `empty_world.sdf` is a blank world
provided for your own experiments — drop in your own robot or obstacles;
nothing in the solution references it.

## Test
```bash
colcon test --packages-select my_robot_control my_robot_nav my_robot_perception
colcon test-result --verbose
```
Each Python package runs `flake8` + `pep257` style checks (tuned to allow the
aligned-constant tables; import order is enforced) plus unit tests for the pure
helper functions.
