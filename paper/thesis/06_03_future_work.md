### 6.3 Future Work

Future work may extend GLPE to richer observation modalities, including image-based inputs, where latent representation quality and dynamics-model calibration can affect both impact and progress estimates [6,13].

Additional investigation is warranted for off-policy or hybrid training regimes to determine whether the same intrinsic formulation preserves its practical advantages when replay dynamics, target networks, and update frequencies differ from PPO [19].

Adaptive gating mechanisms should be examined to reduce conservatism in high-variance environments while retaining protection against persistent noisy-error regions. Candidate directions include robust online threshold adaptation and confidence-aware region statistics grounded in existing uncertainty-aware exploration literature [8].

Computational refinement remains important for broader deployment. Follow-up work should evaluate efficient approximations for region statistics and update scheduling that reduce overhead without materially altering gating decisions or benchmark conclusions .

Broader benchmark coverage is also recommended, including more diverse sparse-reward tasks and additional continuous-control settings, so that generalization claims can be assessed under wider dynamics and reward structures .
