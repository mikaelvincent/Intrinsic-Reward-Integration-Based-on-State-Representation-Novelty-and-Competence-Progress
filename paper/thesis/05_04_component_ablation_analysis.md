### 5.4 Component Ablation Analysis

Component ablations evaluated whether impact and learning-progress terms contributed differently across environments [18]. On MountainCar-v0, full GLPE obtained a final mean return of -96.2, while impact-only and LP-only variants fell to -111.8 and -106.6, respectively [18]. This gap indicated that combining both signals was important in sparse-reward exploration.

On Ant-v5, the impact-only variant reached 5233, exceeding full GLPE at 4961, while LP-only was lower at 4599 [18]. On BipedalWalker-v3, LP-only reached 298.8, closest to the solved cutoff of 300, and exceeded both full GLPE and impact-only in final-checkpoint mean return [18].

Taken together, the ablation results showed that no single intrinsic component was uniformly optimal across tasks. The combined GLPE score remained a robust default because task-specific dominance between impact and learning progress could not be assumed in advance [18].
