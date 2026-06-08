# Week 0 — Python Foundations & Environment Setup

## Overview

This week serves as a **self-assessment**. The exercise notebook tests whether your Python skills and development environment are ready for the rest of the course. It also introduces the Perceive–Reason–Act (PRA) loop — the central framework of this course — on a simple discrete grid world.

## How to Use This Material

1. Set up your environment (see [Setup](#setup) below).
2. Open `exercise.ipynb` and work through all parts.
3. If you get stuck, consult the refresher notebooks in `python-intro/` for the relevant topic, then return to the exercise.
4. You should be able to complete all parts (the bonus section is optional).

A reference solution is provided in `exercise_solution.ipynb`.

## Setup

Create and activate the conda environment:

```bash
conda env create -f setup/environment.yaml
conda activate asmr
```

For detailed instructions (including a JupyterHub option), see [`setup/README.md`](../setup/README.md).

## Contents

| File / Folder | Description |
|---------------|-------------|
| `exercise.ipynb` | Self-assessment exercise — PRA loop on a 2D grid world |
| `utils.py` | Helper functions for visualisation and grid operations |
| `python-intro/` | Refresher notebooks on Python, NumPy, and Matplotlib |


## Learning Objectives

- Set up a Python development environment for the course
- Represent a robot's state as a vector $[x,\; y,\; \theta]$
- Implement discrete robot actions (move forward, turn)
- Read sensor data from a grid world
- Close the PRA loop with a simple reactive control policy
