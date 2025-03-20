# Self-Supervised Exploration via Disagreement

> **Link**: <https://doi.org/10.48550/arXiv.1906.04161>

> **Parenthetical**: (Pathak et al., 2019)
> **Narrative**: Pathak et al. (2019)

---

## Notes

### Selected Direct Quotes and Formulas

- **Motivation and Goal**  
  > “We propose a formulation for exploration inspired by the work in active learning literature. Specifically, we train an ensemble of dynamics models and incentivize the agent to explore such that the disagreement of those ensembles is maximized.”

- **Core Idea: Disagreement as Intrinsic Reward**  
  The method learns an ensemble of forward models \( f_1, f_2, \dots, f_k \), each predicting the next state \(\mathbf{x}_{t+1}\) from the current state \(\mathbf{x}_t\) and action \(\mathbf{a}_t\). The **intrinsic reward** is the variance among the model predictions:
  \[
  r_t^i \;=\; \mathbb{E}\Bigl[\bigl(f(\mathbf{x}_t,\mathbf{a}_t) - \mathbb{E}[f(\mathbf{x}_t,\mathbf{a}_t)]\bigr)^2\Bigr].
  \]
  > “Taking actions to maximize the model disagreement allows the agent to learn skills by exploring in a self-supervised manner without any external reward.”

- **Stochastic Environments**  
  > “In a stochastic scenario, a dynamic prediction model will converge to predicting the mean of different possible next states, and all models in the ensemble will eventually predict similarly. [...] Hence, the agent will not get stuck forever in purely noisy transitions.”

- **Differentiable Exploration**  
  Unlike most curiosity-based methods that rely on reinforcement learning for policy updates, the authors propose directly **optimizing** the policy via the gradient of the disagreement term itself.  
  \[
  \max_{\pi_\theta} \; \sum_{t=0}^T \gamma^t \; r_t^i,\quad \text{where } r_t^i \text{ depends on } f(\mathbf{x}_t, \pi_\theta(\mathbf{x}_t)).
  \]  
  > “Our intrinsic reward formulation [...] does not depend on the environment interaction at all, i.e., no dependency on \(\mathbf{x}_{t+1}\). It is purely a mental simulation of the ensemble of models based on the current state and the agent’s predicted action.”

- **Toy Example: Noisy MNIST**  
  The authors set up a simplified environment where states are MNIST digits. Transitions from certain digits lead deterministically to the same class, while transitions from others lead stochastically to multiple classes. A **prediction-error** approach remains high in the stochastic transitions, encouraging the agent to stay “stuck.” The disagreement-based method, however, converges to low intrinsic rewards in both deterministic and stochastic states, avoiding infinite curiosity loops.

- **3D Navigation and Atari with Sticky Actions**  
  In these stochastic benchmarks (e.g., TVs with random images, repeated or “sticky” actions in Atari), the authors demonstrate that maximizing disagreement avoids over-focus on randomness better than prediction-error-based curiosity.  

- **Real Robotics Experiment**  
  A 7-DOF Sawyer arm manipulates objects purely from an intrinsic reward. By optimizing a short-horizon differentiable model of the disagreement, the robot learns to interact with objects in under 1000 trials, compared to reinforcement-based approaches that fail to discover meaningful object interactions.

---

### Concise Summary of the Article

This paper proposes **self-supervised exploration** guided by the **disagreement among an ensemble of learned forward models**. Each model predicts the next state from the current state and action. Where the ensemble agrees, the environment’s dynamics are well understood; where it disagrees, the agent sees a high intrinsic reward. The authors show that this approach:

1. **Handles Stochastic Environments**: Because all models eventually converge to similar predictions (often the mean) for truly random transitions, the disagreement signal vanishes, preventing the agent from getting trapped in noise.  
2. **Enables Differentiable Policy Optimization**: The intrinsic reward is computed **without** needing to observe the actual next state \(\mathbf{x}_{t+1}\), letting the agent optimize its actions directly via supervised-like gradients (at least in short-horizon settings).  
3. **Scales to Real Robotics**: The authors demonstrate object interaction on a Sawyer arm from raw RGBD inputs, showing fewer samples needed for meaningful behavior compared to standard reinforcement-based curiosity.

The article aligns a classical “query-by-committee” style approach from active learning with modern RL exploration, motivating exploration by **model variance** rather than raw prediction error.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Avoiding Noise Traps**: By design, a disagreement-based approach decays to low rewards in truly random regions, avoiding “noisy TV” pitfalls—a central challenge in partially random RL.  
- **Adaptive Curiosity via Ensembles**: This method focuses curiosity on states where the **ensemble** remains uncertain, effectively capturing the gap between random and learnable transitions.  
- **Practical Implementation**: The authors’ real robotic manipulations underscore how ensembles plus differentiable exploration can be efficient in partially controlled, partially random settings.

Hence, the paper is **highly relevant** to adaptive curiosity frameworks that must handle partially random elements. Its demonstration that curiosity can self-correct in noise-laden or unlearnable subspaces is directly applicable.

---

### How It May Inform Future Research

1. **Long-Horizon Differentiable Exploration**  
   The authors limit direct policy optimization to short horizons. Extending differentiable ensemble-based methods to multi-step predictions (e.g., via recurrent world models) could enable deeper planning in partially random domains.

2. **Combining with Other Intrinsic Signals**  
   Merging ensemble disagreement with other curiosity signals (like count-based or Bayesian exploration) could further enhance robustness and coverage.  

3. **Adaptive Ensemble Size**  
   Dynamically adjusting the number of models in the ensemble based on the environment’s complexity or noise level might optimize computation while preserving exploration quality.

4. **Safe Exploration**  
   Disagreement-based approaches might be integrated with safety constraints (e.g., limiting actions in unknown subspaces to avoid catastrophic outcomes) in real-world robotics tasks.

---

### Open Questions or Possible Critiques

- **Computational Overhead**  
  Training and maintaining multiple models can be expensive for high-dimensional tasks. Strategies for **ensemble distillation** or partial model sharing might reduce overhead while retaining disagreement signals.

- **Long-Range Dependencies**  
  The short-horizon differentiable approach does not fully solve tasks requiring multi-step planning or partial observability. Future work must address how to maintain robust exploration signals over longer temporal spans.

- **Representation Learning**  
  In practice, the authors often embed states into a learned or random feature space. While effective, it is unclear how best to choose or adapt these features for broad generalization.

- **Policy Convergence**  
  The paper reports that in some tasks, policy gradient RL alone may be slow or prone to collapse. The interplay between direct gradient optimization and RL in more complex domains (e.g., hierarchical tasks) requires further exploration.
