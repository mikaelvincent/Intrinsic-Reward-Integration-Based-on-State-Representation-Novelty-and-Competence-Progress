### 5.8 Summary of Findings

Results across curve-level, threshold-level, and efficiency-level analyses support four main findings. First, GLPE was strongest in sparse-reward exploration, with clear gains on MountainCar-v0 in both step-AUC and solved-threshold reliability. Second, on dense-reward locomotion tasks, GLPE variants remained competitive but did not consistently exceed the best intrinsic baseline on all metrics {{CIT:6,13,15}}.

Third, thresholded analysis showed that many apparent gaps at solved level were concentrated in high-variance or near-cutoff settings, especially BipedalWalker-v3 and Humanoid-v5, while intermediate-threshold competence was often comparable to top baselines {{CIT:2}}. Fourth, ablation and diagnostic results indicated that combining impact and learning progress was generally robust across mixed task regimes, and that gating behaved selectively rather than globally.

Overall, the evidence indicates that GLPE is a practical intrinsic-shaping framework for balancing exploration guidance and policy optimization stability, with strongest benefits in sparse or exploration-sensitive environments and acceptable competitiveness elsewhere.
