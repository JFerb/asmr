# my_robot_control

Motion-control nodes for MiniLab 1.

- **velocity_controller** — hosts the `set_velocity` action server and is the
  sole publisher of `cmd_vel` during the lab. On each accepted goal it drives
  `cmd_vel` at 10 Hz until a newer goal preempts it or the client cancels.
- **move_square** — standalone week-3 open-loop demo that publishes `cmd_vel`
  directly to drive a square (illustrating drift). Not part of the MiniLab 1
  stack; do not run it alongside `velocity_controller`.

`VelocityState` is kept rclpy-free so its transitions are unit-tested directly.
