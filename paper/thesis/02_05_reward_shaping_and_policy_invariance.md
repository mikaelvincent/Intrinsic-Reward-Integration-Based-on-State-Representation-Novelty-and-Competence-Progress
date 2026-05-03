### 2.5 Reward Shaping and Policy Invariance

Reward shaping modifies the optimization signal to accelerate learning, but shaping terms can alter policy preferences if they are not theoretically constrained [12]. The policy-invariance result of Ng, Harada, and Russell showed that only potential-based shaping guarantees preservation of optimal policies under reward transformation [12].

Most intrinsic rewards used in deep reinforcement learning are not potential-based in this strict sense, because they depend on nonstationary predictive models, visitation statistics, or representation dynamics [9], [10], [11], [13]. Consequently, such methods are generally treated as heuristic but effective objectives whose value must be demonstrated empirically.

This theoretical context was important for the present study. The GLPE intrinsic term was applied as additive shaping during PPO training, with clipping and scheduling controls, but it was not claimed to be policy-invariant [12], [16], [18]. Therefore, evaluation focused on empirical outcomes, including step efficiency, wall-clock efficiency, thresholded reliability, and final extrinsic return [16], [17], [18].
