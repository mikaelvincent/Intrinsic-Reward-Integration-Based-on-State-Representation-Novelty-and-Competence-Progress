### 4.8 Algorithmic Workflow

The intrinsic reward workflow followed the same sequence described in the source paper: latent encoding, forward-error computation, online region assignment, region-level EMA updates, impact and learning-progress normalization, weighted intrinsic-score construction, optional gating, and PPO optimization with augmented reward .

Figure 4.1. High-level pseudocode for computing GLPE-family intrinsic rewards within one PPO update .

```text
Input: on-policy transitions {(o_t, a_t, o_{t+1})}_{t=1}^N;
       encoder phi_omega; forward model f_psi; inverse model g_xi;
       region assignment rho; region EMAs; RMS accumulators; optional gate states
Output: intrinsic rewards {r_t^int}_{t=1}^N; updated region statistics; updated intrinsic model parameters

for t = 1 to N:
    z_t <- phi_omega(o_t), z_{t+1} <- phi_omega(o_{t+1})
    e_t <- (1/d) ||f_psi(z_t, a_t) - z_{t+1}||^2
    r <- rho(z_t), including insertion and split when needed
    update short and long EMAs for region r with e_t
    LP_t <- max(0, mu_long(r) - mu_short(r))
    I_t <- ||z_{t+1} - z_t||
    normalize I_t and LP_t with running RMS
    u_t <- alpha_impact * I_t_tilde + alpha_LP * LP_t_tilde
    if gating enabled:
        compute global medians across visited regions
        update gate state with persistence and hysteresis
        r_t^int <- g_r * u_t
    else:
        r_t^int <- u_t

update intrinsic model parameters using supervised forward and inverse losses
```
