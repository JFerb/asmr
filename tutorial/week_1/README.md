# Week 1 — ROS 2 Basics, Control, and Communication Patterns

## Overview

This week introduces ROS 2 through two hands-on exercises and a control theory notebook.
You will go from observing a running robot system to writing your own ROS 2 package from scratch.

> **Note:** Week 2 (28.4) is cancelled. You have two weeks to complete both exercises.

## Exercises

### Part I — Go1 Quadruped (`exercise_ros2.pdf`, Tasks 1–3)

You launch the Unitree Go1 quadruped in simulation, explore its ROS 2 node graph, and interact with the robot via an action server. No node-writing required — the focus is on understanding how a real ROS 2 system is structured.

What you will do:
- Launch the simulation and visualise the robot in RViz
- Inspect the node graph with `rqt_graph` and `ros2` CLI tools
- Command sitting/standing poses through the `go1_control` action server
- Tune PD gains and observe the effect on joint tracking

### Part II — Turtle Star (`exercise_ros2.pdf`, Tasks 4–7)

You write a complete Python ROS 2 package called `turtle_star` that draws a five-pointed star in Turtlesim. This is your first node-writing exercise and covers all four ROS 2 communication patterns.

What you will implement:
- A **publisher** node that drives the turtle along a star path
- A **service client** for pen colour/width control and teleport
- An **action client** for `rotate_absolute`
- A **launch file** that starts everything with one command

### Notebook — PID Control (`exercise.ipynb`)

A simulation of a 2D lane-following car. You implement controllers in increasing order of sophistication: bang-bang → P → PD → PID. Work through each cell in order; the notebook is self-contained and takes roughly 60 minutes.

## Contents

| File / Folder | Description |
|---|---|
| `exercise_ros2.pdf` | ROS 2 exercise sheet (Parts I and II) |
| `exercise.ipynb` | PID control notebook |
| `utils.py` | Helper functions used by the notebook |
| `go1-packages.zip` | Pre-built Go1 ROS 2 packages — extract into your workspace |
| `ros2-101.md` | ROS 2 Jazzy best practices reference |
| `slides.pdf` | Lecture slides for this week |

## Setup

### JupyterHub (recommended)

Select the appropriate image when starting your server — no further setup needed:

- **ROS 2 exercise (Parts I & II):** choose the ROS 2 image
- **Control notebook:** choose the Data Science / ML image

### Local / VM

Extract the Go1 packages into your ROS 2 workspace and build:

```bash
unzip go1-packages.zip -d ~/ros2/asmr_ws/src/
cd ~/ros2/asmr_ws
colcon build --symlink-install --packages-select go1_description
source install/setup.bash
```

For the notebook, activate the `asmr` conda environment from Week 0:

```bash
conda activate asmr
jupyter notebook exercise.ipynb
```

## Learning Objectives

- Navigate a running ROS 2 system using CLI tools and `rqt_graph`
- Understand the four communication patterns: topics, services, actions, parameters
- Write a complete Python ROS 2 package with a launch file
- Implement and compare bang-bang, P, PD, and PID controllers on a simulated robot
