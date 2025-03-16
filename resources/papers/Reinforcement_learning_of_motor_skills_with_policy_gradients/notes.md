# Reinforcement learning of motor skills with policy gradients

> **Authors**: Jan Peters, Stefan Schaal
> **Date**: 13 August 2018
> **Link**: <https://doi.org/10.1016/j.neunet.2008.02.003>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Policy Gradient Framework**  
  > “Reinforcement learning is probably the most general framework in which such learning problems of computational motor control can be phrased.”

- **Learning Setup**  
  The paper is set in a continuous, high-dimensional reinforcement learning (RL) context. The authors define:
  \[
    x_{k+1} \sim p(x_{k+1} \mid x_k, u_k), \quad u_k \sim \pi_\theta(u_k \mid x_k),
  \]  
  where \(x_k \in \mathbb{R}^N\) is the state and \(u_k \in \mathbb{R}^M\) is the action at discrete time step \(k\). The policy \(\pi_\theta\) is parameterized by \(\theta \in \mathbb{R}^K\).

- **Episodic Return**  
  \[
    J(\theta) \;=\; \frac{1}{a_\Sigma} \, \mathbb{E}\!\biggl[\sum_{k=0}^H a_k\,r_k \biggr],
  \]  
  with weight factors \(a_k\) (e.g., discounting \( \gamma^k \)) or simply \(a_k = 1\). The distribution \(d_\pi(x)\) and definitions for \(V^\pi(x)\), \(Q^\pi(x,u)\) appear. The goal is maximizing \(J(\theta)\).

- **Motor Primitives**  
  1. **Spline-Based**:  
     \[
       q_{d,n}(t) \;=\; \theta_{0n} + \theta_{1n}\,t \;+\; \theta_{2n}\,t^2 \;+\; \theta_{3n}\,t^3,
     \]  
     with boundary conditions at each spline node to ensure continuity.

  2. **Dynamical Systems (Ijspeert et al.)**:  
     \[
       \ddot{q}_d \;=\; f\bigl(q_d,\,z,\,g,\,\tau,\,\theta\bigr),
     \]  
     plus canonical system \(\dot{z} = f_c(z,\tau)\). The open parameters \(\theta\) are typically the linear weights of a function approximator. This approach yields robust “attractor” behaviors and allows online adjustments.

- **Policy Gradient Approaches**  
  - **Finite-Difference (FD)**:  
    \[
      \nabla_\theta J \;\approx\; \frac{1}{2\Delta \theta} \bigl(J(\theta + \Delta \theta) - J(\theta - \Delta \theta)\bigr),
    \]  
    or more general simultaneous perturbation forms (SPSA). Straightforward but can be high variance and prone to local minima in high-dimensional, noisy tasks.

  - **Likelihood Ratio / REINFORCE** (Williams, 1992):  
    \[
      \nabla_\theta J(\theta) \;=\; \mathbb{E}\bigl[\nabla_\theta \log \pi_\theta(u_k \mid x_k)\,r(\tau)\bigr].
    \]  
    Introduces baselines to reduce variance:
    \[
      \nabla_\theta J(\theta) \;=\; \mathbb{E}\Bigl[\nabla_\theta \log \pi_\theta(\tau)\,\bigl(r(\tau) - b\bigr)\Bigr].
    \]

  - **Policy Gradient Theorem (Sutton et al., 2000) / G(PO)MDP**:  
    Removes some terms that vanish in expectation, e.g.,  
    \[
      \nabla_\theta J \;=\; \mathbb{E}\Bigl[\nabla_\theta \log\pi_\theta(u_k \mid x_k)\,\sum_{l \ge k} a_l\,r_l \Bigr].
    \]  
    Potentially lower variance than raw REINFORCE.

  - **Compatible Function Approximation**:  
    One can replace \(\hat{Q}^\pi(x,u)\) with a linear function \(\bigl(\nabla_\theta \log \pi_\theta(u \mid x)\bigr)^T w\). This preserves unbiasedness under certain conditions.

- **Natural Policy Gradient**  
  > “... the steepest ascent with respect to the Fisher information metric (Amari 1998) ... is called the natural policy gradient.”  
  The Kullback–Leibler divergence between old and new policy is approximated by \(\frac12 \Delta \theta^T F_\theta \Delta \theta\), leading to the update
  \[
    \Delta \theta \;=\; \alpha \, F_\theta^{-1} \,\nabla_\theta J,
  \]
  with \(F_\theta\) the Fisher information matrix. This form re-scales gradient directions so that policy changes are performed more “naturally” in parameter space.

- **Natural Actor-Critic**  
  Derives a critic that estimates an advantage function in “compatible” form \(A^\pi(x,u) = (\nabla_\theta \log \pi_\theta(u \mid x))^T\,w\). Solves a linear system to get the parameters \(w\), then updates \(\theta\) with the natural gradient \(\Delta \theta = \alpha w\). This approach can be further specialized:
  - **Episodic NAC**: Summation over entire trajectories.
  - **Time-Variant Baseline** NAC: Further reduces variance by using partial returns at each time step.

### Concise Summary of the Article

In this paper, Peters and Schaal address how to learn complex motor skills—like hitting a baseball with a multi-joint robotic arm—under a reinforcement learning framework where states and actions are high-dimensional and continuous. They:

1. **Motivate Motor Primitives**:  
   - **Spline-based** and **dynamical system-based** primitives represent continuous movements.  
   - These provide parameterized control policies, ready for RL.

2. **Survey and Compare Policy Gradient Methods**:  
   - **Finite-Difference** (SPSA-type) can handle non-differentiable policies but is often slow and susceptible to local minima in large problems.  
   - **Vanilla Likelihood Ratio (REINFORCE / G(PO)MDP)** reduces variance with a baseline, but still can converge slowly.  
   - **Natural Policy Gradients** re-scale the gradient by the Fisher information of trajectories to accelerate convergence.  
   - **Actor-Critic** merges a learned value function (critic) with gradient-based policy updates (actor). The authors present the **Episodic Natural Actor-Critic** as a best-of-breed method that significantly outperforms simpler methods.

3. **Empirical Results**:  
   - **Synthetic 1-DoF tasks**: NAC achieves an order of magnitude faster convergence than simpler policy gradients or finite differences.  
   - **Real Robot T-ball**: A 7-DoF Sarcos arm learns to swing a bat and hit a ball off a tee. Imitation from demonstration initializes the motor primitives; NAC then significantly refines the policy, achieving strong performance in ~200–300 trials.

Overall, the article strongly supports **natural policy gradient** and **actor-critic** approaches as the most effective policy gradient methods for high-dimensional motor skill learning.

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: While the paper does not directly address “noisy TV” or fully random transitions, it provides thorough methods for stable, efficient policy optimization in high-dimensional, continuous spaces.  
- **Adaptive Curiosity**: NAC can handle exploration by incorporating stochastic policies. The re-scaling of gradient steps is helpful for balancing exploration vs. exploitation when the environment is partially random.  
- **Takeaway**: The methods here (especially NAC) can give insight into stable gradient updates in the presence of exploration noise, potentially combining well with curiosity-driven or intrinsic motivation signals.

**Worth Citing?**  
Yes. This paper is a foundational reference for **policy gradient** and **natural actor-critic** methods in robotics and motor skill learning. It systematically compares classic policy gradient techniques, introduces new variants, and demonstrates real-robot success. Researchers dealing with RL-based skill acquisition or extended to partially random domains will find the NAC approach relevant as a robust, theoretically well-founded method for updating policies in continuous spaces.

### How It May Inform Future Research

1. **Combining NAC with Intrinsic Rewards**  
   The stable natural gradient framework could incorporate curiosity signals (exploration bonuses) in partial-stochastic tasks, limiting the detrimental “plateau” or “random trap” phenomena.
2. **Hierarchical Skills**  
   The “motor primitive” concept might be expanded or stacked hierarchically, learning entire skill repertoires with an NAC-based approach.
3. **Extensions to Noisy, Partially Observed Systems**  
   Future studies might combine NAC with state estimators or robust dynamic models to handle the uncertain transitions typical of real-world tasks.

### Open Questions or Possible Critiques

- **High-Dimensional Fisher Inversion**: NAC requires the Fisher matrix \(\sim \mathcal{O}(K^2)\) operations for \(K\) parameters. Approximations or low-rank factorization might be required for even larger-scale systems.
- **Exploration**: The paper uses Gaussian noise in action space. More adaptive exploration strategies might be needed for tasks with partial randomness or complex reward landscapes.
- **Model-Based NAC**: The authors focus on model-free updates. In principle, one might exploit approximate models or prior knowledge to accelerate learning, but that remains an open topic in NAC frameworks.
- **Locomotion & Full Humanoids**: The T-ball experiment is promising, but real-time NAC in full humanoid walking or running would test the algorithm’s scalability and require carefully managed exploration to avoid physical damage.
