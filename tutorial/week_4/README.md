# Week 4 — MiniLab 1: Reactive Navigation

## Overview

MiniLab 1 is the first integration project of the semester. Using the robot you built in Weeks 2–3, you implement a reactive ROS 2 node that navigates a Gazebo obstacle world using only LiDAR (and optionally odometry) — no map, no path planner, no memory. You close the Perceive–Reason–Act loop yourself.

The minilab is built around one task: build `my_robot_nav` with a reactive `obstacle_nav.py`, plus the simulation launch file. The algorithm is deliberately open — a potential field, a sector-based avoid-and-steer, or any reactive approach. There is no prescribed solution; only correct ROS 2 integration and a robot that reaches the goal through the obstacle parcour.

## Task

The full task description, world overview, acceptance criteria, and submission format are in `minilab_1.pdf`. Read it carefully before starting.

**One graded task (40 pts total, pass at 20 pts):**

| Task | Description | Points |
|------|-------------|--------|
| 1 | Build `my_robot_nav` (with `obstacle_nav.py`), write `sim.launch.py` in `my_robot_bringup`, and implement reactive obstacle navigation using the provided `SetVelocity` action client and `goal_checker_node` | 40 pts |

**Deadline:** 10.06.2026, 23:59 (before Week 7).

## Getting Started

Copy `reference_ws/src/` into your ROS 2 workspace. It contains:

- the obstacle world SDF (`obstacle_world.sdf`) — drop it into your existing `my_robot_bringup/worlds/`;
- the `my_robot_perception` package (sensor helpers, `goal_checker_node`, and the opt-in `scan_to_pointcloud_node`);
- the `my_robot_interfaces` package (defines the `SetVelocity` action);
- `velocity_controller_node` added to your existing `my_robot_control` package.

Your Week 2–3 robot packages (`my_robot_description`, `my_robot_bringup`, `my_robot_control`) must already be in the workspace (alternatively you can use the provided packages too). You add a new launch file (`sim.launch.py`) to `my_robot_bringup`, create the `my_robot_nav` package, and implement the reactive navigation logic in `obstacle_nav.py`.

## Contents

| File | Description |
|------|-------------|
| `minilab_1.pdf` | Full task description, acceptance criteria, submission format. |
| `reference_ws/` | Workspace with `my_robot_perception`, `my_robot_interfaces`, `velocity_controller_node`, and the obstacle world. |
| `slides.pdf` | Session slides: reactive control, ROS 2 communication recap, algorithm options |

## Learning Objectives

- Implement a reactive controller that subscribes to LiDAR data and drives the robot through a `SetVelocity` action client
- Apply the Perceive–Reason–Act loop in code (sensor data → decision logic → action goal → motion command, with `/goal_reached` as a higher-level event)
- Organise a multi-package ROS 2 system with a launch file
