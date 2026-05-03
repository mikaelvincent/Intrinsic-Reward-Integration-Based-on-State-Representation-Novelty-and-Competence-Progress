### 4.12 Evaluation Protocol

Evaluation used undiscounted episodic extrinsic return. Online evaluation during training was not performed. Instead, saved checkpoints were evaluated offline in separate environment instances using deterministic action selection based on distribution mode [18].

Each evaluated checkpoint was run for 20 episodes. Episode seeds were fixed per training seed to support consistent between-method comparison. Aggregation was performed across multiple independent training seeds per environment [18].

Checkpointing included step zero, additional warmup checkpoints within the initial interval, regular checkpoints at fixed fractions of total budget, and a final checkpoint at training completion. Scalar metrics were logged at fixed step intervals. This structure supported curve-level, threshold-level, and efficiency-level analyses from a common checkpoint record [18].
