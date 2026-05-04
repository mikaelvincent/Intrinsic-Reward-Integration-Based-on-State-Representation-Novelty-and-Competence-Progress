### 2.3 Learning Progress Based Exploration

Learning-progress exploration was motivated by the idea that intrinsically valuable experience is experience that improves predictive performance, not merely experience that is difficult {{CIT:17}}. Classical formulations tracked reductions in prediction error over time, often by comparing short-term and long-term competence statistics within local regions of the state space {{CIT:2,12}}.

R-IAC is a representative method in this family. It partitioned the space adaptively and prioritized regions where competence improved, while reducing attention to regions that were either already mastered or persistently unpredictable {{CIT:2}}. This mechanism addressed an important limitation of purely novelty-driven exploration by introducing a temporal notion of utility.

The literature also revealed practical challenges for scaling progress-based ideas to modern deep reinforcement learning. First, progress estimates depend on how locality is represented in high-dimensional observations. Second, progress signals can become unstable without careful smoothing and normalization. Third, exploration behavior may still degrade when regions maintain high error but negligible progress for extended periods {{CIT:2}}.

These limitations informed the GLPE design. The proposed framework estimated region-local progress in latent feature space using online partitioning and exponential moving averages, then combined this signal with feature-space impact to retain exploratory coverage while prioritizing learnable regions {{CIT:2}}.
