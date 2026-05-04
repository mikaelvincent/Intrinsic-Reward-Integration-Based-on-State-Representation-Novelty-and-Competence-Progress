### 2.5 Reward Shaping and Policy Invariance

Reward shaping modifies optimization signals to accelerate learning, but shaping terms can alter policy preferences when theoretical constraints are not satisfied {{CIT:9}}. The policy-invariance result of Ng, Harada, and Russell showed that only potential-based shaping guarantees preservation of optimal policies under reward transformation {{CIT:9}}.

Most intrinsic rewards used in deep reinforcement learning are not potential-based in this strict sense, because they depend on nonstationary predictive models, visitation statistics, or representation dynamics {{CIT:2,6,13,15}}. Consequently, these methods are generally treated as heuristic objectives that must be validated empirically.

This theoretical context was central to the present study. The GLPE intrinsic term was applied as additive shaping during PPO training, with clipping and scheduling controls, and no claim of policy invariance was made. Evaluation therefore emphasized empirical outcomes, including step efficiency, wall-clock efficiency, thresholded reliability, and final extrinsic return.
