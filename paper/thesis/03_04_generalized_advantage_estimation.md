### 3.4 Generalized Advantage Estimation

Generalized Advantage Estimation (GAE) computes advantage targets by exponentially weighting temporal-difference residuals, yielding a controllable bias-variance tradeoff for policy-gradient training {{CIT:18}}.

Within the training pipeline, GAE was applied to the reward stream after intrinsic augmentation when intrinsic methods were active. This design preserved consistency between value-target construction and the reward signal used for policy optimization.
