#### 1.2.2 Specific Objectives

1. To formulate an intrinsic reward score that combines feature space impact and region local learning progress from online latent space partitioning and forward model error trends.
2. To implement GLPE and GLPE (no gate) within a shared PPO training pipeline and aligned model architecture.
3. To define a region specific gating mechanism that suppresses intrinsic shaping in persistently high error and low progress regions, and to compare it with the non gated variant.
4. To compare the proposed variants with Vanilla PPO, ICM, RND, RIDE, and RIAC under consistent training budgets, evaluation checkpoints, and multi seed aggregation.
5. To evaluate performance using learning curves, step normalized AUC, thresholded reliability, intrinsic reward dynamics, and wall clock normalized AUC.
