### 1.4 Scope and Limitations of the Study

The study focused on intrinsic reward design for on policy deep reinforcement learning with a shared PPO backbone. The proposed methods were limited to GLPE and GLPE (no gate), which used the same base intrinsic score with and without region specific gating.

The experimental scope was restricted to MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5, with fixed environment rewards and termination settings. Baseline comparisons were limited to Vanilla PPO, ICM, RND, RIDE, and RIAC under aligned training budgets, checkpoint schedules, and deterministic offline evaluation from saved checkpoints.

The intrinsic formulation depended on learned latent representations, forward and inverse dynamics components, online region partitioning, and exponential moving average statistics for progress estimation. Therefore, findings were bounded by the selected model classes, hyperparameter settings, and implementation configuration used in this project.

Computational analysis was conducted in the project execution environment. Wall clock results reflected the recorded runtime components under common time budgets, so absolute timings may vary across hardware or software stacks.

The study did not claim policy invariance for intrinsic shaping terms. Conclusions were interpreted empirically through returns, reliability at selected thresholds, intrinsic reward behavior, and measured computational overhead {{CIT:9}}.
