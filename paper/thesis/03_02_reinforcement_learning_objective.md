### 3.2 Reinforcement Learning Objective

Policy parameters were optimized using rewards augmented by an intrinsic shaping term. For each transition, the scalar reward was defined as

\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}),
\]

where η_t controlled the intrinsic contribution and r_max bounded intrinsic magnitude. This bounded augmentation preserved a stable reward scale while allowing intrinsic guidance during exploration. Intrinsic reward was set to zero on environment-terminal transitions to avoid dependence on episode termination effects.

For GLPE-family methods, η_t could be annealed over training progress with a cosine taper, which emphasized exploration earlier in training and reduced intrinsic influence in later stages when policy exploitation became more important.
