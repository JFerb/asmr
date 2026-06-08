# Week 7 — MiniLab 2: Localisation and Arm Trajectory

## Overview

MiniLab 2 has two independent tracks, each worth separate points. You choose the order and can work on them in parallel.

The **Jupyter track** asks: *where is the robot?* You implement probabilistic localisation from scratch — first on a 1D discrete grid (Markov), then in a 2D continuous world with landmarks (Monte Carlo). The **ROS 2 track** applies the FK/IK from Week 6 to a real arm in simulation: you build a full kinematic service stack and command the arm through a trajectory that pushes a box.

**Deadline:** Submit before Week 9.

## Tasks

The full task descriptions, interface specifications, acceptance criteria, and submission format are in `minilab_2.pdf`. Read it carefully before starting.

| Track | Task | Points |
|-------|------|--------|
| Jupyter | Markov localisation: implement `predict()` and `update()` in an `Agent` class; 9-step belief evolution plot | 10 pts |
| Jupyter | Monte Carlo localisation: implement `move()`, `sense()`, `resample()`, `redistribute()` in a particle filter; 30-step convergence panel | 10 pts |
| ROS 2 | Kinematics node: define `ComputeFK.srv` + `ComputeIK.srv` and implement the service server (port from Week 6 notebook) | 5 pts |
| ROS 2 | Trajectory node: define `ExecuteTrajectory.action` and implement the action server with linear joint interpolation and feedback | 15 pts |
| ROS 2 | Push client: send a home→approach→push trajectory that visibly displaces the box in Gazebo | 10 pts |

**Total: 50 pts. Pass at 25 pts.**

## Getting Started

Open `exercise_localisation.ipynb` for the Jupyter track and work through both parts.

For the ROS 2 track, extract `asmr_arm_ws.zip` into your workspace. It contains `asmr_arm_description` — the provided arm URDF, Gazebo world (`push_world.sdf`), and launch file. You create `asmr_arm_interfaces` and `asmr_arm_control` from scratch following the task sheet.

## Contents

| File | Description |
|------|-------------|
| `exercise_localisation.ipynb` | Localisation notebook — Markov and Monte Carlo |
| `minilab_2.pdf` | Full task description, interface specs, acceptance criteria, submission format |
| `asmr_arm_ws.zip` | Provided arm packages — extract into your ROS 2 workspace |
| `slides.pdf` | Session slides: Bayesian filter, predict/update, Markov vs particle filter, arm demo |

## Learning Objectives

- Implement the Bayes filter predict and update steps on a discrete 1D belief
- Implement a particle filter: propagate, weight, resample, and redistribute particles
- Define custom ROS 2 service and action interfaces (`.srv`, `.action`)
- Implement a ROS 2 action server with a `MultiThreadedExecutor` and service clients
- Command an arm through a trajectory using IK-computed joint angles with smooth interpolation
