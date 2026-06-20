# my_robot_interfaces

Action and message interfaces for the ASMR mobile robot.

- `action/SetVelocity.action` — request a constant `(linear_x, angular_z)`
  velocity. The controller publishes `cmd_vel` at its tick rate using these
  values until a new goal preempts this one or the client cancels. Feedback
  reports the current commanded velocity; the result reports whether the robot
  was stopped.

This is the motion-command contract between `my_robot_nav` (clients) and
`my_robot_control`'s `velocity_controller` (server).
