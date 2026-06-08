# Week 2 — Robot Body and Blind Locomotion

## Overview

Before a robot can perceive or reason, it needs a body. This week you build a differential-drive mobile robot from scratch using URDF, give it a valid coordinate frame tree, and drive it in Gazebo. The robot you create here is the platform you will extend for the next few weeks — adding sensors in Week 3 and navigating a maze in MiniLab 1.

The session focuses on the **Reason** phase of the PRA loop: a robot that has no model of itself cannot situate its actions in space. Odometry is its first self-sense — it tracks how far it has moved based on wheel rotations alone, with no external reference.

## Exercise

The exercise sheet (`exercise_ros2.pdf`) guides you through a 9-task build. You create three ROS 2 packages from scratch and assemble them step by step:

| Task | Topic |
|------|-------|
| 1 | Set up the workspace — three packages, directory layout, first build |
| 2 | Describe the chassis — box link with visual, collision, and inertial |
| 3 | Add the drive wheels — cylinder links, continuous joints, axis orientation |
| 4 | Add the caster — sphere link, fixed joint, ground-contact geometry |
| 5 | Visualise in RViz — launch file, GUI-based display configuration, save config |
| 6 | Inspect the TF tree — `view_frames`, kinematic chain, frame roles |
| 7 | Prepare the Gazebo simulation files — plugins, world SDF, bridge config |
| 8 | Launch the Gazebo simulation — bringup launch file, odometry in RViz |
| 9 | Drive and observe — open-loop square trajectory, model error experiments |

## Contents

| File | Description |
|------|-------------|
| `exercise_ros2.pdf` | Step-by-step build exercise (9 tasks) |
| `slides.pdf` | Session slides: REP 103, homogeneous transforms, URDF, TF |

## Snippets

The `snippets/` folder contains starter files you will copy into your workspace:

| File | Purpose |
|------|---------|
| `urdf_reference.urdf.xacro` | Syntax reference — box, cylinder, sphere links and continuous/fixed joints with xacro properties and inertia formulas |
| `robot.gazebo` | Gazebo plugin file — diff-drive block provided, complete the TODO items |
| `bridge.yaml` | Bridge config — `/cmd_vel` entry provided, complete the TODO topics |
| `my_world.sdf` | Gazebo world file — copy as-is, no edits needed |
| `robot_vis.launch.py` | Visualisation launch file skeleton — complete the TODO items |

## Learning Objectives

- Describe a robot body in URDF/Xacro: links, joints, visual, collision, and inertial sub-elements
- Explain reference frames (REP 103), roll-pitch-yaw, and homogeneous transformation matrices
- Read and interpret a TF tree using `tf2_tools view_frames`
- Configure RViz displays and save a reusable configuration
- Spawn a robot in Gazebo and drive it with `/cmd_vel`
- Observe how model parameter errors (wheel separation, friction) affect open-loop trajectory accuracy
- Distinguish proprioception (odometry) from exteroception — the robot knows where it *thinks* it is, but cannot sense the world around it
