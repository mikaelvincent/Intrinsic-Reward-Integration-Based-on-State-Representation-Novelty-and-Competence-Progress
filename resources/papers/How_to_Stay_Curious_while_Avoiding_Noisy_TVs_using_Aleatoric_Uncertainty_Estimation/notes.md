# How to Stay Curious while Avoiding Noisy TVs using Aleatoric Uncertainty Estimation

> **Link**: <https://doi.org/10.48550/arXiv.2102.04399>

> **Parenthetical**: (Mavor-Parker et al., 2021)
> **Narrative**: Mavor-Parker et al. (2021)

---

## Selected Direct Quotes and Formulas

- **Motivation**  
  > “When extrinsic rewards are sparse, artificial agents struggle to explore an environment. Curiosity, implemented as an intrinsic reward for prediction errors, can improve exploration but it is known to fail when faced with action-dependent noise sources (‘noisy TVs’).”

- **Aleatoric Mapping Agents (AMAs)**  
  The paper’s primary contribution is a form of curiosity-driven exploration called **Aleatoric Mapping Agents (AMAs)**. AMAs learn to predict **both** the mean \(\hat{\mu}_{t+1}\) and the aleatoric uncertainty \(\hat{\Sigma}_{t+1}\) of the next state. The intrinsic reward function then subtracts this estimated (predictable) uncertainty from the total prediction error, thereby reducing reward for inherently unlearnable stochastic transitions:
  \[
  r_t^i \;=\; \|s_{t+1} - \hat{\mu}_{t+1}\|^2 \;-\; \eta \,\mathrm{Tr}\bigl(\hat{\Sigma}_{t+1}\bigr),
  \]
  where \(\mathrm{Tr}(\cdot)\) denotes the trace of the diagonal covariance, and \(\eta\) is a hyperparameter controlling how strongly the agent penalizes predicted uncertainty.

- **Heteroscedastic Aleatoric Uncertainty**  
  The authors model the likelihood of the next state as a Gaussian with a diagonal covariance:
  \[
  N(s_{t+1} \mid f_{\theta}(s_{t}, a_{t}),\,g_{\phi}(s_{t}, a_{t})),
  \]
  learning parameters \(\theta\) and \(\phi\) online by maximizing the log-likelihood (or equivalently minimizing the negative log-likelihood). The key cost function for the AMA predictions follows Kendall & Gal (2017):
  \[
  L(\theta, \phi) \;=\; \bigl(s_{t+1} - \hat{\mu}_{t+1}\bigr)^\top \hat{\Sigma}_{t+1}^{-1} \bigl(s_{t+1} - \hat{\mu}_{t+1}\bigr)
  \;+\;\lambda \,\log \bigl(\det (\hat{\Sigma}_{t+1})\bigr).
  \]
  Here, \(\lambda\) is a hyperparameter that controls how “broad” the model’s uncertainty budget is.

- **Noisy TV Problem**  
  > “A naively curious agent could dwell on the unpredictability of a noisy TV screen.”  
  Existing curiosity methods (ICM, RND, etc.) often fail when the *stochastic transitions* are influenced by agent actions—i.e., the agent can keep triggering random transitions. AMAs directly address this trap by decreasing reward when the randomness is recognized as aleatoric (unpredictable noise).

- **Main Findings**  
  1. **AMAs vs. MSE**: Subtracting predicted uncertainty prevents exploring agents from being stuck in regions with action-dependent noise.  
  2. **Comparison with Baselines**: In standard RL exploration benchmarks (MiniGrid, Mario, Space Invaders, Bank Heist, etc.), AMAs match or exceed the state coverage of simpler pixel-based forward dynamics (MSE curiosity) when no noisy TV is present—and drastically outperform them (and sometimes other strong baselines like RND) when a “noisy TV” is introduced.  
  3. **Natural Stochastic Trap**: Even Atari games can contain inherent random transitions (Bank Heist’s bank resets, random police chases). Agents rewarded for raw prediction error can get stuck. AMAs avoid repeated exploitation of unlearnable transitions.

---

## Concise Summary of the Article

This work addresses a longstanding pitfall of curiosity-driven exploration known as the “noisy TV problem,” in which an RL agent that treats raw prediction error as an intrinsic reward becomes entrapped by random transitions yielding infinite novelty. **Aleatoric Mapping Agents (AMAs)** propose a simple yet effective fix:

1. **Double-Headed Prediction Network**  
   A neural network simultaneously predicts the mean and diagonal covariance (aleatoric uncertainty) of the next state.

2. **Intrinsic Reward Function**  
   The agent is rewarded for *epistemic* uncertainties (learning-related errors) while **discounting** transitions that are recognized as fundamentally random or uncontrollable (aleatoric uncertainties).

3. **Empirical Validation**  
   The authors compare AMAs to popular methods:
   - **MSE Curiosity** (forward dynamics in raw or feature space),  
   - **Random Network Distillation** (RND),  
   - **Inverse Dynamics Feature** (IDF),  
   - **Ensemble Disagreement** approaches.  
   AMAs consistently avoid the trap of action-induced noise across a range of tasks (Gym MiniGrid, classic Atari, and Retro Mario environments).

4. **Interpretation in Neuroscience**  
   The paper draws parallels to neuromodulatory signals in the brain, suggesting that acetylcholine might encode *expected* uncertainty (possibly aleatoric), while norepinephrine signals *unexpected* or epistemic uncertainty.

Thus, AMAs constitute a straightforward extension of curiosity-driven RL that remains robust to random disruptions, thereby broadening the applicability of prediction-based exploration methods.

---

## Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Noise vs. Novelty**  
  Adaptive curiosity often aims to guide exploration in ways that are robust to partially random or noise-laden transitions. AMAs directly tackle this problem by separating “unlearnable” randomness from learnable dynamics.
- **Action-Dependent Stochasticity**  
  In partially random RL settings, some transitions may be neither purely deterministic nor purely uncontrollable. AMAs illustrate how subtracting aleatoric noise can help the agent concentrate on states where knowledge can actually improve.

**Hence, this paper is highly relevant**: it offers practical techniques and conceptual insights on how to maintain genuine curiosity without being lured by random transitions.

---

## How It May Inform Future Research

1. **Combining AMAs with Other Feature-Based Curiosity**  
   Future work could embed aleatoric uncertainty estimation into more advanced curiosity frameworks (e.g., RND or ICM in a learned feature space) to handle partial randomness while keeping the benefits of state-of-the-art exploration signals.
2. **Application to Real Robotics**  
   Real-world robotic tasks commonly contain partial observability and sensor noise. AMAs could be integrated to detect irreducible environment uncertainties and avoid wasted exploration time.
3. **Online Hyperparameter Tuning**  
   The authors note that hyperparameters \(\lambda\) and \(\eta\) influence how readily the agent attributes transitions to aleatoric uncertainty. Automatic or adaptive methods for tuning these hyperparameters could further stabilize exploration.

---

## Open Questions or Critiques

- **Reliability of Uncertainty Estimates**  
  Aleatoric uncertainty is only valid if the agent’s model remains well-calibrated for out-of-distribution data. If states or transitions become very novel, uncertainty predictions might be incorrect.
- **Long-Horizon Tasks**  
  The approach focuses on immediate one-step transitions. Tasks with significant partial observability or multi-step dependencies could require recurrent models or memory-based uncertainty estimation.
- **Non-Stationary Rewards**  
  Like most curiosity-driven methods, AMAs generate a moving target for RL algorithms. More research into stable training protocols or trust-region approaches might improve long-term performance.

Given the strong empirical performance and the direct relevance to robust curiosity in stochastic environments, **this paper is well worth citing** for any project focusing on “Adaptive Curiosity for Exploration in Partially Random RL Environments.”
