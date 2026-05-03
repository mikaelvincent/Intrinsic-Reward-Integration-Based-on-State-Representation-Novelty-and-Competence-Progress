### 1.2 Statement of the Problem

Many intrinsic motivation methods improve exploration, but their signals can be misaligned with actual learning progress in sparse-reward or high-variance environments [10], [11], [13], [14]. As a result, agents may allocate substantial interaction budget to transitions that remain surprising without producing sustained policy improvement.

This study addressed the following problem: how to construct an intrinsic reward mechanism that preserves exploratory behavior while reducing unproductive curiosity, and how to evaluate its effectiveness relative to established baselines under both sample-efficiency and wall-clock-efficiency criteria [9], [16], [17], [18].

Specifically, the work examined whether combining feature-space impact with region-local learning progress, and optionally applying a region-specific gating mechanism, can yield reliable and competitive performance across sparse and dense reward benchmarks when trained with a common PPO backbone [9], [13], [16], [17], [18].
