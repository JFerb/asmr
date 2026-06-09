# my_robot_ws

ROS 2 workspace for the ASMR course robot. Build artifacts (`build/`, `install/`, `log/`) are local only.

## Build & run

```bash
cd my_robot_ws
colcon build --symlink-install
source install/setup.bash
```

Start the obstacle-course simulation (Gazebo, bridges, RViz, goal checker, velocity controller):

```bash
ros2 launch my_robot_bringup sim.launch.py
```

Start the navigator in a second terminal:

```bash
ros2 run my_robot_nav obstacle_nav
```

## How navigation works

Navigation is **reactive**: no map, no planner. The robot reads sensors, picks a behavior, and sends velocity commands in a loop.

```
/scan, /odom  →  obstacle_nav  →  /set_velocity (action)  →  velocity_controller  →  /cmd_vel  →  Gazebo
                      ↑
              /goal_point, /goal_reached
                      ↑
               goal_checker_node
```

1. **Sensors** — Gazebo publishes LiDAR (`/scan`) and wheel odometry (`/odom`) via `ros_gz_bridge`.
2. **Goal** — `goal_checker_node` publishes a latched goal on `/goal_point` and watches `/odom`. When the robot enters a 0.3 m radius around the goal, it latches `/goal_reached` to `true` and also publishes an RViz marker on `/goal_marker`.
3. **Reason** — `obstacle_nav` runs at 10 Hz. Each tick it splits the LiDAR into three sectors (front ±30°, left 30–90°, right −90° to −30°) and applies priority rules:
  - **Safety** — front < 0.3 m → reverse while turning.
  - **Avoidance** — front < 0.6 m → turn toward the side with more space; similar nudges if left or right is tight.
  - **Navigate** — otherwise steer toward the goal using odometry: turn in place if heading error > 0.25 rad, else drive forward.
4. **Act** — chosen `(linear_x, angular_z)` is sent as a `SetVelocity` action goal. `velocity_controller_node` accepts it and publishes that twist on `/cmd_vel` at 10 Hz until a new goal preempts it.
5. **Stop** — when `/goal_reached` becomes `true`, `obstacle_nav` sends `(0, 0)` and stops navigating.

Default goal in `sim.launch.py`: **(9.0, 0.0)** in the `odom` frame.

## Debugging signals in `obstacle_nav`

The navigator does not publish separate debug topics. Instead it logs **state transitions** to the node logger (`ros2 run …` terminal or `ros2 topic echo` on `/rosout`).

### Behavior states

`obstacle_nav` tracks `current_state` and `new_state`. Whenever the behavior changes, it logs one line:

```
<state>: linear_x=<v>, angular_z=<ω>
```


| State             | Meaning                                                              |
| ----------------- | -------------------------------------------------------------------- |
| `Safety`          | Obstacle very close ahead (< 0.3 m); backing up with rotation.       |
| `Avoidance front` | Front blocked (< 0.6 m); turning in place toward the more open side. |
| `Avoidance right` | Right side tight; arc left while moving forward.                     |
| `Avoidance left`  | Left side tight; arc right while moving forward.                     |
| `Turn to goal`    | Path clear; rotating toward the goal bearing.                        |
| `Forward`         | Aligned with goal; driving straight.                                 |


Repeated logs for the same state are suppressed — you only see a line when the robot **switches** behavior. That makes it easy to spot when avoidance kicks in or when the robot returns to goal-seeking.

### Other log messages


| Message                                      | Meaning                                                                             |
| -------------------------------------------- | ----------------------------------------------------------------------------------- |
| `Waiting for odom and lidar services...`     | `/scan` or `/odom` not received yet.                                                |
| `Waiting for goal point...`                  | `/goal_point` not received yet (start `goal_checker_node` or check launch).         |
| `Goal reached: stopping robot`               | `/goal_reached` is `true`; navigator has sent a zero velocity goal.                 |
| `Action server not available: /set_velocity` | `velocity_controller_node` is not running.                                          |
| `Goal rejected`                              | The action server refused the velocity goal (unusual with the provided controller). |


### Tips

- Watch state names to verify the priority order (safety beats avoidance beats goal-seeking).
- If the robot never leaves `Waiting …`, check that `sim.launch.py` is running and bridges are up.
- Compare logged `linear_x` / `angular_z` with `/cmd_vel` to confirm the velocity controller is forwarding commands.

