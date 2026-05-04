### 1.2 Statement of the Problem

Many intrinsic motivation methods improved exploration, but their reward signals were not always aligned with actual learning progress in sparse reward or high variance environments {{CIT:2,6,8,15}}. Agents could therefore spend substantial interaction budget on transitions that remained surprising without producing sustained policy gains.

This thesis addressed the problem of constructing an intrinsic reward mechanism that preserves exploratory behavior while reducing unproductive curiosity, and of evaluating that mechanism against established baselines under both sample efficiency and wall clock efficiency criteria.

Specifically, the study examined whether combining feature space impact with region local learning progress, with optional region specific gating, can provide reliable and competitive performance across sparse and dense reward benchmarks under a common PPO backbone.
