### 5.3 Thresholded Reliability and Steps-to-Threshold

Thresholded analysis was used to separate delayed attainment from complete non-attainment [18]. Solved-threshold statistics showed that both GLPE variants solved MountainCar-v0 in all seeds, each at a median of 0.35M steps, while the most reliable baseline solved 9 of 10 seeds at 0.44M steps [11][18].

At solved level, reliability differed more on tasks near the performance cutoff. On BipedalWalker-v3, GLPE solved 4 of 8 seeds and GLPE without gating solved 2 of 8, while RIAC solved 8 of 8 but at a slower median of 4.09M steps [13][18]. On Humanoid-v5, solved-threshold reach counts were low across methods, which was consistent with the high-variance behavior seen in learning curves [18].

At 50 percent threshold, GLPE without gating reached the target in all seeds on four tasks and in 4 of 5 seeds on Humanoid-v5, matching the strongest baseline reach count on each environment [18]. The gap between 50 percent and 100 percent success therefore concentrated on high-variance or near-cutoff regimes rather than on early competence acquisition [18].
