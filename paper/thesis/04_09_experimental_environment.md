### 4.9 Experimental Environment

Experiments were conducted on five Gymnasium benchmark tasks spanning sparse-reward and dense-reward control settings: MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5 , , . The protocol used default environment rewards and termination conditions, with no domain randomization and no additional frame skipping .

Training used vectorized environments with \(B\) parallel instances and rollout length \(T\), configured so that nominal batch size per PPO update was
\[
N=B\times T=16{,}384
\]
transitions. The final update could be smaller when remaining budget was below \(N\). Environment-specific step budgets and seed counts were fixed according to the source experimental table, and all compared methods used identical per-environment seed sets .

Execution was performed under deterministic settings when supported, and timing measurements were gathered in the same execution mode used for training so that wall-clock statistics reflected end-to-end optimization overhead .


Table 4.1. Benchmark suite and training budgets.

| Environment | B | T | N | Total steps | Seeds |
|---|---:|---:|---:|---:|---:|
| MountainCar-v0 | 16 | 1,024 | 16,384 | 3,000,000 | 10 |
| BipedalWalker-v3 | 8 | 2,048 | 16,384 | 7,000,000 | 8 |
| Ant-v5 | 8 | 2,048 | 16,384 | 15,000,000 | 8 |
| HalfCheetah-v5 | 8 | 2,048 | 16,384 | 15,000,000 | 8 |
| Humanoid-v5 | 4 | 4,096 | 16,384 | 30,000,000 | 5 |

The symbol B denotes the number of parallel environment instances, T denotes rollout horizon per instance, and N = B x T denotes transitions per PPO update .
