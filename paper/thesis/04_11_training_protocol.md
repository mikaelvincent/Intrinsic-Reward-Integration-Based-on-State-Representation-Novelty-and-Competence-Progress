### 4.11 Training Protocol

All agents were trained with PPO and GAE using separate policy and value multilayer perceptrons with two hidden layers of width 256 and ReLU activations [16-18]. Continuous-control policies used diagonal Gaussian outputs with action squashing to finite environment bounds when required [18].

Each training iteration collected up to \(N=16{,}384\) on-policy transitions, computed intrinsic rewards when applicable, set intrinsic rewards to zero on terminal transitions and specific truncation cases without final observation, then computed advantages and value targets. PPO updates were applied across shuffled minibatches for multiple epochs. Adam optimization, per-batch advantage normalization, and gradient-norm clipping at 1.0 were used for policy and value updates [16-18].

Vector observations were normalized online using running mean and variance, and the same normalization was applied across policy, value, and intrinsic modules. Trainable intrinsic modules were updated once per PPO iteration using the same collected on-policy batch. For methods without internal intrinsic normalization, running RMS normalization was applied to raw intrinsic output before scaling and clipping. For methods with intrinsically normalized outputs, scaling and clipping were applied directly [18].


Table 4.2. PPO hyperparameters by environment [18].

| Environment | LR | Epochs | Minibatches | Clip | Lambda | Entropy | V-clip | KL stop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MountainCar-v0 | 3.0e-4 | 10 | 16 | 0.20 | 0.95 | 0.00 | 0.00 | 0.06 |
| BipedalWalker-v3 | 5.0e-4 | 5 | 16 | 0.25 | 0.95 | 0.00 | 0.00 | 0.06 |
| Ant-v5 | 1.5e-4 | 15 | 64 | 0.20 | 0.95 | 0.00 | 0.20 | 0.04 |
| HalfCheetah-v5 | 3.0e-4 | 10 | 32 | 0.20 | 0.95 | 0.01 | 0.20 | 0.03 |
| Humanoid-v5 | 2.0e-4 | 5 | 32 | 0.20 | 0.97 | 0.01 | 0.20 | 0.03 |

Table 4.3. GLPE hyperparameters by environment [18].

| Environment | eta | r_max | alpha_LP | p_start | p_end | C | D_max | beta_long | beta_short | kappa | tau_s | K | R_min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MountainCar-v0 | 0.05 | 4.0 | 0.5 | 0.05 | 0.80 | 128 | 10 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 8 |
| BipedalWalker-v3 | 0.08 | 4.0 | 0.5 | 0.12 | 0.75 | 200 | 12 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 16 |
| Ant-v5 | 0.06 | 4.0 | 0.6 | 0.10 | 0.70 | 256 | 12 | 0.997 | 0.92 | 0.012 | 2.5 | 8 | 64 |
| HalfCheetah-v5 | 0.04 | 5.0 | 0.5 | 0.05 | 0.75 | 256 | 12 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 32 |
| Humanoid-v5 | 0.06 | 5.0 | 0.5 | 0.05 | 0.80 | 256 | 12 | 0.998 | 0.92 | 0.010 | 2.0 | 5 | 32 |
