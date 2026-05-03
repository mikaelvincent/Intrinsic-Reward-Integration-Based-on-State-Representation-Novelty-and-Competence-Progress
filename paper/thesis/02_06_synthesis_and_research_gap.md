### 2.6 Synthesis and Research Gap

The reviewed literature established that intrinsic motivation can substantially improve exploration under sparse or delayed extrinsic feedback [1], [2], [3], [4]. It also showed that novelty and prediction-error bonuses can become misaligned with task progress when stochasticity or model mismatch produces persistent surprise [9], [10], [14].

Learning-progress methods addressed part of this issue by prioritizing regions where predictive competence improved over time [5], [13]. Impact-driven methods added a complementary signal that favored transitions producing meaningful state change [11]. However, prior approaches did not fully resolve the joint requirement of maintaining broad exploratory behavior while suppressing intrinsically attractive but persistently unproductive regions in a lightweight on-policy setting [11], [13], [18].

Based on this gap, the thesis focused on a combined intrinsic formulation that integrated feature-space impact and region-local learning progress, with an optional region-specific gate for high-error low-progress regions [18]. The research direction remained consistent with the project problem statement, scope, and evaluation design by testing this formulation against established baselines under a shared PPO backbone using both sample-based and wall-clock based criteria [16], [17], [18].
