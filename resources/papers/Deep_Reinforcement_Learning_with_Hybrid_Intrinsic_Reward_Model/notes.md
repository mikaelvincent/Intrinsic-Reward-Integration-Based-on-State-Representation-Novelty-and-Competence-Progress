# Deep Reinforcement Learning with Hybrid Intrinsic Reward Model

> **Authors**: Mingqi Yuan, Bo Li, Xin Jin, Wenjun Zeng
> **Date**: 22 January 2025
> **Link**: <https://doi.org/10.48550/arXiv.2501.12627>

---

## Notes

### Selected Direct Quotes and Formulas

- **Motivation for Hybrid Intrinsic Rewards**  
  > “While single intrinsic rewards [...] often limit the diversity and efficiency of exploration, [...] the potential and principle of combining multiple intrinsic rewards remains insufficiently explored.”

- **Definition of the Hybrid Reward**  
  The authors augment the standard RL objective to combine multiple intrinsic reward functions \( \{ I_i \} \) using a fusion model \( f \). The new optimization objective is:  
  \[
    J^\pi(\theta) \;=\; \mathbb{E}_\pi \Biggl[\sum_{t=0}^\infty \gamma^t\,\Bigl(E_t + \beta_t\, f(I)\Bigr)\Biggr],
  \]  
  where \( \beta_t = \beta_0 (1 - \kappa)^t \) is a decaying coefficient, \( E_t \) is the extrinsic reward at time \( t \), and \( f(I) \) fuses the selected intrinsic signals.

- **Four Fusion Strategies**  
  The paper introduces four ways to unify multiple intrinsic rewards:

  1. **Summation (S):**  
     \[
       I_t \;=\; \sum_{i=1}^n w_i \, I_t^{(i)}.
     \]
  2. **Product (P):**  
     \[
       I_t \;=\; \prod_{i=1}^n I_t^{(i)}.
     \]
  3. **Cycle (C):**  
     \[
       I_t \;=\; I_t^{\,(j)}, \quad j = (t \,\mathrm{mod}\,n).
     \]
  4. **Maximum (M):**  
     \[
       I_t \;=\; \max\{ I_t^{(1)},\,I_t^{(2)},\dots,I_t^{(n)} \}.
     \]

- **Experimental Environments**  
  They evaluate in three benchmarks:  
  1. **MiniGrid** with grid-based navigation and sparse rewards.  
  2. **Procgen** with procedurally generated platform-like tasks.  
  3. **Arcade Learning Environment (ALE)** under an unsupervised RL setting (no extrinsic rewards during pre-training).

- **Key Findings**  
  1. The **Cycle** fusion strategy is generally the most robust.  
  2. **NGU** (Never Give Up) is often the most consistently beneficial single reward to include, combining episodic and lifelong novelty.  
  3. Hybrid rewards can outperform single intrinsic signals in both general RL and unsupervised RL tasks.  
  4. Combining three intrinsic rewards can offer good trade-offs in MiniGrid, whereas two-reward mixtures often suffice in Procgen.  
  5. More than three integrated rewards may impose heavy computational costs without consistent performance gains.

- **Computational Trade-Off**  
  > “HIRE configurations with up to three rewards strike a balance between exploration performance and computational cost.”

---

### Concise Summary of the Article

The paper tackles **hard-exploration** and **sparse reward** challenges in reinforcement learning (RL) by proposing **HIRE** (Hybrid Intrinsic REward). HIRE is a modular framework that combines any number of single intrinsic reward signals into a single hybrid bonus, through four fusion strategies: *Summation, Product, Cycle,* and *Maximum*. By systematically experimenting with several well-known curiosity/novelty baselines (ICM, NGU, RE3, E3B) across MiniGrid, Procgen, and unsupervised RL tasks in ALE, the authors reveal:

1. **Cycle strategy** achieves robust performance gains and adaptive exploration by periodically switching among motivations.  
2. **NGU** is especially effective, as it fuses episodic and global novelty. Pairing NGU with another approach (e.g., RE3) performs consistently well.  
3. Hybrid intrinsic rewards often outperform single reward methods, especially in tasks with high-dimensional or changing layouts.  
4. Users should limit the number of fused rewards (two or three) to keep computational overhead manageable while still reaping the benefits of diverse exploration signals.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random RL Environments"

- **Hybrid Approach for Partially Random Tasks**  
  The paper’s emphasis on combining diverse exploration signals (e.g., episodic vs. lifelong novelty, count-based vs. prediction-based) aligns with the goal of **adaptive curiosity** in noisy or partially random scenarios. Multiple intrinsic motives can help an agent stay engaged even when certain transitions are purely random, mitigating the overfitting to noise that can occur with a single curiosity metric.
- **Reduced Sensitivity to Single Failure Mode**  
  By fusing multiple reward signals, HIRE avoids the risk of relying on one approach that might fail in stochastic transitions. This “hybrid” perspective is valuable where some facets of the environment are random but others remain learnable.

Hence, **citing this work** is recommended, as HIRE provides a practical framework and empirical insights into how multiple curiosity-driven signals can be combined to improve robustness and efficiency in exploration—both relevant to partially random RL settings.

---

### How It May Inform Future Research

1. **Adaptive Weighting or Scheduling**  
   Explore how the fusion strategy might dynamically adjust weights (rather than fixed or cyclical) depending on the stage of training or the agent’s uncertainty.
2. **Integration with Skill Discovery**  
   HIRE is demonstrated mainly with curiosity/novelty-based signals. Future methods could incorporate skill-based or successor-feature-based explorations, investigating how multi-motivation setups further enhance coverage or task-agnostic skills.
3. **Real-World Robotics**  
   Deploying HIRE in real robot tasks may illuminate how hybrid rewards handle complex sensorimotor noise and partial observability.

---

### Open Questions or Critiques

- **Scalability to Larger Reward Sets**: The paper uses four single intrinsic rewards. Integrating more (5–6) might be interesting but becomes computationally expensive, potentially confusing the agent’s priorities.  
- **Complexity of Weight Tuning**: Although HIRE is flexible, the right weighting strategy remains non-trivial. Future work might investigate automated or learning-based approaches to mixing signals.  
- **Sparse vs. Dense Environments**: The tested benchmarks are known to be relatively sparse. Would results differ in dense-reward tasks, where the effect of added intrinsic bonuses may be overshadowed?
