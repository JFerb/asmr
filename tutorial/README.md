# Autonomous Systems and Mobile Robots (ASMR) — Tutorial

## Overview

This repository contains the tutorial material accompanying the ASMR lecture. The tutorial applies concepts from the lecture in hands-on exercises — theory is covered in the lecture first, then practised here.

Each session combines two tracks:

1. **Jupyter / Python** — first-principles algorithms, plotting, and controlled experiments.
2. **ROS 2 / Linux** — system integration, simulation, and practical robot software on Ubuntu.

## Guiding Idea

The tutorial follows the **Perceive–Reason–Act (PRA)** loop introduced in the lecture. Each session advances students along this loop, building on a single evolving robot platform that grows from a bare model into a sensing, reasoning, acting system.

- **Act** — actuation, control, ROS 2 communication
- **Reason** — frames, models, kinematics, localisation
- **Perceive** — sensing, signal interpretation, uncertainty, state estimation

The semester begins with basic control and ROS 2 communication (**Act**), moves to robot modelling and kinematics (**Reason**), introduces sensors and state estimation (**Perceive**), and culminates in two integration projects (MiniLabs) where all three phases come together.

## Topics

- Robot control and actuation
- ROS 2 communication (topics, services, actions)
- Robot modelling (URDF/Xacro, TF)
- Sensors and uncertainty
- Forward and inverse kinematics
- Localisation and state estimation
- System integration (Gazebo, MoveIt)

## Prerequisites

- Basic programming experience
- Basic Linux experience

## Getting Started

**Set up the Python environment:**

```bash
conda env create -f setup/environment.yaml
conda activate asmr
```

For installation options and platform-specific guidance, see [`setup/README.md`](setup/README.md).

## Repository Structure

| Folder | Content |
|--------|---------|
| `week_0/` | Python self-assessment, environment setup, introduction to the PRA loop |
| `week_1/` | ROS 2 basics, all four communication patterns, PID control notebook, Go1 quadruped exercise |
| `week_2/` | Build a differential-drive robot from scratch — URDF, TF tree, Gazebo simulation |
| `week_3/` | Add a LiDAR sensor to the week 2 robot — Gazebo plugin, ROS 2 bridge, RViz |
| `week_4/` | **MiniLab 1** — reactive maze navigation using LiDAR (take-home, 50 pts) |
| `week_6/` | FK/IK notebook for a 2-link planar arm, UR3e arm exploration with MoveIt |
| `week_7/` | **MiniLab 2** — probabilistic localisation notebook + robotic arm kinematics and trajectory (take-home, 50 pts) |
| `week_9/` | Recap — PRA arc map, student MiniLab presentations, future directions |

## Contact

Janosch Bajorath — [j.bajorath@uni-muenster.de](mailto:j.bajorath@uni-muenster.de)

Autonomous Intelligent Systems Group, University of Münster
