# Week 3 — Exteroception: LiDAR Integration

## Overview

The robot from Week 2 can move and report its own position — but it is blind to the world around it. This week you give it eyes. You add a LiDAR sensor to your existing robot, bridge the scan data into ROS 2, and learn to read and interpret it. By the end of the session your robot perceives the environment — the last piece before MiniLab 1.

This is the **Perceive** phase: odometry tells the robot where it *thinks* it is; LiDAR tells it what is *in front of it*. Both are needed to close the reactive navigation loop.

## Exercise

The exercise sheet (`exercise_ros2.pdf`) extends your Week 2 workspace with a LiDAR sensor. You work through six tasks:

- **Task 1:** Add a `lidar_link` to the URDF and configure the Gazebo GPU LiDAR sensor plugin
- **Task 2:** Add the `/scan` bridge entry to `bridge.yaml` and verify the topic is live
- **Task 3:** Visualise the scan in RViz; explore the topic graph with `rqt_graph`
- **Task 4:** Inspect the `LaserScan` message; derive the forward-facing index; plot live with `rqt_plot`
- **Task 5:** Place a wall in the simulation and compare odometry vs LiDAR over a 1 m drive
- **Task 6:** Write a ROS 2 node that transforms the nearest obstacle position from `lidar_link` to `base_link` using TF2

No new packages are required — you modify the robot you built in Week 2.

## Contents

| File | Description |
|------|-------------|
| `exercise_ros2.pdf` | LiDAR integration exercise (6 tasks) |
| `slides.pdf` | Session slides: proprioception vs exteroception, LiDAR principles, sensor models |

## Learning Objectives

- Distinguish proprioceptive sensors (odometry, IMU) from exteroceptive sensors (LiDAR, camera)
- Explain how a 2D LiDAR works: rotating laser, distance per angle, output as a ring of distances
- Add a Gazebo sensor plugin to a URDF and bridge the topic to ROS 2
- Read and interpret `sensor_msgs/LaserScan`: the `ranges` array, `angle_min`, `angle_max`, `angle_increment`
- Identify systematic error (calibration offset) vs random error (noise)
- Use TF2 to transform a point between coordinate frames in Python code
