### 3.6 Latent Dynamics Models A latent dynamics module was used to produce intrinsic quantities from learned features rather than from privileged state variables. An encoder \(\phi_\omega\) mapped observations to latent vectors \(z_t\), a forward model \(f_\psi\) predicted \(z_{t+1}\) from \((z_t,a_t)\), and an inverse model \(g_\xi\) predicted action information from \((z_t,z_{t+1})\). Training minimized a weighted sum of forward and inverse losses [9,16]. Per-transition forward prediction error,
\[
e_t = \frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2,
\]
was treated as the core signal for learning-progress tracking. This design aligned with established curiosity frameworks, where representation learning and predictive modeling jointly shape exploratory behavior [9,11].
