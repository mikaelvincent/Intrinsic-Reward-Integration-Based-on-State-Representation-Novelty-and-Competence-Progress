### 2.2 Novelty and Prediction-Error Methods

A major line of exploration research rewarded novelty in rarely visited or weakly modeled states. Count-based methods formalized this idea through visitation frequencies and pseudo-counts, including density-model extensions for high-dimensional observations {{CIT:4,10,22}}. Episodic reachability-based curiosity provided a related mechanism by rewarding experiences that expanded short-horizon behavioral coverage {{CIT:16}}.

Prediction-error curiosity provided a complementary strategy by rewarding transitions that were difficult for a learned forward model to predict {{CIT:13,21}}. Feature-space formulations, including ICM, operationalized novelty through model mismatch in learned representations {{CIT:13}}. Random Network Distillation used prediction error against a fixed random target network to produce a scalable novelty signal {{CIT:6}}. Related approaches included ensemble-disagreement and directed exploration variants {{CIT:1,14}}.

The common strength of novelty and prediction-error methods was broad exploratory pressure with limited environment-specific engineering {{CIT:4,6,13}}. The common weakness was sensitivity to stochastic or weakly learnable dynamics, where prediction error could remain high without corresponding task progress {{CIT:8,15}}. This failure mode is often described as unproductive curiosity, and the noisy-TV effect is a representative example {{CIT:8}}.

These findings were directly relevant to this thesis. They indicated that high surprise alone was not a sufficient criterion for useful exploration, and they motivated augmentation of novelty-oriented signals with explicit estimates of local model improvement over time {{CIT:2,17}}.
