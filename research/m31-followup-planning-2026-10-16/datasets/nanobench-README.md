# NanoBench: A Multi-Task Benchmark Dataset for Nano-Quadrotor Research

[![arXiv](https://img.shields.io/badge/arXiv-2603.09908-b31b1b.svg)](https://arxiv.org/abs/2603.09908)
[![Demo Video](https://img.shields.io/badge/Demo-Video-blue)](https://syediu.github.io/assets/img/nanobench_demo.mp4)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-green.svg)](LICENSE)

**NanoBench** is an open dataset and reproducible benchmark suite for nano-quadrotor research, collected from a Crazyflie 2.1 platform under Vicon motion-capture ground truth. The dataset spans 172 flight recordings across 12 trajectory types, totalling approximately 107 minutes of synchronized flight data. Three benchmark tasks are provided covering system identification, controller, and onboard state estimation, each with runnable baselines and structured evaluation outputs.

▶️ **[Watch the demo video](https://syediu.github.io/assets/img/nanobench_demo.mp4)** to see sample flights from the dataset.

This repository accompanies the following publication:

```bibtex
@misc{ullah2026nanobenchmultitaskbenchmarkdataset,
      title={NanoBench: A Multi-Task Benchmark Dataset for Nano-Quadrotor System Identification, Control, and State Estimation},
      author={Syed Izzat Ullah and Jose Baca},
      year={2026},
      eprint={2603.09908},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2603.09908},
}
```

---

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Dataset](#dataset)
4. [Environment Setup](#environment-setup)
5. [Task 1: System Identification](#task-1-system-identification)
6. [Task 2: Control](#task-2-control)
7. [Task 3: State Estimation](#task-3-state-estimation)
8. [License](#license)

---

## Overview

The Crazyflie 2.1 is among the most widely used platforms for nano-quadrotor research, yet publicly available datasets that include synchronized Vicon ground truth, onboard EKF estimates, motor commands, IMU readings, and battery telemetry from a single flight are scarce. NanoBench fills this gap by providing:

- **172 flight recordings** across 12 trajectory types (circles, figure-eights, helices, trefoil knots, lissajous curves, random waypoints, battery drain, and more), each with multiple independent repetitions.
- **52 synchronized signal columns** per recording: Vicon ground-truth position, velocity, and orientation; onboard EKF state estimates; raw IMU (accelerometer + gyroscope); per-motor PWM commands; flight controller setpoints and PID outputs; and battery voltage.
- **Three ready-to-run benchmark tasks** with baseline implementations and standardized metrics, structured to facilitate direct comparison of new methods against established algorithms.

All flights were flown in an instrumented configuration that adds retroreflective markers and the wireless-charging deck to the stock airframe, raising the flying mass from 27 g to a measured 40.85 g. All data are in flat CSV format, readable without any robotics middleware.

---

## Repository Structure

```
nanobench/
├── datasets/
│   └── dataset/                    # 172 flight CSV files + paired metadata YAMLs
│       ├── B2_circle_slow_rep1.csv
│       ├── B2_circle_slow_rep1_metadata.yaml
│       └── ...
│
└── benchmarks/
    ├── utils/
    │   ├── data_loader.py          # Trajectory discovery and loading (TrajectoryData)
    │   ├── metrics.py              # ATE, RTE, RMSE
    │   └── plotting.py             # matplotlib style and save helpers
    │
    ├── task1_sysid/                # Task 1: quadrotor system identification
    │   ├── run_nanobench_sysid.py  # Entry point (setup / train / test / compare)
    │   ├── models/models.py        # Physics, Residual, Phys+Res, LSTM models
    │   ├── dataset/
    │   │   ├── dataset.py          # QuadDataset (PyTorch)
    │   │   └── convert_csvs.py     # NanoBench CSV → IDSIA format converter
    │   ├── train/                  # Training scripts for learned models
    │   ├── test/                   # Inference scripts
    │   └── data/                   # Auto-populated: data/train/, data/test/
    │
    ├── task2_control/              # Task 2: offline imitation-learning controllers
    │   ├── run_task2.py            # Entry point
    │   ├── data/loader.py          # Imitation-learning dataset builder
    │   ├── baselines/
    │   │   ├── bc_mlp.py           # Behavioural Cloning MLP
    │   │   ├── bc_lstm.py          # Behavioural Cloning LSTM
    │   │   └── mppi_controller.py  # MPPI with learned dynamics prior
    │   ├── dynamics/               # Learned forward dynamics model
    │   ├── evaluation/             # Closed-loop rollout evaluator
    │   └── results/                # Auto-populated outputs
    │
    ├── task3_stateEst/             # Task 3: EKF evaluation on trefoil trajectories
        ├── run_task3_trefoil.py    # Entry point
        ├── mellinger_trefoil/      # 15 Mellinger-controller trefoil flights
        ├── pid_trefoil/            # 13 PID-controller trefoil flights
        └── results/                # Auto-populated outputs

```

---

## Dataset

### Trajectory Types

| ID prefix | Trajectory | Speed variants | Flights |
|-----------|-----------|----------------|---------|
| A1b | Multi-sine excitation | n/a | 4 |
| B2 | Circle | slow, medium, fast | 18 (6 each) |
| B3 | Figure-eight | slow, medium, fast | 16 (6/6/4) |
| B5 | Helix | slow, medium, fast, Mellinger | 19 |
| B6 | Linear ramp | n/a | 8 |
| B7 | Oval | slow, medium, fast | 18 (6 each) |
| B8 | Star | slow, medium, fast | 18 (6 each) |
| B9 | Trefoil knot | slow, medium, fast | 57 (24/16/17) |
| B10 | Lissajous | slow, fast | 4 (2 each) |
| B11 | Random waypoints | n/a | 4 |
| B12 | Staircase climb | n/a | 2 |
| C4 | Battery drain (hover) | n/a | 4 |

**Total: 172 recordings, ~107 minutes of flight, 641,915 timesteps at 100 Hz.**

### Categories

The 12 trajectory types are grouped into three categories used by the benchmark protocols:

| Category | Trajectory types | Flights | Flight time | Samples |
|----------|-----------------|---------|-------------|---------|
| A: Excitation | Multi-sine (3D) | 4 | 4.6 min | 27,518 |
| B: Tracking | Circle, figure-8, oval, star, trefoil, lissajous, helix, ramp, random waypoints, staircase | 164 | 96.4 min | 578,623 |
| C: Battery drain | Battery-drain hover | 4 | 6.0 min | 35,774 |
| **Total** | | **172** | **107.0 min** | **641,915** |

Battery voltage across the dataset spans 3.08 V to 4.2 V, covering the full operational discharge curve of a single-cell LiPo. Category B tracking flights sit in the mid-to-nominal regime (3.8 V to 4.2 V), while the Category C hovers capture a complete discharge from ≈ 4.2 V down to ≈ 3.1 V.

### Time Synchronization

Firmware telemetry and Vicon pose are recorded on separate clocks and aligned offline by cross-correlating the onboard gyroscope rate against Vicon-derived angular velocity, searched on a 1 ms grid over ±2 s. The estimated offset has a median magnitude of 282 ms with a standard deviation of 17.3 ms across flights. After correction, all modalities are resampled onto a uniform 100 Hz Vicon time base and written to a single CSV per flight. Because a single Crazyradio link is bandwidth-limited, each firmware log block is delivered below its nominal rate; the raw per-block sample counts are preserved in the paired metadata file so the interpolated fraction of any signal can be recovered.

### CSV Column Reference

Every file in `datasets/dataset/` shares the following 52-column schema:

| Column(s) | Units | Source | Description |
|-----------|-------|--------|-------------|
| `t` | s | Vicon host clock | Timestamp |
| `px`, `py`, `pz` | m | Vicon | Ground-truth position (world frame) |
| `qx`, `qy`, `qz`, `qw` | unitless | Vicon | Ground-truth orientation (unit quaternion, scalar-last) |
| `roll`, `pitch`, `yaw` | deg | Vicon | Ground-truth Euler angles (ZYX) |
| `vx`, `vy`, `vz` | m/s | Vicon | Ground-truth linear velocity (Savitzky-Golay differentiated) |
| `wx_vicon`, `wy_vicon`, `wz_vicon` | rad/s | Vicon | Ground-truth angular velocity (world frame) |
| `imu_acc_x`, `imu_acc_y`, `imu_acc_z` | g | Onboard IMU | Specific force (body frame) |
| `imu_gyro_x`, `imu_gyro_y`, `imu_gyro_z` | rad/s | Onboard IMU | Angular velocity (body frame) |
| `motor_motor_m1` … `motor_motor_m4` | PWM [0–65535] | Onboard | Per-motor PWM commands |
| `est_stateEstimate_x/y/z` | m | Onboard EKF | EKF position estimate |
| `est_stateEstimate_vx/vy/vz` | m/s | Onboard EKF | EKF velocity estimate |
| `est_stateEstimate_ax/ay/az` | m/s² | Onboard EKF | EKF acceleration estimate |
| `att_stateEstimate_roll/pitch/yaw` | deg | Onboard EKF | EKF attitude (Euler) |
| `att_stateEstimate_qx/qy/qz/qw` | unitless | Onboard EKF | EKF attitude (quaternion) |
| `sp_ctrltarget_x/y/z/yaw` | m, deg | Flight controller | Position and yaw setpoints |
| `pid_controller_roll/pitch/yaw` | n/a | Flight controller | PID roll/pitch/yaw outputs |
| `pid_controller_cmd_thrust` | n/a | Flight controller | PID thrust command |
| `pwr_pm_vbat` | V | Onboard power monitor | Battery voltage (10 Hz, forward-filled) |

> **Note on the onboard EKF.** During collection the Vicon pose is relayed to the Crazyflie through cflib's `send_extpose()`, so `est_stateEstimate_*` and `att_stateEstimate_*` are the output of a Vicon-aided filter, not a dead-reckoning estimate. Task 3 therefore measures the consistency of the onboard fusion rather than standalone onboard estimation.

### Metadata Files

Each CSV is paired with a `<filename>_metadata.yaml` containing trajectory type, speed category, repetition index, nominal flight parameters, start and end battery voltage, and the raw per-block sample counts.

---

## Environment Setup

A single conda environment covers all three tasks. Python 3.10 is recommended; PyTorch is needed for Tasks 1 and 2.

```bash
conda create -n nanobench python=3.10
conda activate nanobench

# Core scientific stack
pip install numpy scipy pandas matplotlib scikit-learn pyyaml tqdm joblib

# Task 1 and Task 2: deep learning
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
# (CPU-only alternative: pip install torch torchvision)

# Task 2: imitation learning library
pip install imitation

# Task 2: MPPI
pip install pytorch-mppi

# Task 1: pytorch3d (for SO(3) rotation representation)
# Install from source if pip wheel is unavailable for your CUDA version:
pip install pytorch3d
# or: pip install "git+https://github.com/facebookresearch/pytorch3d.git"
```

All benchmark scripts are run from the repository root:

```bash
cd /path/to/nanobench
```

---

## Task 1: System Identification

### Scientific Question

Can a data-driven dynamics model trained on motor PWM commands and onboard state estimates accurately predict next-step quadrotor states? How do physics-based, residual, and recurrent architectures compare on unseen trajectories?

### Baselines

| Model | Description |
|-------|-------------|
| **Naive** | Predict zero acceleration (constant-velocity) |
| **Physics** | Rigid-body model with fixed thrust and drag coefficients |
| **Residual** | Physics model + MLP residual correction |
| **Phys+Res** | Combined physics and learned residual in a single network |
| **LSTM** | Sequence-to-sequence recurrent model, no physics prior |

### Input / Output

- **Input:** Current state (12D: position, velocity, SO(3) log-map rotation, angular velocity) + motor speeds in rad/s (4D)
- **Output:** Next-step state (12D) over a configurable prediction horizon, reported at h = 1, 10 and 50 steps (10 ms, 100 ms and 500 ms at 100 Hz)
- **Split:** trained on the Category A multi-sine excitation flights with a temporal 80/20 train/validation split within each flight; tested on held-out Category B tracking flights
- **Data source:** `datasets/dataset/`. Flat CSVs are automatically converted to IDSIA format during the setup step

### How to Run

```bash
cd benchmarks/task1_sysid

# Step 1: Convert NanoBench CSVs to IDSIA format and split into train/test
python run_nanobench_sysid.py setup

# Step 2: Train all learned models (default 500 epochs)
python run_nanobench_sysid.py train

# Optional: specify device and epoch count
python run_nanobench_sysid.py train --epochs 300 --device cuda:0

# Step 3: Run inference on the test split
python run_nanobench_sysid.py test

# Step 4: Compute metrics and print LaTeX table
python run_nanobench_sysid.py compare

# Or run all steps in sequence
python run_nanobench_sysid.py all --epochs 500 --device cuda:0
```

### Outputs

```
benchmarks/task1_sysid/
├── data/
│   ├── train/       # IDSIA-format CSVs for training
│   └── test/        # IDSIA-format CSVs for evaluation
├── checkpoints/     # Saved model weights (.pt)
└── results/         # Prediction CSVs, metric tables, comparison plots
```

---

## Task 2: Control

### Scientific Question

Can a controller trained offline via imitation learning from logged Crazyflie PID data reproduce competitive motor-command sequences? How do a feedforward MLP, a recurrent LSTM, and an MPPI planner with a learned dynamics prior compare under closed-loop rollout evaluation?

### Baselines

| Baseline | Architecture | Description |
|----------|-------------|-------------|
| **BC-MLP** | Feedforward MLP | Behavioural cloning: state → motor PWM |
| **BC-LSTM** | Recurrent LSTM | Sequence-to-sequence behavioural cloning |
| **MPPI** | Sampling-based MPC | Model Predictive Path Integral with a learned forward dynamics model and BC prior as warm-start. Default configuration: 10-step (100 ms) horizon, 128 sampled rollouts, temperature λ = 0.1, exploration noise σ = 0.02 on normalised commands |

### Observation and Action Space

- **Observation (14D):** position (3), EKF velocity (3), EKF attitude quaternion (4), position setpoint (3), battery voltage (1)
- **Action (4D):** normalised motor PWM ∈ [0, 1] (divide by 65535 to recover raw values)

### Evaluation Domains

The three baselines above are evaluated offline, as closed-loop rollouts against the learned dynamics model. The accompanying paper additionally reports the firmware PID and Mellinger controllers measured in real flight. The two domains are reported separately and are not directly comparable: offline rollouts are deterministic and carry no run-to-run spread, while the real-flight rows are averaged over repeated flights. Position RMSE, average displacement error, velocity RMSE, mean heading error, and a divergence rate (the percentage of time steps with position error above 0.5 m) are reported for both.

### How to Run

```bash
cd /path/to/nanobench   # repository root

# Train all three baselines and run evaluation
python benchmarks/task2_control/run_task2.py --mode all

# Train only
python benchmarks/task2_control/run_task2.py --mode train

# Evaluate a previously trained checkpoint
python benchmarks/task2_control/run_task2.py --mode eval

# Key options
python benchmarks/task2_control/run_task2.py \
    --mode all \
    --dataset-root datasets/dataset \
    --out-dir benchmarks/task2_control/results \
    --epochs 200 \
    --device cuda:0
```

### Outputs

```
benchmarks/task2_control/results/
├── bc_mlp_checkpoint.pt
├── bc_lstm_checkpoint.pt
├── dynamics_mlp_checkpoint.pt
├── split_metadata.json         # Train/val/test file assignment (reproducible)
├── scaler.pkl                  # StandardScaler fit on training observations
├── rollout_results.csv         # Per-trajectory rollout metrics
└── tables/
    └── task2_performance_table.tex / .csv
```

---

## Task 3: State Estimation

### Scientific Question

How accurately does the Crazyflie's onboard EKF track position and attitude during aggressive trefoil-knot trajectories? Does accuracy degrade systematically with battery discharge, and does it differ between the Mellinger and PID flight controllers?

### Evaluation

Onboard EKF estimates (`est_stateEstimate_*`, `att_stateEstimate_*`) are compared against Vicon ground truth using standard TUM/EuRoC trajectory evaluation metrics:

| Metric | Description |
|--------|-------------|
| **ATE RMSE / Mean** | Absolute Trajectory Error after Umeyama alignment |
| **RTE (1 m window)** | Relative Trajectory Error over 1 m path-length segments |
| **Velocity RMSE** | EKF vs. Vicon velocity, integrated over the flight |
| **Attitude RMSE** | Per-axis angle error (roll, pitch, yaw), pooled RMS |

Because the estimator already operates in the Vicon frame, the recovered Umeyama alignment is close to the identity, so the reported ATE is effectively a direct error in the common reference frame.

The evaluation subset contains 28 trefoil flights split across two controllers:

| Controller | Slow | Medium | Fast | Total |
|-----------|------|--------|------|-------|
| Mellinger | 5 | 5 | 5 | 15 |
| PID | 6 | 5 | 2 | 13 |

Runs from both controllers are pooled per speed regime, giving N = 11 slow, 10 medium and 7 fast.

### How to Run

```bash
# Trefoil-specific evaluation (Mellinger vs PID, three speed regimes)
python benchmarks/task3_stateEst/run_task3_trefoil.py

```

### Outputs

```
benchmarks/task3_stateEst/results/
├── task3_trefoil_ate_comparison.pdf          # Bar chart: EKF ATE per speed
├── task3_trefoil_error_timeseries.pdf        # Position error with std bands (stacked)
├── task3_trefoil_error_2x2_with_overlay.pdf  # 2×2: error panels + XY trajectory overlay
├── task3_trefoil_trajectory_overlay.pdf      # 3D Vicon vs EKF, one panel per speed
├── task3_trefoil_velocity_error.pdf          # Velocity error per speed regime
├── task3_trefoil_per_axis_error.pdf          # X/Y/Z error components over normalized time
└── tables/
    ├── task3_trefoil_table.tex
    └── task3_trefoil_table.csv
```

---


## License

This dataset and codebase are released under the BSD 3-Clause License. See `LICENSE` for details.
