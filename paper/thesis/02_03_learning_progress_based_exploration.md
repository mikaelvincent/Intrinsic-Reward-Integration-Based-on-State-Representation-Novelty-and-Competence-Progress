### 2.3 Learning-Progress Based Exploration

Learning-progress exploration was motivated by the view that intrinsically valuable experience is experience that improves predictive performance, rather than experience that is only difficult {{CIT:17}}. Classical formulations tracked reductions in prediction error over time, often by comparing short-horizon and long-horizon competence statistics within local regions of the state space {{CIT:2,12}}.

R-IAC is a representative method in this family. It partitioned the space adaptively and prioritized regions with active competence improvement, while reducing emphasis on regions that were already mastered or persistently unpredictable {{CIT:2}}. This mechanism addressed a central limitation of purely novelty-driven exploration by introducing a temporal notion of utility.

The literature also identified practical challenges when scaling progress-based ideas to modern deep reinforcement learning. Progress estimates depend on how locality is represented in high-dimensional observation spaces, and the resulting signals can be unstable without smoothing and normalization. In addition, behavior can still degrade when regions maintain high error but negligible progress over long intervals {{CIT:2}}.

These limitations informed the GLPE design. The framework estimated region-local progress in latent feature space through online partitioning and exponential moving averages, then combined this signal with feature-space impact to preserve exploratory coverage while prioritizing learnable regions {{CIT:2}}.
