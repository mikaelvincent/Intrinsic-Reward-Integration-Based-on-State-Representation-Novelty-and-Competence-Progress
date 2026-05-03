### 3.4 Generalized Advantage Estimation

Generalized Advantage Estimation (GAE) provides a bias-variance tradeoff for policy-gradient updates by exponentially weighting temporal-difference residuals. Compared with single-step estimators, GAE generally reduces variance in advantage estimates and improves optimization stability in continuous control settings [18].

In the study pipeline, GAE was applied to rewards after intrinsic augmentation when intrinsic methods were enabled. Bootstrapping behavior for time-limit truncations followed the available final-observation signal in the logged rollouts, which maintained consistent target construction across methods [18,19].
