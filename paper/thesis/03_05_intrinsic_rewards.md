### 3.5 Intrinsic Rewards

Intrinsic rewards were used to complement sparse or delayed extrinsic rewards by assigning additional utility to informative transitions. Prior work has used prediction error, random-network disagreement, impact-based signals, and competence-progress principles for this purpose [2,6,13,15].

The study used a composite intrinsic score with two components: feature-space impact and region-local learning progress. Impact was computed from latent-state displacement across consecutive observations, while learning progress was derived from short-horizon and long-horizon error trends of a forward dynamics model. To reduce scale sensitivity across environments and training phases, each component was normalized online using running root-mean-square statistics before weighted combination.

Two variants were evaluated. GLPE (no gate) used the combined intrinsic score directly. GLPE introduced a region-specific binary gate that suppressed intrinsically attractive regions when prediction error remained high and measured local learning progress remained low. Gate updates used persistence and hysteresis conditions based on robust cross-region thresholds.
