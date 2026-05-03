### 6.2 Recommendations

For comparable low-dimensional continuous-control tasks trained with PPO, GLPE without gating should be considered the primary default configuration because it provided the best overall balance between consistency and performance across environments [19].

The gated variant should be prioritized when the task exhibits sparse or delayed extrinsic feedback and when instability from persistent high prediction error is expected. In such cases, region-wise suppression can improve reliability by reducing time spent in low-progress exploratory regimes [2,8].

Evaluation practice should retain multiple complementary views, including learning curves, step-normalized AUC, wall-clock AUC, and thresholded reliability at solved and reduced levels. This combined protocol avoids over-reliance on a single metric and better captures delayed attainment and variance-sensitive behavior .

Reporting of computational results should continue to separate algorithmic quality from implementation overhead. Runtime decomposition and explicit disclosure of optional optimizations, such as cached gating statistics, should be preserved so that comparisons remain interpretable and reproducible .

Future implementations should maintain consistency between shaping design and policy optimization settings by preserving explicit schedules for intrinsic scaling and by documenting hyperparameter choices in a task-aware manner [19].
