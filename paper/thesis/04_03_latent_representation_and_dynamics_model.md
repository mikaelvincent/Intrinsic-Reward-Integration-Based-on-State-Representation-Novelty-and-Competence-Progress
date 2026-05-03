### 4.3 Latent Representation and Dynamics Model Intrinsic computation relied on a learned latent dynamics model. Observations were encoded as \(z_t=\phi_\omega(o_t)\), then used by a forward predictor \(f_\psi(z_t,a_t)\) to estimate \(z_{t+1}\), and by an inverse predictor \(g_\xi(z_t,z_{t+1})\) to infer action information [13],. The inverse model was treated as a classifier in discrete-action tasks and as a Gaussian-likelihood model in continuous-action tasks. Training used the composite objective
\[
\mathcal{L}_{\mathrm{dyn}}(t)=\beta_{\mathrm{fwd}}\mathcal{L}_{\mathrm{fwd}}(t)+\beta_{\mathrm{inv}}\mathcal{L}_{\mathrm{inv}}(t),
\]
with positive coefficients for forward and inverse losses. The forward loss used mean squared error in latent space,
\[
\mathcal{L}_{\mathrm{fwd}}(t)=\frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2,
\]
and per-transition prediction error was defined as \(e_t=\mathcal{L}_{\mathrm{fwd}}(t)\) [13],. For vector-observation tasks in the experiment suite, the encoder used a two-layer multilayer perceptron with 256 hidden units per layer and produced a 128-dimensional latent feature. Dynamics modules were optimized with Adam at learning rate \(3\times10^{-4}\), with intrinsic-model gradient clipping at 5.0.
