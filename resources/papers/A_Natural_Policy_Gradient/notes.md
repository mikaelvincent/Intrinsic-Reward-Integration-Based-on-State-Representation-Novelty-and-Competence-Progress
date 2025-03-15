# A Natural Policy Gradient

> **Authors**: Sham M. Kakade
> **Date**: 2001
> **Link**: <https://papers.nips.cc/paper/2073-a-natural-policy-gradient>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Motivation**  
  > “We provide a natural gradient method that represents the steepest descent direction based on the underlying structure of the parameter space. [...] We show that the natural gradient is moving toward choosing a greedy optimal action rather than just a better action.”

- **Core Definition of the Natural Gradient**  
  The paper proposes measuring the gradient direction using the Fisher information matrix:
  \[
    F(\theta) \;=\; \sum_{s} p_\pi(s)\,F_s(\theta), 
    \quad\text{where}\quad
    F_s(\theta) \;=\; \mathbb{E}_{a \sim \pi(\cdot \mid s)}\Bigl[\nabla_{\theta}\log\pi(a \mid s,\theta)\,\nabla_{\theta}\log\pi(a \mid s,\theta)^\top\Bigr].
  \]
  The **natural gradient** descent step is then
  \[
    \Delta \theta_{\text{natural}} \;=\; -\,F(\theta)^{-1}\,\nabla_\theta \eta(\theta),
  \]
  where \(\eta(\theta)\) is the average reward under policy \(\pi_\theta\).

- **Policy Gradient Formula**  
  In an undiscounted, ergodic Markov decision process (MDP), the standard policy gradient can be written as:
  \[
    \nabla_\theta \eta(\theta) 
    \;=\; \sum_{s,a} p_\pi(s)\,\pi(a\mid s,\theta)\,\nabla_\theta \log \pi(a\mid s,\theta)\,Q_\pi(s,a).
  \]
  The paper notes that typical gradient descent uses the identity matrix as the metric (i.e., \(\Delta \theta = -\nabla_\theta \eta(\theta)\)), which does not account for the geometry of the parameter space.

- **Compatible Function Approximation**  
  For actor-critic methods where \(Q_\pi(s,a)\) is approximated by a function \(f_\pi(s,a; w)\), they adopt *compatible* features:
  \[
    \psi_\pi(s,a) 
    \;=\; \nabla_{\theta} \log \pi(a \mid s, \theta),
    \quad
    f_\pi(s,a; w) 
    \;=\; w^\top \psi_\pi(s,a).
  \]
  A key result (Theorem 1) shows:
  \[
    w \;=\; F(\theta)^{-1}\,\nabla_\theta \eta(\theta),
  \]
  linking the natural gradient to the weights \(w\).

- **Moving Toward a Greedy Action**  
  The paper demonstrates that the natural gradient “pushes” the policy toward the best action (in a local, linear sense), in contrast to the standard gradient, which only ensures an action better than average is favored:
  > “It is in this sense that the natural gradient tends to move toward choosing the best action. [...] A sufficiently large step in the natural gradient direction will lead to a policy that is equivalent to a greedy policy improvement step.”

- **Hessian vs. Fisher Matrix**  
  The paper discusses the Hessian of \(\eta(\theta)\) and notes that it contains additional terms dependent on \(Q_\pi\). In general, the Hessian is not guaranteed to be positive definite and might not be reliable far from the optimum:
  \[
    \nabla^2_\theta \eta(\theta)
    \;=\; \underbrace{\sum_{s,a} p_\pi(s)\,\nabla^2_\theta \pi(a\!\mid\!s,\theta)\,Q_\pi(s,a)}_{\text{term 1}}
    \;+\; \dots
  \]
  The Fisher matrix \(\!F(\theta)\) focuses on the structure of the policy distribution itself (i.e., how \(\theta\) changes probability assignments), ignoring the explicit dependence on \(Q_\pi\).

- **Empirical Demonstrations**  
  1. **Linear Quadratic Regulator (LQG)**: A 1D LQR with state transition \(x_{t+1} = 0.7\,x_t + u_t + \epsilon_t\). The natural gradient converges faster and more robustly under scaling of the parameters.  
  2. **Two-State MDP**: A simple example shows how standard gradient descent can stall in “plateaus” because states with small stationary probabilities are updated slowly. The natural gradient, by contrast, balances parameter updates more effectively, reducing plateaus and improving exploration in that small MDP.  
  3. **Tetris**: The paper replicates known results where a greedy policy iteration approach with linear function approximation can suffer performance degradation. Standard gradient-based policy search fails to learn quickly. By using a natural gradient (with an exponential softmax policy parameterization), it avoids policy collapse and obtains strong performance—albeit not outpacing the best greedy iteration in raw speed.

- **Interpretations and Notes**  
  - The **natural gradient** does not converge to the full Hessian. Instead, it is an *invariant metric* for probability distributions.  
  - Closer to convergence, second-order methods (like a true Hessian-based approach or conjugate gradient) may be more efficient.  
  - Far from the optimum, however, the Fisher-based approach can be more robust, as it “pushes” the policy to choose near-greedy actions in a stable, gradient-based manner.

- **Importance**  
  > “With the overhead of a line search, the methods [natural gradient and approximate policy iteration] are even more similar. The benefit is that performance improvement is now guaranteed, unlike in a greedy policy iteration step.”

- **References**  
  The paper cites foundational work by Amari (1998) for natural gradients, policy gradient methods by Sutton et al. (2000), and analyses of performance in large MDPs such as Tetris.

---

### Concise Summary of the Article

Kakade’s paper **“A Natural Policy Gradient”** proposes leveraging the Fisher information matrix—an **invariant metric** on the space of probability distributions—to define a **natural gradient** for policy gradient reinforcement learning. This approach accounts for the geometry of the policy’s parameter space, yielding steps that remain consistent under reparameterization. The paper demonstrates:

1. **Connection to Greedy Improvement**: The natural gradient locally nudges the policy toward choosing the best action (for the approximate value function), making it conceptually closer to one-step policy iteration.  
2. **Implementation via Compatible Function Approximation**: If the critic or value estimator is chosen to be compatible with the actor, the weight vector of that critic is directly tied to the natural gradient steps.  
3. **Empirical Gains**: Simulations on a 1D LQG, a small two-state MDP, and the large-scale Tetris environment show that the natural gradient method can avoid plateauing and catastrophic policy collapses, often converging faster and more robustly than standard gradient descent.

Because the Hessian of the average reward function is not necessarily positive definite, the Fisher matrix provides a more stable, first-order method that can be less prone to local plateaus, especially when far from optimality. Results indicate that the natural gradient can yield smoother and more effective improvements compared to standard policy gradient in certain challenging RL tasks.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Primary Focus**: This paper concentrates on improving policy gradient efficiency by incorporating a geometry-aware metric. It does not directly address *intrinsic motivation*, *novelty detection*, or partial randomness.  
- **Indirect Relevance**: In partially random environments, stable and robust policy updates can prevent premature convergence or wasted exploration in unproductive directions. While Kakade’s approach does not supply intrinsic rewards or curiosity, it could serve as a **complementary optimization method** for any curiosity-driven RL algorithm needing more reliable gradient steps (e.g., to avoid numeric instabilities when environment randomness skews the state distribution).

Therefore, while not explicitly about curiosity or partial randomness, **citing this work can be valuable** if one’s adaptive curiosity framework requires a robust, geometry-aware approach to policy parameter updates. The natural gradient can help maintain stable learning even when random transitions might make the standard gradient ineffective or slow.

---

### Worth Citing?

**Yes.** Even though the article does not deal directly with intrinsic exploration or partial stochasticity, it is a seminal reference for using the Fisher information matrix in policy gradient RL. Any advanced reinforcement learning work—including those involving curiosity in noisy or partially random domains—may benefit from the stable training properties of the natural gradient approach.

---

### How It May Inform Future Research

1. **Stable Actor-Update Mechanisms**: Researchers developing curiosity-driven or exploration-heavy methods can use natural gradient updates to ensure stable optimization, particularly in high-dimensional or noisy tasks.  
2. **Combining Natural Gradient with Curiosity**: Future studies might integrate a natural gradient actor with an intrinsic reward or count-based explorer, verifying if the geometry-aware updates mitigate “stalling” or “plateau” behaviors in partially random environments.  
3. **Line Search in Intrinsic-Reward RL**: Kakade suggests that line searches can guarantee improvement with natural gradients. This might inspire line-search-based curiosity approaches, ensuring robust improvement even with dynamic intrinsic reward terms.

---

### Open Questions or Possible Critiques

- **Full vs. Partial Observability**: The paper assumes an ergodic MDP with well-defined stationary distributions. Realistic partially observable or random domains might challenge these assumptions.  
- **Near-Optimal vs. Far-From-Optimal**: Closer to local maxima, second-order (Hessian-based) or conjugate gradient methods can dominate. More investigation on switching from natural gradient to second-order near convergence might boost efficiency.  
- **Implementation Complexity**: Maintaining and inverting the Fisher matrix can be expensive for large parameter spaces. Approximations, block-diagonal forms, or Kronecker-factored approaches (K-FAC) may be necessary in practice.  
- **Policy Degradation**: The paper highlights how standard gradient descent can degrade a policy drastically, whereas the natural gradient does not. However, large-scale tasks still might require careful tuning of regularization or learning rates to prevent numerical issues.
