### 3.3 Proximal Policy Optimization

Proximal Policy Optimization (PPO) is an on-policy actor-critic algorithm that constrains policy updates using a clipped probability-ratio objective [19]. The clipping mechanism limits destructive update steps and improves optimization stability while preserving practical sample efficiency.

PPO served as the common optimization backbone for all compared methods in the study. Rollouts were collected on-policy, advantages were estimated from trajectory data, and policy and value updates were performed through multiple minibatch epochs per rollout. Using a common PPO configuration across methods isolated the effect of intrinsic reward design from differences in policy optimizer behavior.
