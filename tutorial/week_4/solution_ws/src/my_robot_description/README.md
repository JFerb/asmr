# my_robot_description

URDF/xacro model of the differential-drive robot used throughout MiniLab 1.

- `urdf/my_robot.urdf.xacro` — robot model (base, wheels, lidar_link).
- `urdf/robot.gazebo` — Gazebo plugins (diff-drive, lidar, odometry).

Consumed by `my_robot_bringup` launch files via `robot_state_publisher`
(`xacro` expands the model into `/robot_description`).
