### 4.8 Algorithmic Workflow

Per PPO iteration, the workflow followed four stages. First, on-policy transitions were collected from vectorized environments until the target batch size was reached. Second, intrinsic quantities were computed per transition from latent dynamics outputs, region statistics, normalization states, and, for GLPE, gate states. Third, augmented rewards were formed, advantages and value targets were computed with GAE, and rollout data were prepared for optimization. Fourth, policy and value networks were updated through multi-epoch PPO minibatch optimization, while intrinsic-model parameters were updated once on the same on-policy batch [16-18].

Intrinsic and region-level states were updated online during transition processing. These included partition-tree assignments and splits, EMA statistics, RMS accumulators, gate counters, and gate states when applicable. The use of shared on-policy data for both policy optimization and intrinsic-model updates aligned training signals temporally and avoided off-policy replay dependencies [9], [13], [16], [18].

A full pseudocode view of the intrinsic computation pipeline was provided in the source paper's algorithm figure, and the thesis narrative retained the same operational sequence to ensure implementation consistency with reported experiments [18].
