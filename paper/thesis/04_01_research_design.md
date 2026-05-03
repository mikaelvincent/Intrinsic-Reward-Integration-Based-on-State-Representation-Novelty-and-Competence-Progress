### 4.1 Research Design

The study used an experimental comparative design in which two proposed methods, GLPE and GLPE (no gate), were evaluated against five baseline methods: Vanilla PPO, ICM, RND, RIDE, and RIAC [2,6,13,15,18,19]. The core objective was to determine whether combining feature-space impact and region-local learning progress, with or without region-specific gating, improved exploration behavior and downstream control performance under fixed training conditions.

A within-environment control strategy was applied. For each environment, all methods used the same PPO architecture, optimizer family, discounting setup, and total interaction budget. Training and evaluation seeds were aligned across methods, and deterministic evaluation actions were used at each saved checkpoint. This design reduced confounding effects from policy backbone differences and focused comparison on intrinsic reward formulation [18,19].

Performance was analyzed from both sample-efficiency and computational-efficiency perspectives. Sample efficiency was examined through learning curves versus environment steps, final-checkpoint return, and step-normalized area under curve. Computational efficiency was examined through wall-clock AUC and per-component runtime decomposition [18]. Reliability was further examined using threshold-based reach rates and steps-to-threshold summaries across seeds .
