### 6.1 Conclusions

The study showed that intrinsic-reward shaping based on combined feature-space impact and region-local learning progress can improve exploration quality while preserving practical training stability across mixed task regimes [11][13][18]. Under the benchmark conditions used in this work, GLPE without gating behaved as the most consistent default variant, remaining competitive with strong intrinsic baselines on both step-normalized and wall-clock views in most tested environments [9][10][18].

The strongest gains were observed in sparse-reward exploration, particularly on MountainCar-v0, where GLPE produced favorable threshold reliability and step-efficiency behavior relative to compared methods [18]. On dense-reward locomotion tasks, outcomes indicated competitive but non-uniform superiority, which is consistent with the higher variance and task-dependent exploration demands of those settings [18].

The gated GLPE variant provided targeted suppression of intrinsic shaping in regions where prediction error stayed high while local learning progress was weak, reducing exposure to potentially unproductive curiosity signals [14][18]. This behavior supported robustness in sparse settings but could be conservative in high-variance domains, especially when aggressive filtering delayed beneficial exploration [18].

The cosine taper schedule for intrinsic-reward scaling supported the intended transition from exploration assistance to task-return optimization later in training [18]. This schedule design helped maintain compatibility with PPO optimization dynamics while limiting late-stage dependence on intrinsic bonuses [16][18].

The study remained bounded to vector-observation control benchmarks and an on-policy PPO backbone, and the applied intrinsic shaping was not policy-invariant in the formal reward-transformation sense [12][16][18]. Therefore, conclusions should be interpreted as evidence of practical effectiveness within the evaluated setup rather than universal guarantees across architectures, observation modalities, or training paradigms [18].
