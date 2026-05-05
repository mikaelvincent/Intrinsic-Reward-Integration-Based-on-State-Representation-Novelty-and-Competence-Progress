### 3.8 Evaluation Metrics

Evaluation emphasized extrinsic task performance and efficiency under fixed training budgets. Primary curves reported undiscounted episodic return over environment interaction, aggregated across random seeds per method.

Two scalar summaries were used. Step-AUC integrated return with respect to environment steps and normalized by the step budget, representing sample efficiency. Time-AUC integrated return with respect to cumulative wall-clock training time under a common time budget per environment, allowing direct comparison of learning efficiency when computational costs differed across methods.
