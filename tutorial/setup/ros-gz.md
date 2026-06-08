# ROS 2 and Gazebo

This document describes the software installation path for ROS 2 and Gazebo. It assumes the workstation environment is already available.

## Overview

ROS 2 and Gazebo are software layers separate from the host operating system. Complete workstation setup first, then install ROS 2 and Gazebo.

## Prerequisites

- Ubuntu 24.04 LTS or Ubuntu 24.04 within WSL.
- A user account with `sudo` privileges.
- Internet access.
- Basic familiarity with the Linux terminal.

## Installation resources

Follow the official guides rather than duplicating installation instructions:

- ROS 2 Jazzy installation: https://docs.ros.org/en/jazzy/Installation.html
- Gazebo Harmonic ROS integration: https://gazebosim.org/docs/harmonic/ros_installation/

## Recommended workflow

1. Complete workstation setup (`windows.md` or `vm.md`).
2. Install ROS 2 Jazzy using the official ROS 2 guide. The `ros-jazzy-desktop` variant is recommended (includes RViz and common tools).
3. Install the Gazebo Harmonic ROS integration using the official Gazebo guide. Note that Gazebo is **not** included in the standard ROS 2 desktop install — it must be installed separately.
4. Source the ROS 2 setup file. Add this line to your `~/.bashrc` so it runs automatically in every new terminal:
   ```bash
   source /opt/ros/jazzy/setup.bash
   ```
5. Verify the installation:
   ```bash
   ros2 --version
   gz sim --version
   ```
   Both commands should print a version number without errors.
