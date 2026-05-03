### 3.2 Reinforcement Learning Objective

In policy-gradient reinforcement learning, parameters are updated to maximize expected return under the current policy distribution. The study used an augmented per-transition reward,
\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}),
\]
where \(r_t^{\mathrm{int}}\) denotes intrinsic reward, \(\eta_t\) controls intrinsic strength, and \(r_{\max}\) bounds intrinsic magnitude. This formulation is consistent with reward shaping practices that preserve task-directed optimization while improving exploration behavior [9].

For GLPE-family methods, intrinsic weight was optionally annealed by a cosine schedule over training progress, so intrinsic guidance was emphasized in earlier phases and reduced later when exploitation became more important. Intrinsic rewards were set to zero on environment-terminal transitions to avoid dependence on termination artifacts [19].
