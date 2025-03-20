# Algorithms of Reinforcement Learning

> **Link**: <https://doi.org/10.1007/978-3-031-01551-9>

> **Parenthetical**: (Szepesvári, 2010)
> **Narrative**: Szepesvári (2010)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **On Reinforcement Learning (RL) and MDPs**  
  > “Reinforcement learning is a learning paradigm concerned with learning to control a system so as to maximize a numerical performance measure that expresses a long-term objective. [...] We assume that the system we want to control is stochastic. Further, we assume that the measurements available on the system’s state are detailed enough so that the controller can avoid reasoning about how to collect information about the system.”  

- **Value Functions and Bellman Equations**  
  > “In MDPs with discount factor \(0 < \gamma < 1\), the optimal value function \(V^*\) is the unique fixed point of the Bellman optimality operator:  
  \[
     (T V)(x) \;=\; \max_{a \in A} \Bigl[r(x,a) \;+\; \gamma \sum_{y \in X} P(x,a,y)\,V(y)\Bigr].
  \]  
  \(T\) is a \(\gamma\)-contraction in the supremum norm, so by Banach’s fixed-point theorem \(V^*\) exists and is unique.”

- **Value Iteration and Policy Iteration**  
  The text details classical dynamic programming algorithms:
  1. **Value Iteration** iterates \(V_{k+1} = T(V_k)\), converging to \(V^*\).  
  2. **Policy Iteration** alternates exact policy evaluation with policy improvement until convergence.

- **TD(0) Algorithm (Tabular)**  
  For a Markov Reward Process (MRP) with observed transitions \((X_t, R_{t+1}, X_{t+1})\), the basic TD(0) update:
  \[
    V_{t+1}(X_t) \;\leftarrow\; V_t(X_t) \;+\; \alpha_t\,\Bigl(R_{t+1} + \gamma\,V_t(X_{t+1}) \;-\; V_t(X_t)\Bigr).
  \]

- **Monte Carlo vs. TD**  
  > “Monte-Carlo methods use multi-step returns, while TD(0) bootstraps from its own predictions. Each can be faster under different circumstances. TD(λ) unifies these approaches.”

- **Function Approximation**  
  > “In large or infinite state spaces, storing one value per state is infeasible. Instead, one uses a parametric representation \(V_{\theta}(x)\). This leads to new challenges, such as possible divergence unless special conditions are satisfied.”  

- **Gradient TD Methods (GTD2, TDC)**  
  For linear function approximation, the Gradient TD algorithms can converge even off-policy by minimizing a specific objective:
  \[
    J(\theta) \;=\; \|V_{\theta} - \Pi (T V_{\theta})\|^2_{\mu},
  \]
  where \(\Pi\) is a projection to the function class and \(T\) is the Bellman operator (or a variant).  
  > “They behave like stochastic gradient descent in a derived objective, but use an auxiliary weight vector to stabilize updates.”

- **Least-Squares TD (LSTD)**  
  > “By computing a solution to a linear system derived from the TD fixed-point condition, LSTD can converge faster than incremental TD in practice, at higher computational cost \(O(d^3)\) or \(O(d^2)\) per step when using recursive techniques.”

- **Control (Q-Learning, SARSA, Actor-Critic)**  
  - **Q-Learning**:  
    \[
      Q_{t+1}(X_t,A_t) \;\leftarrow\; Q_t(X_t,A_t) \;+\; \alpha_t\Bigl(R_{t+1} + \gamma \max_a Q_t(X_{t+1},a) \;-\; Q_t(X_t,A_t)\Bigr).
    \]  
    Convergent in tabular settings if every state-action is visited infinitely often.  
  - **SARSA**: On-policy version that uses the next action \(A_{t+1}\) from the same policy being improved.  
  - **Actor-Critic**:  
    - Critic learns a value function or action-value function using e.g. TD.  
    - Actor uses policy gradient or approximate policy iteration steps to improve the policy.

- **Exploration (UCB, E3, R-Max, UCRL2)**  
  The text reviews approaches to systematic exploration:  
  > “A good learner must take actions that look suboptimal, i.e., must explore. The question is how to balance the frequency of exploring and exploiting actions.”  
  **UCRL2** is an OFU (optimism in face of uncertainty) algorithm for finite MDPs, achieving regret bounds on the order of \(\tilde O(\sqrt{T})\) or \(\tilde O(T^{2/3})\) under certain assumptions.  
  **PAC-MDP** approaches (R-Max, MBIE, Delayed Q-Learning) guarantee polynomially many suboptimal steps with high probability.

- **Fitted Q-Iteration**  
  > “Creates a Monte-Carlo approximation to \(T Q^k\)(x,a) from a sample, then uses regression to fit \(Q^{k+1}\). Convergence can fail unless the approximator is a non-expansion (e.g., local averaging).”

- **Policy Gradient and Natural Gradient**  
  For parametric policies \(\pi_{\theta}\), the performance gradient is  
  \[
    \nabla_{\theta} J(\theta) \;=\; \mathbb{E}\bigl[\nabla_{\theta}\log \pi_{\theta}(A_t|X_t)\,Q^{\pi_{\theta}}(X_t,A_t)\bigr].
  \]
  A related update is the **natural gradient** (NAC) approach using a Fisher-information-matrix-based metric.  

---

### Concise Summary of the Article

**"Algorithms of Reinforcement Learning"** by Csaba Szepesvári provides a thorough introduction to fundamental RL concepts, emphasizing the interplay between **dynamic programming** and **function approximation**. Major topics include:

1. **Markov Decision Processes**  
   Formal definitions, Bellman equations, and the fundamental results (optimal value existence, policy iteration, contraction mappings, etc.).
2. **Value Prediction**  
   - TD(0), TD(\(\lambda\)), Monte-Carlo, and how they unify in TD(\(\lambda\)).  
   - Extensions to function approximation, including linear methods, potential divergence off-policy, and advanced incremental gradient TD algorithms (GTD2, TDC).
   - Least-squares TD (LSTD, LSTD(\(\lambda\))) and their complexities.
3. **Control**  
   - Q-learning, SARSA, and actor-critic frameworks, plus the importance of exploration.  
   - Systematic exploration algorithms (OFU, R-Max, E3, UCRL2) for small MDPs.  
   - Policy iteration variants, fitted Q-iteration, policy gradient, and natural actor-critic.
4. **Convergence Analyses and Error Bounds**  
   The text gives rigorous proofs using Banach fixed-point theorem, references to standard results in SA (stochastic approximation), performance bounds for approximate dynamic programming, and a summary of crucial open research questions.

Throughout, the manuscript balances theoretical clarity (covering proofs, asymptotic analyses, finite-sample bounds) with practical algorithmic sketches (pseudocode for TD(0), Q-learning, LSTD, etc.). The final sections discuss advanced or omitted topics (bandit-based sampling, partial observability, hierarchical RL, and numerous references to real-world RL applications).

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **State-of-the-Art RL Foundations**  
  The text thoroughly covers core RL algorithms (TD, Q-learning, policy gradient, approximate dynamic programming). Many *adaptive curiosity* methods expand upon these basics, e.g., layering on intrinsic rewards or specialized exploration heuristics.
- **Exploration in MDPs**  
  Although the text mostly addresses *optimal exploration* from a formal standpoint (regret, PAC-MDP), the same fundamental ideas (optimism in face of uncertainty, importance of visiting unknown transitions) apply in partially random domains.  
  This allows for controlled exploration even if some transitions are unlearnable noise.
- **Handling Large or Continuous Spaces**  
  The discussions on function approximation, LSTD, fitted methods, or policy gradient are directly relevant when investigating partially random or complex RL tasks, since scale and partial noise often require robust function approximators.

Hence, **citing Szepesvári’s monograph** is advisable for any research on *"Adaptive Curiosity for Exploration in Partially Random Environments"*, as it provides an authoritative introduction to both the theoretical underpinnings (dynamic programming, function approximation, convergence proofs) and various exploration strategies.

---

### Worth Citing?

**Yes.** This draft monograph is comprehensive, rigorous, and clearly written. It serves as:

- A reference for fundamental RL algorithms (tabular to approximate).  
- A consolidated presentation of major RL developments (value iteration, policy iteration, TD methods, function approximation, advanced exploration).  
- A stepping stone to specialized topics (hierarchical RL, partially observed MDPs, sophisticated exploration approaches).

Anyone delving into curiosity-driven or partially-random RL can benefit from the meticulous coverage of value-function approximation and exploration frameworks.

---

### How It May Inform Future Research

1. **Extending Function Approximation**  
   Researchers combining *adaptive curiosity* with partial randomness can use advanced linear or kernel-based methods from the text as a stable foundation for building intrinsic motivation signals.
2. **Exploration**  
   The coverage of UCRL2, R-Max, E3, and their regret/PAC-MDP analyses might inspire more refined curiosity-driven exploration that similarly leverages confidence bounds or model uncertainty.
3. **Policy Gradients and Natural Gradient**  
   In partially random continuous tasks, stable and data-efficient policy improvement is crucial. Natural policy gradients or NAC-based algorithms provide robust alternatives to naive gradient methods.
4. **TD Control with Large State Spaces**  
   The text’s emphasis on potential off-policy divergence highlights design constraints for curiosity-based RL, especially if partial environment randomness causes distribution shifts during learning.

---

### Open Questions or Possible Critiques

- **Off-Policy Stability**  
  While the text highlights off-policy divergence issues, a deeper analysis of *intrinsic rewards* driving distribution changes remains an open question, especially if partial randomness alters transition probabilities in ways not covered by standard off-policy convergence analyses.
- **Scalability of Exploration Algorithms**  
  The purely theoretical coverage of E3, R-max, or UCRL2 in small MDPs does not fully address how to adapt these strong guarantees to high-dimensional, partially random environments.
- **Approximation Trade-Offs**  
  The monograph underscores the approximation-estimation trade-off and the risk of divergence. Integrating curiosity-driven or partially random RL with large-scale function approximators might require more refined regularization and explicit safety nets (e.g., stable updates for both actor and critic).
