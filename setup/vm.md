# Virtual Machine

This document covers the workstation setup for running Ubuntu 24.04 in VirtualBox.

## Installation

1. Install VirtualBox from https://www.virtualbox.org/wiki/Downloads.
2. Download the Ubuntu 24.04 LTS desktop ISO from https://ubuntu.com/download/desktop.
3. In VirtualBox, click **New** and create a virtual machine with at least:
   - **RAM**: 4 GB (8 GB recommended for running Gazebo later in the course)
   - **Storage**: 30 GB dynamically allocated
   - **CPU**: 2 cores
   - **Video memory**: 128 MB (set under Display)
4. Attach the Ubuntu ISO as the optical drive and start the VM.
5. Follow the Ubuntu installer to complete the installation.

For additional guidance, use the official Ubuntu VirtualBox tutorial:

https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox

## After installation

Once Ubuntu 24.04 is installed in the VM, install the course software using the following guides:

- `ros-gz.md` for ROS 2 and Gazebo.
- `python.md` for the Python environment.