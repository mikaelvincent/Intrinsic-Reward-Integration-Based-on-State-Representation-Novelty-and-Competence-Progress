### 1.1 Rationale of the Study

Exploration remains a central challenge in reinforcement learning because data collection decisions directly affect convergence speed, policy quality, and training stability when external rewards are limited {{CIT:3,11}}. Novelty and prediction error based intrinsic rewards can accelerate discovery, but these signals may remain high in stochastic or poorly modeled regions that contribute little to long term task improvement {{CIT:6,8,13}}.

Learning progress provides a more selective criterion by prioritizing regions where predictive capability is improving {{CIT:12,17}}. However, practical application in high dimensional deep RL requires a mechanism that localizes progress, remains computationally lightweight, and integrates with standard policy optimization.

The study was motivated by this methodological need. GLPE was designed to combine representation change sensitivity, region local progress estimation, and optional suppression of unproductive intrinsic shaping through a simple gate. This design targeted unproductive curiosity while preserving compatibility with PPO based training.

The rationale also included an evaluation concern. Step based return alone does not fully represent method utility in real training pipelines. For this reason, the study assessed both environment step performance and wall clock performance, together with thresholded reliability summaries across benchmark tasks.
