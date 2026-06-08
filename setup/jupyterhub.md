# JupyterHub

This document describes how to use the University JupyterHub for the ASMR tutorial.

## Overview

JupyterHub provides a hosted notebook environment. It is a software installation path, not a workstation setup path.

## What this file covers

- Accessing JupyterHub.
- Using the provided notebook environment.
- Starting course work without local package installation.

## Instructions

1. Open the University JupyterHub URL provided on the course page (Moodle / course website).
2. Log in with your university credentials.
3. Once logged in, you will see a file browser.

## Getting the course files onto JupyterHub

The course notebooks must be uploaded to your JupyterHub workspace. There are two ways:

**Option A — Upload via the browser (simplest)**
1. Click the **Upload** button (arrow icon) in the JupyterHub file browser.
2. Navigate to `week_0/` on your local machine and select `exercise.ipynb` and `utils.py`.
3. Upload both files.

**Option B — Clone via a terminal**
1. Open a terminal in JupyterHub (File → New → Terminal).
2. Run:
   ```bash
   git clone <course-repository-url>
   ```
   The repository URL is provided on the course page.

## Notes

- No local Python or ROS 2 installation is required when using JupyterHub.
- If JupyterHub is unavailable, use `python.md` for a local Python environment.
## Next step

After uploading the files, open `exercise.ipynb` and run the first code cell (Part 0 — Environment Check). If it completes without errors, the environment is ready.
