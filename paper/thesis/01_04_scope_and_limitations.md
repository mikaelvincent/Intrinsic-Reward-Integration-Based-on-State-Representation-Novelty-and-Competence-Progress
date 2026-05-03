### 1.4 Scope and Limitations of the Study

The study covered intrinsic reward design and evaluation for on-policy deep reinforcement learning using a shared PPO backbone with generalized advantage estimation [18]. The proposed methods were limited to the GLPE family, consisting of a gated variant and a non-gated variant that shared the same base intrinsic score [13,18].

Experimental scope was restricted to five Gymnasium benchmarks, namely MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5, under fixed environment reward functions and termination rules . Comparisons were limited to Vanilla PPO, ICM, RND, RIDE, and RIAC using common training budgets, aligned checkpoint schedules, and deterministic offline evaluation from saved checkpoints [2,6,15,18,19].

The intrinsic formulation relied on learned latent representations, forward and inverse dynamics modeling, online region partitioning, and exponential moving average statistics for learning progress. Therefore, conclusions were bounded by the chosen model classes, hyperparameter settings, and implementation choices documented in the experiment configuration [13,18].

The computational analysis was performed in the execution setting used by the project, with wall-clock comparisons derived from logged runtime components and common per-environment time budgets. Consequently, absolute timing results may vary under different hardware or software stacks, although the reported procedure remains reproducible within the documented setup [18].

The study did not claim policy invariance of intrinsic shaping and did not treat intrinsic reward terms as theoretically neutral transformations of the task objective. Findings were interpreted empirically in relation to exploration behavior, final returns, reliability at selected thresholds, and measured computational overhead [9,18].
