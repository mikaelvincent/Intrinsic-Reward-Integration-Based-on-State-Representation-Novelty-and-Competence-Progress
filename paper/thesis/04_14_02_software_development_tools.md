### 4.14.2 Software Development Tools

Software development and experimentation were implemented through a Python-based research stack with explicit separation of training, evaluation, benchmarking, visualization, and testing modules in the codebase [18]. The selected tools supported the PPO-centered pipeline, intrinsic reward modules, and benchmark environments described in prior sections [16][18][19][20].

| Tool or Library | Role in the Study | Evidence in Repository |
|---|---|---|
| Python 3.10 to 3.11 runtime | Core execution environment for all scripts and modules | Project runtime constraint in code configuration [18] |
| PyTorch | Neural network modeling and optimization for policy, value, and intrinsic modules | Declared project dependency [18] |
| Gymnasium | Standardized environment interface and benchmark task execution | Declared dependency and benchmark usage alignment [18][19] |
| MuJoCo and Gymnasium MuJoCo integration | Continuous-control physics simulation for Ant, HalfCheetah, and Humanoid tasks | Optional dependency and task-level alignment [18][20] |
| NumPy | Array operations and numerical preprocessing | Declared dependency [18] |
| Pandas | Structured result aggregation and CSV-based summaries | Declared dependency and results artifacts [18] |
| Matplotlib | Figure generation for evaluation curves, timing, and ablation visualizations | Declared dependency and plot artifacts [18] |
| Typer | Command-line interface for experiment and utility entry points | Declared dependency [18] |
| PyYAML | Configuration parsing for experiment setup | Declared dependency [18] |
| ImageIO and imageio-ffmpeg | Video and frame export support for experiment outputs | Declared dependency and video utility modules [18] |
| Pillow | Image processing support for generated visual outputs | Declared dependency [18] |
| Pytest | Automated verification of configuration, training, evaluation, and algorithm utilities | Optional development dependency and test suite presence [18] |

The toolchain was selected to preserve reproducibility and maintain compatibility between research code, generated metrics, and thesis reporting artifacts [18].
