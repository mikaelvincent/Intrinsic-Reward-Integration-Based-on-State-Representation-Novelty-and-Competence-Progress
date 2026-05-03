### 4.9 Experimental Environment

Experiments were conducted on five Gymnasium benchmark tasks spanning sparse-reward and dense-reward control settings: MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5 [18], [19], [20]. The protocol used default environment rewards and termination conditions, with no domain randomization and no additional frame skipping [18].

Training used vectorized environments with \(B\) parallel instances and rollout length \(T\), configured so that nominal batch size per PPO update was
\[
N=B\times T=16{,}384
\]
transitions. The final update could be smaller when remaining budget was below \(N\). Environment-specific step budgets and seed counts were fixed according to the source experimental table, and all compared methods used identical per-environment seed sets [18].

Execution was performed under deterministic settings when supported, and timing measurements were gathered in the same execution mode used for training so that wall-clock statistics reflected end-to-end optimization overhead [18].
