### 3.3 Proximal Policy Optimization

Proximal Policy Optimization (PPO) is an on-policy actor-critic method that constrains policy updates through a clipped probability-ratio objective. The clipping operation limits destructive update steps while retaining first-order optimization efficiency {{CIT:19}}.

PPO served as the common optimization backbone for all methods in the study. Rollouts were collected on policy, advantages were computed from trajectory data, and multiple minibatch epochs were executed per update. Using shared PPO settings across methods reduced confounding factors in baseline comparisons.
