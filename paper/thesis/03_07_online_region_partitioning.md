### 3.7 Online Region Partitioning

Learning progress was localized through an online partition of latent space. The partition was represented by a binary tree whose leaves defined adaptive regions. As embeddings accumulated in a leaf, splitting was triggered by capacity and depth criteria, and split rules were selected from coordinate variance with median thresholding to avoid degenerate partitions [2,19].

Each region maintained short-horizon and long-horizon exponential moving averages of prediction error. Region-local progress was defined as the positive part of the long-minus-short difference,
\[
\mathrm{LP}(r)=\max(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}),
\]
which became large when local predictive performance was improving. This mechanism adapted exploration pressure to nonstationary learning dynamics in different parts of feature space [2,19].
