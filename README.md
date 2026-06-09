# ASMR

Personal workspace for the ASMR course. Course tutorial material lives in `tutorial/` as a [git subtree](https://git-scm.com/book/en/v2/Git-Tools-Subtree-Merging); own code belongs elsewhere in this repo.

## Tutorial subtree

| | |
|---|---|
| Remote | `tutorial` |
| Upstream | https://zivgitlab.uni-muenster.de/ai-systems/teaching/public/26-ss/asmr/tutorial |
| Branch | `main` |
| Path | `tutorial/` |

Treat `tutorial/` as read-only reference. Start with [`tutorial/README.md`](tutorial/README.md) and [`tutorial/setup/README.md`](tutorial/setup/README.md).

### Pull upstream updates

```bash
git fetch tutorial
git subtree pull --prefix=tutorial tutorial main --squash
```

## ROS workspace (`my_robot_ws`)

`build/`, `install/`, and `log/` are not tracked — they are created locally by colcon.

After cloning or pulling, build from scratch:

```bash
cd my_robot_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

If you moved the workspace or see CMake path errors, delete the artifacts first:

```bash
rm -rf build install log
colcon build --symlink-install
```
