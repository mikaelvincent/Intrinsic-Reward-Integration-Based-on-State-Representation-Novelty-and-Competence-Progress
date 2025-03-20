# Curiosity-Driven Exploration via Latent Bayesian Surprise

> **Link**: <https://doi.org/10.48550/arXiv.2104.07495>

> **Parenthetical**: (Mazzaglia et al., 2021)
> **Narrative**: Mazzaglia et al. (2021)

---

## Notes

### Selected Direct Quotes and Formulas

- **On Bayesian Surprise**  
  > “Bayesian surprise [...] measures the difference between the posterior and prior beliefs of an agent, after observing new data.”  
  Specifically, the paper focuses on *latent* Bayesian surprise instead of parameter-space surprise:  
  \[
  r_t^{(i)} \;=\; I(z_{t+1}; s_{t+1} \mid s_t, a_t) \;=\; D_{\mathrm{KL}}\Bigl[q_\theta\bigl(z_{t+1}\mid s_t,a_t,s_{t+1}\bigr)\,\bigl\|\,p_\theta\bigl(z_{t+1}\mid s_t,a_t\bigr)\Bigr].
  \]

- **Latent Variable Model and Training Objective**  
  The paper describes a latent dynamics model. The future state \(s_{t+1}\) is predicted through a latent variable \(z_{t+1}\) with:
  \[
  p_\theta(z_{t+1} \mid s_t, a_t), \quad 
  q_\theta(z_{t+1} \mid s_t, a_t, s_{t+1}), \quad 
  p_\theta(s_{t+1} \mid z_{t+1}).
  \]
  They maximize a variational lower bound (ELBO) on \(\log p(s_{t+1} \mid s_t, a_t)\):
  \[
  \mathcal{J} \;=\;
  \mathbb{E}_{z_{t+1}\sim q_\theta}\Bigl[\log p_\theta\bigl(s_{t+1}\mid z_{t+1}\bigr)\Bigr]
  \;-\;\beta \,D_{\mathrm{KL}}\Bigl[q_\theta\bigl(z_{t+1}\mid s_t, a_t, s_{t+1}\bigr)\,\bigl\|\,p_\theta\bigl(z_{t+1}\mid s_t, a_t\bigr)\Bigr].
  \]
  Here, \(\beta\) is a weighting factor similar to \(\beta\)-VAE approaches.

- **NoisyTV Problem**  
  The authors highlight that standard “surprisal” metrics (prediction-error-based) can be misled by *stochastic* transitions, e.g., white noise:
  > “In contrast, Bayesian surprise [...] means that for stochastic transitions of the environment, which carry no novel information to update the agent’s beliefs, low intrinsic bonuses are provided, potentially overcoming the NoisyTV issue.”

- **Experiments**  
  - **Continuous Control**: Compared exploration performance on Mountain Car, Ant Maze, and HalfCheetah by counting discretized state-space coverage. LBS reached the highest coverage or performed on par with other strong baselines (ICM, Disagreement, VIME, RND).  
  - **Arcade Games**: On several Atari games plus Super Mario Bros., the authors compare LBS with pixel or feature-based “surprisal” methods. LBS shows better or at least on-par scores in most tests.  
  - **Stochastic Environments**: Further tests, including a synthetic “Noisy MNIST” transition and a “Noisy” version of Mountain Car, reveal that LBS remains robust under environment randomness, while some other methods continue to treat purely stochastic transitions as “novel.”

> “Our model is computationally cheap and compares positively with current state-of-the-art methods on several problems. [...] The results suggest that our approach is resilient to stochastic transitions.”

### Concise Summary of the Article

The paper proposes **Latent Bayesian Surprise (LBS)** as an intrinsic reward for reinforcement learning (RL). Instead of measuring surprise directly on model parameters, LBS applies Bayesian surprise in a latent variable that captures the environment’s dynamics. Specifically:

1. **Latent Variable Model**  
   The method trains a latent prior \(p_\theta(z_{t+1}\mid s_t,a_t)\) and a latent posterior \(q_\theta(z_{t+1}\mid s_t,a_t,s_{t+1})\), along with a reconstruction module \(p_\theta(s_{t+1}\mid z_{t+1})\).  

2. **Surprise Computation**  
   The intrinsic reward is the KL divergence between the latent posterior and prior, indicating “information gained” about latent variables when the new state arrives.

3. **Core Argument**  
   Such Bayesian surprise in latent space naturally de-emphasizes purely stochastic transitions that do not reduce uncertainty. It avoids the “NoisyTV” trap, in which simple prediction-error methods keep finding stochastic updates “interesting.”

4. **Results**  
   - In continuous control (Mountain Car, Ant Maze, HalfCheetah), LBS had superior or near-best exploration coverage.  
   - In pixel-based arcade games, LBS outperformed or matched multiple leading methods (ICM, RND, others) on final scores.  
   - The approach is more robust to randomness in the environment transitions than classical surprisal-based methods.

### Relevance to "Adaptive Curiosity for Exploration in Partially Random RL Environments"

- **Adaptive Curiosity Connection**  
  The LBS framework aligns with the concept of “adaptive curiosity,” where an agent focuses on transitions that truly reduce uncertainty about the world, rather than being driven by raw or noisy signals. Because LBS explicitly accounts for whether new data actually changes latent beliefs, it is highly relevant for partially random environments—precisely the scenario in which standard curiosity approaches fail.  

- **Benefits for Partially Random Settings**  
  The authors demonstrate resilience to environment noise. This property is vital for “partially random RL environments,” where certain transitions are uncontrollable or purely stochastic.  

- **Worth Citing?**  
  **Yes.** LBS directly addresses a major shortcoming of existing curiosity-based methods—namely, the confusion with randomness or “noisy transitions.” Since “Adaptive Curiosity for Exploration in Partially Random RL Environments” focuses on guiding exploration with partial randomness, LBS is an excellent reference for robust, Bayesian-inspired exploration.

### How It May Inform Future Research

1. **Latent-Space Uncertainty Quantification**  
   Future work might refine how latent variables encode environment uncertainties, e.g., through improved architectures, or incorporate confidence intervals for more sophisticated exploration strategies.

2. **Combining LBS with Other Exploration Methods**  
   There could be value in combining LBS with count-based or episodic memory approaches (like RIDE, NGU) to address both novelty in large, sparse domains and partial observability.

3. **Extended Usage in Model-Based RL**  
   The authors show promising “zero-shot adaptation” results by embedding LBS in Dreamer-like frameworks. Expanding this into more complex or real-world tasks can be a fruitful direction.

### Open Questions or Critiques

- **Scalability to Very High-Dimensional Tasks**  
  The authors note that “feature-based” (rather than raw-pixel-based) reconstruction generally performs better. Future work could explore large-scale or 3D tasks where pixel-perfect modeling is expensive, requiring more advanced latent representations (e.g., contrastive).

- **Long-Horizon Dependencies**  
  LBS focuses on immediate transitions. For tasks needing multi-step memory or partial observability, an extension with recurrent latent state might be required.

- **Exploration vs. Exploitation Balance**  
  The paper emphasizes purely intrinsic motivation. Integrating external task rewards might require dynamic weighting or scheduling of the curiosity term, something that remains open to further experimentation.
