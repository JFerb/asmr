# Week 7 — MiniLab 2: Arm Kinematics & Mobile Manipulation

## Overview

MiniLab 2 is a pure **ROS 2** exercise. You give your MiniLab 1 robot an *arm* — and
with it, the ability to interact with the world. Two sequential tasks build on each
other:

- **Task 1 — Build & tune the arm control stack (25 pts).** On a fixed pedestal arm:
  implement the kinematics services (FK/IK ported from your Week 6 notebook),
  complete and tune the closed-loop PID controller, build the `ExecuteTrajectory`
  action server that designs a smooth trajectory to a target, and prove it with a
  push-block mission.
- **Task 2 — Run the mission (25 pts).** Mount that arm on your mobile robot, drive a
  straight corridor with LiDAR, push a hinged door open with the arm, and enter the
  room beyond — structured as a behaviour-based mission protocol.

**ROS 2:** Jazzy · **Simulator:** Gazebo Harmonic
**Issued:** 19.06.2026 · **Due:** 01.07.2026, 23:59 (submit to LearnWeb)

## Tasks

The full task descriptions, interface specifications, acceptance criteria, and
submission format are in `minilab_2.pdf`. **Read it carefully before starting.**

| Task | Subtask | Points |
|------|---------|--------|
| 1 | Kinematics server (FK/IK services) | 5 |
| 1 | Tune the controller | 5 |
| 1 | Trajectory action server | 10 |
| 1 | Push-block mission + launch | 5 |
| 2 | Mount the arm | 5 |
| 2 | Bring up the system | 5 |
| 2 | Drive the corridor | 5 |
| 2 | Open the door & enter the room | 10 |

**Total: 50 pts. Pass at 25 pts.**

## Getting started

Build your solution in the provided starter workspace (`reference_ws/`). It provides
the parts you should not have to rebuild — robot/arm descriptions, the worlds, the
pinned service/action interfaces, perception helpers, and the controller/hardware
**templates** you complete — and leaves the graded packages for you to create. Its
own `README.md` lists exactly what is provided vs what you build.

```bash
cd reference_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

Then work through `minilab_2.pdf` task by task. You may build on your own MiniLab 1
robot or the provided reference robot.

## Contents

| File | Description |
|------|-------------|
| `minilab_2.pdf` | Full task description, interface specs, acceptance criteria, submission format |
| `reference_ws/` | Starter ROS 2 workspace — build your solution here |
| `slides.pdf` | Session slides: the control stack, Perceive–Reason–Act, the mission protocol |

## Learning Objectives

- Transfer your Week 6 FK/IK into live ROS 2 services with proper service conventions
- Configure and tune a `ros2_control` PID controller (hardware interfaces + gains)
- Implement a ROS 2 action server: trajectory design, the full goal/feedback/result/cancel contract, and executors / callback groups
- Compose sensor-responsive behaviours into a reactive mission (behaviour-based control / a finite state machine)
- Mount and command an arm on a mobile base; LiDAR-driven corridor navigation and arm targeting
