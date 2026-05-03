### 4.11 Training Protocol

All agents were trained with PPO and GAE using separate policy and value multilayer perceptrons with two hidden layers of width 256 and ReLU activations [16-18]. Continuous-control policies used diagonal Gaussian outputs with action squashing to finite environment bounds when required [18].

Each training iteration collected up to \(N=16{,}384\) on-policy transitions, computed intrinsic rewards when applicable, set intrinsic rewards to zero on terminal transitions and specific truncation cases without final observation, then computed advantages and value targets. PPO updates were applied across shuffled minibatches for multiple epochs. Adam optimization, per-batch advantage normalization, and gradient-norm clipping at 1.0 were used for policy and value updates [16-18].

Vector observations were normalized online using running mean and variance, and the same normalization was applied across policy, value, and intrinsic modules. Trainable intrinsic modules were updated once per PPO iteration using the same collected on-policy batch. For methods without internal intrinsic normalization, running RMS normalization was applied to raw intrinsic output before scaling and clipping. For methods with intrinsically normalized outputs, scaling and clipping were applied directly [18].
