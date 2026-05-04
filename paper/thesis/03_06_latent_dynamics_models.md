### 3.6 Latent Dynamics Models

Intrinsic quantities were computed from a learned latent representation rather than privileged simulator state. An encoder ϕ_ω mapped observations to latent vectors z_t, a forward model f_ψ predicted z_{t+1} from (z_t,a_t), and an inverse model g_ξ predicted action information from (z_t,z_{t+1}), following curiosity-driven representation learning practice [13].

Model training used a weighted sum of forward and inverse objectives. The forward prediction error

\[
e_t = \frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2
\]

served as the local difficulty signal for learning-progress estimation. This design linked intrinsic reward computation to model improvement dynamics in representation space [13,15].
