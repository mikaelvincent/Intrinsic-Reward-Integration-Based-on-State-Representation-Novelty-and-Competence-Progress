### 3.2 Reinforcement Learning Objective

Policy parameters were optimized under an augmented reward signal:
\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}).
\]
Here, \(r_t^{\mathrm{int}}\) denotes intrinsic reward, \(\eta_t\ge 0\) controls intrinsic contribution, and \(r_{\max}>0\) limits shaping magnitude. This construction preserved task reward as the primary objective while permitting bounded exploratory shaping {{CIT:9}}.

For GLPE-family methods, \(r_t^{\mathrm{int}}\) was set to zero on environment-terminal transitions. Intrinsic weight \(\eta_t\) was either fixed or scheduled over training progress, depending on configuration.
