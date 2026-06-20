# my_robot_bringup

Launch files, worlds, bridge, and RViz config for MiniLab 1.

## Launch
- **sim.launch.py** — full simulation: Gazebo + bridge + robot spawn + the
  `my_robot`-namespaced first-party nodes + RViz. Arg `world:=obstacle`.
- **robot_sim.launch.py** — robot in `wall_world` for sensor bring-up (no
  first-party nodes).
- **robot_vis.launch.py** — RViz + `joint_state_publisher_gui`, no Gazebo.

## Config
- `config/bridge.yaml` — ros_gz bridge: pins global `/cmd_vel`, `/scan`,
  `/odom`, `/clock`, `/joint_states`, `/tf`.
- `config/my_robot.rviz` — RViz layout (internal topics under `/my_robot/`).

## Worlds
`obstacle_world` (graded), `wall_world` (sensor bring-up), `empty_world`
(blank, for student experiments — unused by the solution).
