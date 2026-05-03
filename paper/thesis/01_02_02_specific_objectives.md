#### 1.2.2 Specific Objectives

1. To formulate an intrinsic reward score that combines feature-space impact and region-local learning progress derived from online latent-space partitioning and forward-model error trends [9], [16], [17], [18].
2. To implement two variants of the proposed method, namely GLPE and GLPE (no gate), within a shared PPO training pipeline and common model architecture [9], [17], [18].
3. To define and apply a region-specific gating mechanism that suppresses intrinsic shaping in persistently high-error and low-progress regions, then compare its behavior against the non-gated variant [9], [14], [17].
4. To compare the proposed variants against Vanilla PPO, ICM, RND, RIDE, and RIAC using consistent training budgets, evaluation checkpoints, and multi-seed aggregation [10], [11], [13], [16], [17], [18].
5. To evaluate outcomes using learning curves, step-normalized AUC, thresholded reliability statistics, intrinsic reward dynamics, and wall-clock-normalized AUC to capture both effectiveness and computational tradeoffs [17], [18].
