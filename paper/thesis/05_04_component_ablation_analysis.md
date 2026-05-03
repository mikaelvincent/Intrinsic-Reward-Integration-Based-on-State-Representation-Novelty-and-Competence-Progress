### 5.4 Component Ablation Analysis

Component ablations evaluated whether impact and learning-progress terms contributed differently across environments [18]. On MountainCar-v0, full GLPE obtained a final mean return of -96.2, while impact-only and LP-only variants fell to -111.8 and -106.6, respectively [18]. This gap indicated that combining both signals was important in sparse-reward exploration.

On Ant-v5, the impact-only variant reached 5233, exceeding full GLPE at 4961, while LP-only was lower at 4599 [18]. On BipedalWalker-v3, LP-only reached 298.8, closest to the solved cutoff of 300, and exceeded both full GLPE and impact-only in final-checkpoint mean return [18].

Taken together, the ablation results showed that no single intrinsic component was uniformly optimal across tasks. The combined GLPE score remained a robust default because task-specific dominance between impact and learning progress could not be assumed in advance [18].


Table 5.4. Final-checkpoint mean extrinsic return for GLPE and component ablations [18].

| Environment | GLPE | Impact-only | LP-only |
|---|---|---|---|
| MountainCar-v0 | -96.2 [-96.5,-95.9] | -111.8 [-137.0,-96.2] | -106.6 [-127.4,-96.0] |
| BipedalWalker-v3 | 266.5 [214.0,301.3] | 277.5 [256.0,296.5] | 298.8 [285.5,308.1] |
| Ant-v5 | 4,961 [4,421,5,359] | 5,233 [4,544,5,663] | 4,599 [3,617,5,401] |
