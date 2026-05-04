### 3.8 Evaluation Metrics

Evaluation emphasized task performance and efficiency under common experimental budgets. Primary curves used extrinsic episodic return from deterministic policy evaluation at checkpoints during training.

Two scalar summaries were used for cross-method comparison. Step-AUC integrated return over environment interaction steps and was normalized by the step budget, which reflected sample efficiency. Wall-clock AUC integrated return over elapsed training time within a common time budget per environment, defined by the minimum final runtime among compared methods in that environment. This common-budget protocol prevented unfair extrapolation beyond measured runtimes and enabled runtime-aware comparison.
