# Python Environment

This document describes the local Python environment setup with conda for the ASMR tutorial.

## Install Miniconda

1. Download Miniconda from https://docs.conda.io/en/latest/miniconda.html.
2. Choose the installer for your operating system.
3. Follow the installation instructions.

## Create the course environment

From the repository root, run:

```bash
conda env create -f setup/environment.yaml
conda activate asmr
```

The environment is defined in `setup/environment.yaml` and contains the packages used in the course notebooks.

## Verify basic packages

Always activate the course environment before working on the tutorial:

```bash
conda activate asmr
```

Run:

```bash
python --version
python -c "import numpy, matplotlib; print('Python packages imported successfully')"
```

If these commands complete without errors, the Python environment is ready.

## Launch JupyterLab

Navigate to the `week_0` folder and start JupyterLab:

```bash
cd path/to/week_0
jupyter lab
```

JupyterLab will open in your browser. Click `exercise.ipynb` to open the exercise. Run the first code cell (Part 0) — if it executes without errors and shows a plot, everything is working.
