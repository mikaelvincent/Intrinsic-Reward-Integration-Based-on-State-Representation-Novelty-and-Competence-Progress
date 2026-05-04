### 2.6 Synthesis and Research Gap

The reviewed literature showed that intrinsic motivation can improve exploration when extrinsic rewards are sparse or delayed {{CIT:3,11,12,20}}. It also showed that novelty and prediction-error bonuses can become misaligned with task progress when persistent stochasticity or model mismatch sustains high surprise {{CIT:6,8,13}}.

Learning-progress methods addressed part of this issue by prioritizing regions where predictive competence improved over time {{CIT:2,17}}. Impact-driven methods added a complementary signal that favored transitions associated with meaningful state change {{CIT:15}}. However, existing approaches did not fully resolve the combined requirement of maintaining broad exploration while suppressing intrinsically attractive but persistently unproductive regions in a lightweight on-policy setting {{CIT:2,15}}.

Based on this gap, this thesis focused on a combined intrinsic formulation that integrated feature-space impact and region-local learning progress, with an optional region-specific gate for high-error, low-progress regions. This direction remained consistent with the problem statement, scope, and evaluation design by testing the formulation against established baselines under a shared PPO backbone using both sample-based and wall-clock criteria.
