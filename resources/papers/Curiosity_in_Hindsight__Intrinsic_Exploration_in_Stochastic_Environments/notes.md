# Curiosity in Hindsight: Intrinsic Exploration in Stochastic Environments

> **Link**: <https://doi.org/10.48550/arXiv.2211.10515>

> **Parenthetical**: (Jarrett et al., 2022)
> **Narrative**: Jarrett et al. (2022)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Motivation**  
  > “In the curiosity-driven paradigm, the agent is rewarded for how much each realized outcome differs from their predicted outcome. But using predictive error as intrinsic motivation is fragile in stochastic environments, as the agent may become trapped by high-entropy areas of the state-action space, such as a ‘noisy TV’.”

- **Core Idea: Curiosity in Hindsight**  
  The paper proposes adding **hindsight representations** that capture exactly the unpredictable aspects of environment transitions. By conditioning a learned reconstructor on these additional variables, the agent’s intrinsic reward “filters out” irreducible noise (pure randomness), ensuring curiosity is driven only by actual novelty or learnable dynamics.

- **Stochasticity Issues in Curiosity**  
  > “A classic example is the problem of a ‘noisy TV,’ which generates a stream of intrinsic rewards around which predictive-error-based agents become stuck indefinitely. [...] Our key idea is to learn representations of the future that capture precisely the unpredictable aspects of each outcome—no more, no less—so that the agent’s intrinsic rewards vanish in the limit for irreducible noise.”

- **MDP Setup**  
  Agents operate on state \(X\), action \(A\), with transitions \(X_{t+1}\sim \tau(\cdot \mid x_t, a_t)\). Traditional curiosity methods use predictive error:  
  \[
    R_\eta(x_t,a_t) \;=\; -\,\mathbb{E}\Bigl[\log \tau_\eta(X_{t+1}\mid x_t,a_t)\Bigr],
  \]  
  or similar variants (e.g. BYOL-Explore). This approach fails in partially random domains because the environment’s inherent noise keeps prediction error high.

- **Structural Causal Model**  
  The environment is viewed as a deterministic function \(x_{t+1} = f(x_t, a_t, z_{t+1})\) plus a latent random variable \(z_{t+1}\). If that variable were observed, the next state would be perfectly predictable. Hence, the unpredictability is purely “in the latent.” By training a model that reconstructs \(x_{t+1}\) given \((x_t,a_t,z_{t+1})\), plus a generator that samples “hindsight” vectors \(z_{t+1}\) from a posterior, the agent eliminates irreducible noise from its curiosity signal.

- **Disentangling Noise from Novelty**  
  The agent uses two main objectives:
  1. **Reconstruction Loss**:  
     \[
       L_{\mathrm{rec}} = \bigl\|x_{t+1} - f_\eta\bigl(x_t, a_t, z_{t+1}\bigr)\bigr\|^2,
     \]  
     encouraging \((x_t,a_t,z_{t+1})\) to reconstruct outcomes.
  2. **Invariance Loss** (contrastive form):  
     \[
       L_{\mathrm{inv}} = \mathrm{PMI}_\theta(x_t,a_t; z_{t+1}),
     \]  
     or a practical approximation with negative samples. It ensures \(z_{t+1}\) does not redundantly store what is already predictable from \((x_t,a_t)\).  

  Combined:
  \[
    R_{\theta,\eta}(x_t,a_t) \;=\; \frac{1}{\lambda} R_{\mathrm{rec}} + R_{\mathrm{inv}},
  \]
  gives an intrinsic reward that converges to zero if the environment’s transitions become fully explained by the reconstructive model *plus* the latent capturing irreducible noise.  

- **Contrastive Loss for Invariance**  
  A learned critic \(g_\nu\) is used in a standard contrastive manner, taking negative samples from a batch. This ensures that \(z_{t+1}\) remains conditionally independent of \((x_t,a_t)\). The net effect: the agent’s intrinsic reward does *not* stay high for random outcomes, preventing noisy-TV traps.

- **Instantiating with BYOL**  
  The authors introduce **BYOL-Hindsight**—a variant of BYOL-Explore that replaces forward predictions with a reconstructor. The difference:
  1. In BYOL-Explore, the model tries to predict next latent states from \((x_t,a_t)\).  
  2. In BYOL-Hindsight, the agent also samples a “hindsight” variable \(z_{t+1}\) from a generator, enabling it to reconstruct the next state in a way that discounts irreducible noise.

- **Key Theoretical Result**  
  > “By choosing a sufficiently small \(\lambda\), curiosity in hindsight becomes an upper bound on the KL divergence \(\mathrm{DKL}\bigl(\tau\|\tau_{\theta,\eta}\bigr)\) between the real dynamics and the learned model—thus approximating ‘optimistic’ exploration. Furthermore, the intrinsic reward vanishes when the model captures all learnable transitions.”

- **Experiments**  
  1. **Pycolab Maze**: Agents face random oscillators (Brownian blocks), random pixel noise, or action-dependent random noise. BYOL-Explore is easily trapped by irreducible randomness. BYOL-Hindsight navigates more effectively, ignoring unlearnable transitions.  
  2. **Bank Heist**: Some events are unpredictable (bombs, bank respawns), so BYOL-Explore repeatedly triggers them. BYOL-Hindsight outperforms in both intrinsic-only and mixed (extrinsic + intrinsic) reward settings.  
  3. **Montezuma’s Revenge** (with sticky actions for partial randomness): BYOL-Explore collapses. BYOL-Hindsight obtains near state-of-the-art exploration performance, significantly surpassing the baseline in a stochastic version. In the non-sticky (deterministic) version, BYOL-Hindsight matches the baseline’s strong performance.  
  4. **Hard Exploration Atari**: On 10 challenging games with sticky actions, BYOL-Hindsight often substantially improves over standard BYOL-Explore, confirming the method’s robustness to partial randomness.

- **Implementation Details**  
  - The agent runs a **recurrent** architecture that processes a history of observations \((o_t)\) and actions \((a_t)\).  
  - For each observed transition, a **generator** network samples \(z_{t+1}\), a **reconstructor** network tries to reconstruct the next latent representation, and a **critic** enforces that \(z_{t+1}\) does not store what is predictable from \((x_t,a_t)\).  
  - The method plugs seamlessly into standard RL algorithms (VMPO, etc.) to optimize the policy with the resulting intrinsic rewards.

---

### Concise Summary of the Article

**"Curiosity in Hindsight"** addresses a core weakness of **predictive-error-based** curiosity in stochastic domains: standard methods inflate their exploration bonus around intrinsically random transitions (the “noisy TV” problem). The authors provide:

1. **Causal Rationale**: Factor environment stochasticity into a latent \(z_{t+1}\). In an ideal scenario, everything about \(x_{t+1}\) is determined by \((x_t,a_t,z_{t+1})\).  
2. **Hindsight Representations**: The agent infers a “posterior sample” \(z_{t+1}\) after seeing the actual outcome. This is used in a reconstruction objective, ensuring the irreducible randomness is “accounted for” in the model.  
3. **Contrastive Invariance**: They add a mutual-information penalty that prevents storing any *predictable* aspects in \(z_{t+1}\). Only irreducible noise is captured.  
4. **Drop-In for Curiosity**: They demonstrate a direct integration with the recent **BYOL-Explore** algorithm, calling the result **BYOL-Hindsight**.  
5. **Strong Results**: On stochastic versions of Atari (sticky actions), the new method avoids being trapped by random events. It preserves or exceeds performance on deterministic tasks. On Montezuma’s Revenge with sticky actions, it achieves state-of-the-art exploration.

Hence, the approach elegantly **filters out** unlearnable “noise,” letting curiosity target only truly novel or complex-but-learnable transitions. The theoretical analysis shows that the new intrinsic reward upper-bounds the model’s deficiency in capturing environment dynamics—and converges to zero once the agent “understands” everything that is learnable.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Core Problem—Noisy TV**: Precisely the scenario of partial randomness is addressed. Standard curiosity methods get stuck in random states with high entropy. The authors propose **hindsight** latents that decouple irreducible noise from predictable novelty.  
- **Adaptive Curiosity**: Their approach adaptively reduces exploration bonuses in environment regions dominated by noise while maintaining strong incentives for genuinely learnable transitions. This directly aligns with the research theme of “Adaptive Curiosity for Exploration in Partially Random RL.”  
- **Generality**: The technique can drop into most curiosity-driven frameworks, making it broadly applicable. Their focus on single-step or multi-step reconstructions is relevant to varied partially stochastic tasks.

Hence, **the paper is highly relevant** for projects investigating robust exploration under partial environment randomness.

---

### Worth Citing?

**Yes.** It offers a theoretically grounded and empirically validated solution to the fundamental “noisy TV” failure mode of curiosity-based RL. The authors show that:

1. The method *retains good exploration* in deterministic tasks (no performance degradation).  
2. In the presence of partial randomness, it *avoids infinite curiosity loops*.  
3. The approach *integrates easily* with existing representation learning schemes (e.g. BYOL).  

---

### How It May Inform Future Research

1. **Combining Hindsight with Other Curiosity Signals**  
   Researchers might embed the proposed “latent noise channel” into other frameworks (ICM, RND) or into advanced model-based RL (Plan2Explore, Dreamer) to handle partial noise better.
2. **Scaling to Complex Robotics or Multi-Agent**  
   Real-world robotics often has sensor and actuator noise; employing “hindsight latents” may elegantly handle such partial randomness. Similarly, multi-agent environments have actions from other players that appear random.  
3. **Hybrid Uncertainty Decompositions**  
   Future directions might combine ensemble disagreement (epistemic uncertainty) with these learned noise latents (aleatoric uncertainty) to produce more stable, balanced exploration strategies.
4. **Beyond Single-Step**  
   The authors mention multi-step open-loop reconstructions. More advanced sequence modeling or hierarchical approaches might push further improvements in partially observed or deeply stochastic domains.

---

### Open Questions or Possible Critiques

- **Representation Leakage**  
  The invariance constraint relies on a learned critic. In complex tasks, does the critic adequately detect leaked information about \((x_t,a_t)\)? Could partial leakage hamper exploration or produce suboptimal reconstructions?  
- **Model Capacity vs. Noise**  
  If environment randomness is extremely high-dimensional or the reconstructor is underpowered, might the agent still conflate irreducible noise with novelty?  
- **Long-Horizon Planning**  
  The proposed method focuses primarily on single-step or short multi-step transitions. Truly multi-step partial randomness might require more elaborate hierarchical or memory-based expansions.  
- **Real-World Deployment**  
  The experiments center on grid worlds and Atari. Further validation in robotics or multi-agent tasks would confirm the method’s practicality and reliability under real sensor or actuator noise.
