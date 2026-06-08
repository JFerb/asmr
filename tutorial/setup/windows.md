# Windows / WSL Setup

This guide describes how to install and configure WSL with Ubuntu 24.04 on a Windows host.

## Install WSL and Ubuntu 24.04 LTS

To install WSL with Ubuntu 24.04 LTS, open PowerShell as administrator and run:

```powershell
wsl --install -d Ubuntu-24.04
```

If you already use a different distribution or need multiple Linux distributions, consult the official Microsoft guide:

https://learn.microsoft.com/windows/wsl/install

## Optional: Windows Terminal and PowerShell

A modern terminal improves the WSL experience. If you do not already have the Windows Terminal, install it with `winget`:

```powershell
winget install Microsoft.WindowsTerminal
```

If you also want a recent PowerShell version, install it with:

```powershell
winget install Microsoft.PowerShell
```

If `winget` is unavailable, install Windows Terminal from the Microsoft Store.

## First WSL startup

1. Start the installed Ubuntu distribution from the Start menu.
2. Follow the prompts to create a user account and password.
3. Update the package list:

```bash
sudo apt update && sudo apt upgrade -y
```

## GUI support (Gazebo and RViz)

From Week 2 onward the course uses Gazebo and RViz, which are graphical applications. WSL supports this via **WSLg**, which is built into Windows 11 and ships with recent Windows 10 updates.

To verify that GUI apps work, install and run a test application:

```bash
sudo apt install x11-apps -y
xclock
```

A clock window should appear. If it does, Gazebo and RViz will work when you reach those weeks. If not, consult the [WSLg troubleshooting guide](https://github.com/microsoft/wslg/wiki/Diagnosing-&-remediation-of-display-access-issues).

## Next steps

After the workstation setup is complete, install the course software:

- For ROS 2 and Gazebo, see `ros-gz.md`.
- For the Python environment, see `python.md`.