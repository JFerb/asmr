# turtle_star

A ROS 2 Python package that commands a turtlesim turtle to draw a five-pointed star. It demonstrates all four ROS 2 communication patterns in one node: topics (velocity commands), services (pen control, teleport), and actions (rotation).

## Prerequisites

- ROS 2 Jazzy
- turtlesim: `sudo apt install ros-jazzy-turtlesim`

## Setup

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone <this-repo>          # or copy the turtle_star folder here
cd ~/ros2_ws
colcon build --symlink-install --packages-select turtle_star
source install/setup.bash
```

## Run

```bash
ros2 launch turtle_star star.launch.py
```

This starts `turtlesim_node` and `star_node` together. The turtle draws the star and then moves out of the way.
