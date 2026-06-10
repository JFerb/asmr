# Week 6 — Forward and Inverse Kinematics

## Overview

The robot platform switches from wheels to an arm. This week you formalise the coordinate frame intuition from Week 2 into homogeneous transformation matrices, and use them to solve forward and inverse kinematics for a 2-link planar arm. You then apply the same ideas to a real 6-DOF arm (UR3e) in simulation.

This is the **Reason** phase again — now with a manipulator. The FK/IK functions you implement in the notebook are the direct input to MiniLab 2.

## Exercises

### Notebook — FK/IK (`exercise.ipynb`)

A 2-link planar arm with interactive visualisations. Work through the exercises in order; each builds on the previous one.

What you will implement (in the `TwoLinkArm` class):

- Homogeneous transform `ht2d(theta, tx, ty)` and point transformation
- Forward kinematics: `forward_kinematics(theta) -> (x, y)` where `theta = [theta1, theta2]`
- Workspace visualisation: scatter all reachable $(x, y)$ over $\theta \in [-\pi, \pi]$
- Geometric inverse kinematics: `ik_geometric(x, y, elbow_up=True)` — both elbow-up and elbow-down solutions
- Jacobian matrix: 4 partial derivatives of FK with respect to joint angles
- Iterative Jacobian IK: converge to a target from an initial joint configuration
- Singularity analysis: heatmap of $\det(J)$ over joint space

### ROS 2 — UR3e Arm Exploration (`exercise_ros.pdf`)

An exploration exercise — no node-writing. You launch a UR3e arm in Gazebo with MoveIt and inspect the system:

- Survey the node graph and identify who publishes `/joint_states`
- Read the TF tree with `tf2_tools view_frames` and count frames from `base_link` to `tool0`
- Use the MoveIt interactive marker to plan and execute trajectories; observe multiple IK solutions
- Send manual joint commands and observe limit enforcement

The UR3e packages are in `ur3e-packages/` — copy into your workspace.

## Contents

| File | Description |
|------|-------------|
| `exercise.ipynb` | FK/IK notebook — 2-link planar arm with interactive widgets |
| `exercise_ros.pdf` | UR3e exploration exercise (3 tasks) |
| `ur3e-packages/` | UR3e workspace setup: wrapper package, `.repos` manifest, and Jazzy compatibility patch — full setup procedure is in `exercise_ros.pdf` |
| `slides.pdf` | Session slides: homogeneous transforms, FK/IK, Jacobian, singularities, MoveIt |

## Learning Objectives

- Build a homogeneous transformation matrix and compose transforms by matrix multiplication
- Compute forward kinematics for a 2-link planar arm using the kinematic chain
- Derive and implement closed-form geometric inverse kinematics (law of cosines + arctan2)
- Compute the Jacobian and use pseudoinverse-based IK to approach a target iteratively
- Explain what a kinematic singularity is and where it occurs in joint space
- Navigate a live UR3e system: node graph, joint states, TF tree, MoveIt planning
