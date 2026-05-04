## 2. Review of Related Literature

This chapter reviews prior literature on intrinsic motivation for reinforcement learning and establishes the conceptual basis of the GLPE family examined in this thesis. The discussion is organized into five themes: intrinsic motivation foundations, novelty and prediction-error methods, learning-progress based exploration, impact-driven exploration, and reward shaping with policy invariance constraints.

Prior studies consistently reported that intrinsic rewards improved exploration when extrinsic feedback was sparse or delayed {{CIT:3,11,12,20}}. At the same time, multiple works identified a recurring limitation, wherein exploratory behavior was attracted to transitions that remained surprising but did not improve task learning {{CIT:8,15}}. This limitation motivated approaches that evaluate not only surprise, but also whether predictive competence improves over time, which is the core principle of learning progress {{CIT:2,17}}.

The reviewed literature therefore indicated a gap between broad exploratory drive and sustained usefulness of collected experience. The GLPE formulation addressed this gap by combining representation-level impact with region-local learning progress, and by introducing an optional region-wise gate to suppress persistently unproductive intrinsic shaping {{CIT:2,15}}.
