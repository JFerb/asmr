from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# ── Simulation parameters ─────────────────────────────────────────────────────
V: float         = 1.0   # forward speed (m/s)
DT: float        = 0.05  # timestep (s)
STEPS: int       = 800   # default simulation length
Y0: float        = 1.0   # default initial lateral offset (m)
Y_REF: float     = 0.0   # target lane position (m)
W_MAX: float     = 0.5   # maximum heading rate (rad/s)
DIST: float      = 0.15  # systematic error magnitude (rad/s)
NOISE_STD: float = 0.05   # random error standard deviation on e(t)


def simulate(
    controller_fn,
    systematic_error: bool = False,
    random_error: bool = False,
    y0: float = Y0,
    steps: int = STEPS,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Run the lane-following simulation.

    The car obeys simplified unicycle kinematics at fixed forward speed V.
    At each step the controller receives the (possibly corrupted) cross-track
    error and returns a heading rate omega, which is clipped to [-W_MAX, W_MAX].

    Parameters
    ----------
    controller_fn : callable
        Signature: ``controller_fn(e, e_prev, integral, dt) -> float``

        e        : current cross-track error, possibly with random error (m)
        e_prev   : error at the previous timestep (m)
        integral : running sum of e * dt accumulated by the simulator
        dt       : timestep (s)

    systematic_error : bool
        If True, a constant angular velocity DIST (rad/s) biases the car's
        heading at every step, modelling a persistent crosswind yaw torque.
    random_error : bool
        If True, independent Gaussian noise with std NOISE_STD is added to
        the sensed error at every step, modelling sensor uncertainty.
    y0 : float
        Initial lateral position of the car (m). Defaults to Y0.
    steps : int
        Number of simulation steps. Defaults to STEPS.

    Returns
    -------
    t, x, y, e, omega : np.ndarray, each shape (steps,)
        t     : time vector (s)
        x     : longitudinal position (m)
        y     : lateral position (m)  — true, not noisy
        e     : true cross-track error (m)  — Y_REF - y
        omega : heading rate applied at each step (rad/s)
    """
    x, y, theta = 0.0, y0, 0.0
    e_prev   = Y_REF - y
    integral = 0.0

    t_hist = np.zeros(steps)
    x_hist = np.zeros(steps)
    y_hist = np.zeros(steps)
    e_hist = np.zeros(steps)
    w_hist = np.zeros(steps)

    rng = np.random.default_rng(seed=42)

    for k in range(steps):
        e_true   = Y_REF - y
        e_sensed = e_true + (rng.normal(0.0, NOISE_STD) if random_error else 0.0)
        integral += e_sensed * DT

        omega = controller_fn(e_sensed, e_prev, integral, DT)
        omega = np.clip(omega, -W_MAX, W_MAX)

        t_hist[k] = k * DT
        x_hist[k] = x
        y_hist[k] = y
        e_hist[k] = e_true
        w_hist[k] = omega

        theta += omega * DT
        x     += V * np.cos(theta) * DT
        y     += V * np.sin(theta) * DT
        if systematic_error:
            theta += DIST * DT

        e_prev = e_sensed

    return t_hist, x_hist, y_hist, e_hist, w_hist


def plot_trajectory(
    x: np.ndarray,
    y: np.ndarray,
    title: str,
    ax: Axes | None = None,
) -> Axes:
    """Bird's-eye trajectory plot with the target lane marked.

    Parameters
    ----------
    x, y : np.ndarray
        Longitudinal and lateral position arrays.
    title : str
        Axes title.
    ax : Axes or None
        Target axes. A new figure is created when None.

    Returns
    -------
    ax : Axes
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 3))
    ax.axhline(Y_REF, color="green", linewidth=1.5, linestyle="--", label="Target line")
    ax.plot(x, y, color="steelblue", linewidth=1.5, label="Car trajectory")
    ax.scatter(x[0], y[0], color="orange", zorder=5, label="Start")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_ylim(-3., 3.)
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    return ax


def plot_signals(
    t: np.ndarray,
    e: np.ndarray,
    omega: np.ndarray,
    title: str,
    ax_e: Axes | None = None,
    ax_w: Axes | None = None,
) -> tuple[Axes, Axes]:
    """Two-panel signal plot: cross-track error and heading rate over time.

    Parameters
    ----------
    t : np.ndarray
        Time vector (s).
    e : np.ndarray
        Cross-track error (m).
    omega : np.ndarray
        Heading rate (rad/s).
    title : str
        Title placed on the top panel.
    ax_e, ax_w : Axes or None
        Target axes for the error and omega panels respectively.
        A new figure with two stacked axes is created when both are None.

    Returns
    -------
    ax_e, ax_w : Axes
    """
    if ax_e is None:
        _, (ax_e, ax_w) = plt.subplots(2, 1, figsize=(8, 4), sharex=True)

    ax_e.axhline(0, color="green", linewidth=1.0, linestyle="--")
    ax_e.plot(t, e, color="tomato", linewidth=1.2)
    ax_e.set_ylabel("e(t)  (m)")
    ax_e.set_title(title)
    ax_w.axhline(0, color="gray", linewidth=0.8, linestyle=":")
    ax_w.plot(t, omega, color="steelblue", linewidth=1.2)
    ax_w.set_ylabel("ω(t)  (rad/s)")
    ax_w.set_xlabel("t (s)")
    return ax_e, ax_w
