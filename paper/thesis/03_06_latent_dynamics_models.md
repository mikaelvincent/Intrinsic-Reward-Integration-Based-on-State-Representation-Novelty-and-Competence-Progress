### 3.6 Latent Dynamics Models

Intrinsic signals were computed from learned latent representations rather than privileged environment state. An encoder \(\phi_\omega\) produced \(z_t=\phi_\omega(o_t)\). A forward predictor \(f_\psi\) estimated \(z_{t+1}\) from \((z_t,a_t)\), and an inverse predictor \(g_\xi\) modeled action information from \((z_t,z_{t+1})\) {{CIT:13}}.

Training minimized
\[
\mathcal{L}_{\mathrm{dyn}}(t)=\beta_{\mathrm{fwd}}\mathcal{L}_{\mathrm{fwd}}(t)+\beta_{\mathrm{inv}}\mathcal{L}_{\mathrm{inv}}(t),
\]
with forward error
\[
e_t=\mathcal{L}_{\mathrm{fwd}}(t)=\frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2.
\]
The scalar \(e_t\) was used as the primary signal for region-wise learning-progress estimation.
