# EX2: Exploration with Exemplar Models for Deep Reinforcement Learning

> **Authors**: Justin Fu, John D. Co-Reyes, Sergey Levine
> **Date**: 27 May 2017
> **Link**: <https://doi.org/10.48550/arXiv.1703.01260>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **On Sparse Reward Challenges**  
  > “Sparse reward problems remain a significant challenge [for deep RL]. Exploration methods based on novelty detection have been particularly successful in such settings [...] We propose a novelty detection algorithm for exploration that is based entirely on discriminatively trained exemplar models.”  

- **Core Discriminative Idea**  
  > “We train classifiers to discriminate each visited state against all others. Intuitively, novel states are easier to distinguish from previously seen states.”  

- **Implicit Density Estimation**  
  The authors show that *exemplar models* (one classifier per state) can approximate state *densities* without explicitly building generative models. For a discrete distribution \(P_X\), if \(D_x(\cdot)\) is the classifier for an exemplar \(x\), then:
  \[
    D_x(x) \;=\;\frac{\delta_x(x)}{\delta_x(x) + P_X(x)} 
    \quad \implies \quad
    P_X(x) \;=\;\frac{1 - D_x(x)}{D_x(x)}.
  \]
  In continuous spaces, a noisy variant is introduced to provide smoothing.

- **Policy Bonus from Pseudo-Counts**  
  The method assigns an intrinsic reward (bonus) derived from the log of the implicit density estimate:
  \[
    \text{bonus}(s) \;=\; \alpha\,\log\bigl(\hat{p}(s)^{-1}\bigr),
  \]
  where \(\hat{p}(s)\) is estimated via exemplar-based discriminators. Thus, states that are “rare” (low density) get a higher reward for exploration.

- **Amortized and K-Exemplar Models**  
  - **Amortized**: A single discriminator *conditioned* on a reference state (the exemplar).  
  - **K-Exemplar**: Each discriminator handles a small batch \(K\) of positive states. Shared layers reduce overhead, final linear layers differ among exemplars.

- **Relationship to GANs**  
  The policy is seen as a “generator” producing states, while each exemplar discriminator attempts to separate those states from older replay-buffer states:
  > “However, [...] the policy is rewarded for *helping* the discriminator classify states as distinct, rather than fooling it, forming a cooperative rather than adversarial game.”

- **Experimental Highlights**  
  1. **2D Maze**: Visual validation of implicit density matches histogram-based ground truth.  
  2. **Continuous Control**: On SwimmerGather and SparseHalfCheetah, EX2 (discriminative) competes strongly with VIME and hashing-based methods, outperforming naive RL.  
  3. **Atari**: On sparse reward games (Freeway, Frostbite, Venture), EX2 matches or exceeds prior generative methods.  
  4. **vizDoom MyWayHome+**: A 3D, egocentric, partial-observation environment. EX2 *greatly* outperforms generative-based exploration, reaching deeper novel states.

- **Limitations and Insights**  
  - *Overfitting vs. Underfitting*: Because the discriminators can easily overfit in high-dimensional spaces, the authors use noise injection or latent smoothing to control generalization.  
  - *Computational Efficiency*: A single classifier per state is infeasible for large-scale tasks, leading to the amortized and K-exemplar variants.  
  - *Future Directions*: Automatic tuning of smoothing hyperparameters, applying the implicit density approach to other domains like off-policy RL or advanced curiosity-driven tasks.

---

### Concise Summary of the Article

In **“EX2,”** Fu et al. propose a **discriminative** approach to exploration in reinforcement learning, aimed at addressing sparse reward challenges. Instead of modeling state distributions with a **generative** model, they train **exemplar models**—classifiers distinguishing each “new” state (exemplar) from all “old” states stored in a replay buffer. They show this amounts to **implicit density estimation**: a well-trained discriminator’s output can be mapped to a pseudo-count measure that indicates novelty. A high novelty bonus is assigned to states that are easy to distinguish from previously visited ones.

To ensure scalability, the authors devise:
1. **Amortized** discriminators: a single network conditioned on the target exemplar, rather than training one classifier per state from scratch.
2. **K-Exemplar** models: grouping states into small batches to share partial classifiers.

Empirical results on continuous control tasks (2D maze, SwimmerGather, SparseHalfCheetah) and pixel-based tasks (Atari games, vizDoom) confirm that EX2 competes with or surpasses generative-model-based exploration. Especially in **vizDoom**—a high-complexity, first-person environment—EX2 significantly outperforms prior approaches, highlighting the advantage of discriminative novelty detection over complicated generative modeling.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: By focusing on *distinguishability*, EX2 reduces the risk of indefinite exploration of purely random states. Once a “noisy” state recurs, the discriminators quickly incorporate it into the replay buffer, diminishing novelty bonuses for unlearnable transitions.  
- **Adaptive Curiosity**: EX2’s **implicit density** approach parallels adaptive curiosity: it automatically shifts attention toward states unmodeled by the discriminators, ignoring truly stochastic phenomena over time.  
- **Large-Scale Feasibility**: The K-exemplar and amortized schemes make high-dimensional tasks tractable. This is crucial in partially random real-world settings, where generative approaches might fail to model the environment’s complex or noisy aspects.

**Conclusion**: EX2 offers a practical, discriminative path toward exploration that can sidestep pitfalls of environment noise, aligning well with research on robust curiosity in partially random domains.

---

### Worth Citing?

**Yes.** EX2 is a strong contribution for:
- *Novelty detection without generative modeling.*
- *Implicit density estimation through exemplar discriminators,* bridging count-based exploration and deep RL.
- *Empirical success* on challenging, visually complex tasks (vizDoom).  

Researchers seeking **robust exploration** in the presence of partial randomness will find EX2’s discriminative approach relevant and potentially simpler to train than forward-model or reconstruction-based methods.

---

### How It May Inform Future Research

1. **Hybrid or Multi-Method Curiosity**  
   EX2 can be combined with ensemble disagreement or count-based methods to mitigate each method’s flaws in partially random tasks.
2. **Hierarchical RL**  
   Discriminator-based novelty signals might guide skill discovery or meta-controller exploration to surmount extremely sparse or multi-room settings with partial observability.
3. **Scaling Up Real-World Applications**  
   The approach could be tested on real-robot tasks where sensor noise is prevalent. EX2’s discriminators might adapt quickly to repeated “random” observations, preventing curiosity from locking onto unlearnable phenomena.
4. **Adaptive Smoothing**  
   Automating the noise or smoothing hyperparameters, which balance underfitting vs. overfitting, could make the method more robust in continuously changing environments.

---

### Open Questions or Possible Critiques

- **High-Dimensional Classifier Training**  
  Frequent classifier updates may be costly for larger image inputs; improvements in amortized architectures or distillation are needed.
- **Overfitting**  
  Overly powerful discriminators can label minor differences as “novel,” artificially inflating the reward. More sophisticated or multi-scale smoothing strategies might help.
- **Long-Horizon Dependencies**  
  EX2 focuses on immediate novelty. Future work could incorporate multi-step planning or memory to handle tasks requiring extended exploration sequences.
- **Partial Observability**  
  In more severe partial-observation settings than those tested, learned discriminators might need recurrent or belief-state modeling to robustly handle hidden states.
