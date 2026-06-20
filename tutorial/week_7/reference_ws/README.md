# MiniLab 2 — Reference Workspace

The starter workspace for MiniLab 2. Build your solution **here** and submit this
tree (see the task sheet for submission rules).

**ROS 2:** Jazzy · **Simulator:** Gazebo Harmonic

---

## What this workspace contains

This is a *reference package*: it provides the parts you should not have to
rebuild, and leaves the graded work for you to create. See Figure 1 ("the
submitted workspace") in the task sheet for the full map.

### Provided (do not rewrite)
| Package | What it gives you |
|---|---|
| `asmr_arm_description` | the two-link arm xacro (`arm.urdf.xacro`); the **ros2_control hardware-interface template** (`arm.ros2_control.xacro`) and the **controller config template** (`controllers_pedestal.yaml`) — you complete both; the pedestal geometry (`arm_dimensions_pedestal.yaml`); and the Task-1 world (`push_block_world.sdf`) |
| `asmr_arm_interfaces` | the pinned service/action contract: `ComputeFK.srv`, `ComputeIK.srv`, `ExecuteTrajectory.action` |
| `my_robot_description` | a ready-to-use reference mobile base (arm **not** mounted) + the Task-2 world (`corridor_world.sdf`) |
| `my_robot_bringup` | bridge + RViz config and helper launches (you write the scenario launch) |
| `my_robot_control` | a velocity smoother for the base |
| `my_robot_perception` | LiDAR fusion + scan/odom helper utilities |

### You create
- **Packages:** `asmr_arm_control` (kinematics + trajectory servers),
  `asmr_arm_mission` (push mission), `asmr_arm_bringup` (Task-1 launch + bridge)
  for Task 1; `my_robot_mission` (corridor mission) for Task 2. Create them with
  `ros2 pkg create`.
- **Configs you fill in:** the gains and interfaces in `controllers_pedestal.yaml`
  (Task 1); the Task-2 `arm_dimensions.yaml` and `controllers_mobile.yaml`,
  modelled on the provided pedestal versions.
- **Launch files:** `push_block_world.launch.py`, `corridor_world.launch.py`.

You may also build on **your own** MiniLab 1 robot instead of the provided base.

---

## Build

From the workspace root:

```bash
source /opt/ros/jazzy/setup.bash      # if not already in your shell
colcon build
source install/setup.bash             # under zsh: source install/setup.zsh
```

The provided packages build out of the box. Your own packages build once you add
them.

---

## Run

The exact launch/run commands are part of what you build — see the task sheet.
Once your packages and launch files exist, the pattern is:

```bash
# Task 1 (after you write asmr_arm_bringup/launch/push_block_world.launch.py)
ros2 launch asmr_arm_bringup push_block_world.launch.py
ros2 run asmr_arm_mission push_block_mission

# Task 2 (after you write my_robot_bringup/launch/corridor_world.launch.py)
ros2 launch my_robot_bringup corridor_world.launch.py
ros2 run my_robot_mission corridor_mission
```

---

The task sheet (`minilab_2.pdf`) is the authoritative description of what to
build and how it is graded. Start there.
