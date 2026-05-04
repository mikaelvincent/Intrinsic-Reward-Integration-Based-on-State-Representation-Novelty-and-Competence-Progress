### 2.1 Intrinsic Motivation in Reinforcement Learning

Intrinsic motivation in reinforcement learning refers to internally generated reward signals that complement environment rewards during policy optimization {{CIT:3,20}}. In sparse-reward settings, such auxiliary signals were used to encourage exploration before reliable extrinsic feedback became available {{CIT:11,12}}.

Early formulations described intrinsic behavior as seeking experiences that improve predictive competence rather than maximizing immediate external payoff {{CIT:17,20}}. Later taxonomies grouped intrinsic methods into families such as novelty seeking, prediction-error curiosity, information gain, and competence or progress based objectives {{CIT:1,11,12}}.

In deep reinforcement learning, intrinsic rewards were commonly implemented as additive shaping terms combined with extrinsic reward through a task-dependent coefficient {{CIT:6,13,15}}. This formulation was practical and often effective, but it generally did not preserve policy invariance because the shaping term could change trajectory preferences during optimization {{CIT:9}}. For this reason, intrinsic methods were typically assessed empirically using sample efficiency, final return, and reliability across random seeds {{CIT:15,18,19}}.

The literature established two observations relevant to this thesis. First, intrinsic rewards often improved early exploration and learning speed {{CIT:6,13,15}}. Second, intrinsic objectives could remain active in regions where surprise stayed high after useful learning had saturated, creating a mismatch between exploration pressure and task progress {{CIT:8}}. These observations motivated the present focus on progress-sensitive intrinsic shaping.
