### 4.14.2 Software Development Tools

Software development and experimentation were implemented through a Python-based research stack with explicit separation of training, evaluation, benchmarking, visualization, and testing modules in the codebase . The selected tools supported the PPO-centered pipeline, intrinsic reward modules, and benchmark environments described in prior sections [19].

| Tool or Library | Role in the Study | Evidence in Repository |
|---|---|---|
| Python 3.10 to 3.11 runtime | Core execution environment for all scripts and modules | Project runtime constraint in code configuration  |
| PyTorch | Neural network modeling and optimization for policy, value, and intrinsic modules | Declared project dependency  |
| Gymnasium | Standardized environment interface and benchmark task execution | Declared dependency and benchmark usage alignment  |
| MuJoCo and Gymnasium MuJoCo integration | Continuous-control physics simulation for Ant, HalfCheetah, and Humanoid tasks | Optional dependency and task-level alignment  |
| NumPy | Array operations and numerical preprocessing | Declared dependency  |
| Pandas | Structured result aggregation and CSV-based summaries | Declared dependency and results artifacts  |
| Matplotlib | Figure generation for evaluation curves, timing, and ablation visualizations | Declared dependency and plot artifacts  |
| Typer | Command-line interface for experiment and utility entry points | Declared dependency  |
| PyYAML | Configuration parsing for experiment setup | Declared dependency  |
| ImageIO and imageio-ffmpeg | Video and frame export support for experiment outputs | Declared dependency and video utility modules  |
| Pillow | Image processing support for generated visual outputs | Declared dependency  |
| Pytest | Automated verification of configuration, training, evaluation, and algorithm utilities | Optional development dependency and test suite presence  |

The toolchain was selected to preserve reproducibility and maintain compatibility between research code, generated metrics, and thesis reporting artifacts .
