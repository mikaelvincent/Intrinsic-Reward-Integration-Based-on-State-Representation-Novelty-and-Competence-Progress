### 4.13 Statistical Analysis

Performance curves were aggregated across seeds using mean return trajectories, with uncertainty bands derived by bootstrap resampling across seeds. Scalar summaries included final-checkpoint return, step-normalized AUC, and wall-clock AUC under a common per-environment time horizon defined by the minimum final runtime among compared methods.

Thresholded reliability analysis used task-specific solved thresholds and additional reduced thresholds at 25 percent and 50 percent of solved level. For each threshold, summaries included reach rate and steps-to-threshold distribution across seeds. This analysis separated delayed success from non-attainment and was used to complement curve-level comparisons.

Runtime analysis decomposed per-iteration wall-clock into environment interaction, policy inference, intrinsic computation, intrinsic-module update, advantage computation, and PPO optimization. The decomposition was used to attribute efficiency differences and to contextualize wall-clock AUC outcomes. Additional diagnostic measurements, such as gating-median recomputation throughput, were treated as supporting implementation analysis rather than primary benchmark criteria.
