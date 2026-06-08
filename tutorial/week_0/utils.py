from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

# Direction vectors for each heading (theta in degrees).
#
# Coordinate convention:
#   x = column index, increases to the right (East)
#   y = row index,    increases downward (South)  ← screen / array convention
#
# That means "North" (the upward direction on screen) corresponds to y - 1,
# not y + 1, which is why theta = 90° maps to (0, -1).
#
#   theta |  name  |  (dx, dy)
#   ------+--------+-----------
#     0°  |  East  |  (+1,  0)
#    90°  | North  |  ( 0, -1)   y decreases = moves up on screen
#   180°  |  West  |  (-1,  0)
#   270°  | South  |  ( 0, +1)   y increases = moves down on screen
DIRECTION_VECTORS: dict[int, tuple[int, int]] = {
    0: (1, 0),    # East
    90: (0, -1),  # North  (y decreases = up on screen)
    180: (-1, 0), # West
    270: (0, 1),  # South  (y increases = down on screen)
}

# Action constants
FORWARD: int = 0
TURN_LEFT: int = 1
TURN_RIGHT: int = 2


def setup_matplotlib() -> None:
    """Configure matplotlib defaults for the notebook."""
    plt.style.use("default")
    plt.rcParams["figure.figsize"] = (8, 8)
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.grid"] = False


def draw_robot(
    state: np.ndarray,
    ax: Axes,
    color: str = "tab:blue",
    label: str | None = None,
) -> None:

    """Draw a single robot as an arrow on *ax*.

    Parameters
    ----------
    state : np.ndarray, shape (3,)
        Robot state [x, y, theta].
    ax : Axes
        Target axes.
    color : str
        Arrow colour.
    label : str or None
        Optional legend label.
    """
    x, y, theta = state
    dx, dy = DIRECTION_VECTORS[theta % 360]
    ax.annotate(
        "",
        xy=(x + 0.35 * dx, y + 0.35 * dy),
        xytext=(x - 0.15 * dx, y - 0.15 * dy),
        arrowprops=dict(arrowstyle="->", color=color, lw=2),
    )
    ax.plot(x, y, "o", color=color, markersize=8, label=label)


def draw_world(
    world: np.ndarray,
    ax: Axes,
    start: tuple[int, int] | None = None,
    goal: tuple[int, int] | None = None,
) -> None:
    """Render a 2-D grid world.

    Parameters
    ----------
    world : np.ndarray, shape (H, W)
        Grid with 0 = free, 1 = wall.
    ax : Axes
        Target axes.
    start : tuple (x, y) or None
        Optional start cell to highlight.
    goal : tuple (x, y) or None
        Optional goal cell to highlight.
    """
    H, W = world.shape
    ax.imshow(
        world,
        cmap="Greys",
        origin="upper",
        extent=(-0.5, W - 0.5, H - 0.5, -0.5),
        vmin=0,
        vmax=1,
        alpha=0.4,
    )
    for i in range(H + 1):
        ax.axhline(i - 0.5, color="grey", linewidth=0.5)
    for j in range(W + 1):
        ax.axvline(j - 0.5, color="grey", linewidth=0.5)
    if start is not None:
        ax.plot(*start, "s", color="tab:green", markersize=14, alpha=0.5, label="Start")
    if goal is not None:
        ax.plot(*goal, "*", color="tab:orange", markersize=18, alpha=0.7, label="Goal")
    ax.set_xlim(-0.5, W - 0.5)
    ax.set_ylim(H - 0.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")


def draw_trajectory(
    trajectory: list[np.ndarray],
    world: np.ndarray,
    ax: Axes,
    start: tuple[int, int] | None = None,
    goal: tuple[int, int] | None = None,
) -> None:
    """Draw a trajectory on the grid world.

    Parameters
    ----------
    trajectory : list of np.ndarray, each shape (3,)
        Sequence of states.
    world : np.ndarray, shape (H, W)
        The grid world.
    ax : Axes
        Target axes.
    start, goal : tuple or None
        Cells to highlight.
    """
    draw_world(world, ax, start=start, goal=goal)
    xs = [s[0] for s in trajectory]
    ys = [s[1] for s in trajectory]
    ax.plot(xs, ys, "-", color="tab:blue", linewidth=1.5, alpha=0.6)
    draw_robot(trajectory[0], ax, color="tab:green", label="Start pose")
    draw_robot(trajectory[-1], ax, color="tab:red", label="Final pose")
    ax.legend(loc="upper right", fontsize=9, labelspacing=0.8, handletextpad=0.6)


def is_blocked(x: int, y: int, world: np.ndarray) -> bool:
    """Check whether grid cell (x, y) is blocked.

    Parameters
    ----------
    x, y : int
        Cell coordinates.
    world : np.ndarray, shape (H, W)
        Grid world (0 = free, 1 = wall).

    Returns
    -------
    blocked : bool
        True if the cell is a wall or outside the grid.
    """
    H, W = world.shape
    if x < 0 or x >= W or y < 0 or y >= H:
        return True
    return bool(world[y, x] == 1)
