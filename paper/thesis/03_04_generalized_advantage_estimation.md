### 3.4 Generalized Advantage Estimation

Generalized Advantage Estimation (GAE) provides a controlled bias-variance trade-off for policy-gradient methods by exponentially weighting temporal-difference residuals [18]. Compared with high-variance short-horizon estimators, GAE generally yields smoother advantage targets and more stable policy updates in continuous-control settings [18].

In the training pipeline, GAE was computed on augmented rewards when intrinsic methods were enabled. Bootstrapping for truncated episodes followed rollout terminal-observation handling used by the PPO implementation, so advantage construction remained consistent across compared methods.
