import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def setup_matplotlib():
    """Configure matplotlib defaults for the FK/IK notebook."""
    matplotlib.rcParams["figure.figsize"] = (6, 6)
    matplotlib.rcParams["axes.grid"] = True
    matplotlib.rcParams["axes.axisbelow"] = True


def draw_arm(joint_positions, ax, color="steelblue", **kwargs):
    """Draw a 2-link arm as a connected line with joint markers.

    Parameters
    ----------
    joint_positions : list of (float, float)
        Sequence of (x, y) positions: [base, elbow, end-effector].
    ax : matplotlib.axes.Axes
        Axes to draw on.
    color : str, optional
        Line and marker colour. Default ``'steelblue'``.
    **kwargs
        Forwarded to ``ax.plot``.
    """
    xs = [p[0] for p in joint_positions]
    ys = [p[1] for p in joint_positions]
    ax.plot(xs, ys, "-o", color=color, linewidth=3, markersize=8, **kwargs)


def draw_workspace_scatter(points, ax):
    """Scatter-plot a set of end-effector positions.

    Parameters
    ----------
    points : list of (float, float)
        End-effector (x, y) positions to plot.
    ax : matplotlib.axes.Axes
        Axes to draw on.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.scatter(xs, ys, s=1, alpha=0.3, color="steelblue")
