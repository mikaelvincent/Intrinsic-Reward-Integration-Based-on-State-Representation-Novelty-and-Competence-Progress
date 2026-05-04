### 4.10 Baseline Methods

The proposed methods were compared against five baselines that represent established intrinsic-reward or control references: Vanilla PPO, ICM, RND, RIDE, and RIAC {{CIT:2,6,13,15,19}}. Vanilla PPO optimized only extrinsic reward and served as the non-intrinsic control baseline.

ICM used forward-model prediction error in learned feature space as intrinsic reward. RND used predictor error against a fixed random target network. RIDE used feature-space impact modulated by episodic visitation counts from discretized features. RIAC used region-local learning progress from adaptive partitioning of feature space {{CIT:2,6,13,15}}.

All methods shared the same PPO backbone and policy-value architecture within each environment. Intrinsic-reward methods used a common augmented-reward form with scaling and clipping, and per-environment intrinsic scale parameters were held constant across methods to reduce reward-scale confounding in cross-method comparison {{CIT:19}}.
