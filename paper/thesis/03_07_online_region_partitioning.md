### 3.7 Online Region Partitioning

Learning progress was localized by maintaining an online partition of latent space. The partition was represented by a binary space-partitioning tree whose leaves defined active regions. As points accumulated in a leaf, splitting was triggered by capacity and depth constraints. The split dimension was selected from coordinate variance, and the split threshold was set by the median to avoid degenerate partitions.

For each region, short-horizon and long-horizon exponential moving averages of forward-model error were maintained. Region-local learning progress was defined as

\[
\mathrm{LP}(r)=\max\left(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}\right).
\]

This quantity increased when short-term error decreased relative to a slower baseline, indicating active model improvement in that region. The adaptive partition therefore provided locality for nonstationary exploration pressure, and supported region-specific gating in GLPE.
