### 2.2 Novelty and Prediction-Error Methods

A major line of exploration research used novelty estimates to reward rarely visited or weakly modeled states. Count-based approaches formalized this idea through visitation frequencies and pseudo-counts, including density-model variants designed for high-dimensional observations [6], [7], [8]. These methods provided a principled exploration bonus and often improved state-space coverage.

Prediction-error curiosity provided a complementary strategy. Instead of explicit counts, these methods rewarded transitions whose outcomes were difficult for a learned forward model to predict [9]. Deep predictive exploration and later feature-space curiosity models, including ICM, operationalized novelty through model mismatch in learned representations [9]. Random Network Distillation used prediction error against a fixed random target network, yielding a simple and scalable novelty signal [10].

The common strength of novelty and prediction-error methods was broad exploratory pressure with minimal environment-specific engineering [6], [9], [10]. The common weakness was sensitivity to stochastic or chaotic dynamics where prediction error can remain high without yielding meaningful progress in task-relevant competence [11], [14]. This failure pattern is often described as unproductive curiosity and is exemplified by the noisy-TV effect [14].

These findings were directly relevant to the present thesis. They indicated that high surprise alone is not a sufficient criterion for useful exploration, and they motivated augmenting novelty-style signals with explicit estimates of whether model quality is improving locally over time [5], [13], [18].
