### 3.8 Evaluation Metrics

Evaluation focused on extrinsic task performance and computational efficiency. Primary performance curves used undiscounted episodic return evaluated from offline checkpoints under deterministic action selection. Aggregation across multiple seeds provided mean trends and dispersion summaries per method and environment [16].

Two scalar curve summaries were used. Step-AUC integrated return against environment steps and normalized by step budget, which reflected sample efficiency. Wall-clock AUC integrated return against cumulative training time under a common time budget, defined as the minimum final runtime among compared methods in the same environment. This common-budget rule avoided extrapolation beyond measured runtime and enabled fair efficiency comparison [16].
