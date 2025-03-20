# An analysis of temporal-difference learning with function approximation

> **Link**: <https://doi.org/10.1109/9.580874>

> **Parenthetical**: (Tsitsiklis & Van Roy, 1997)
> **Narrative**: Tsitsiklis and Van Roy (1997)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Core Objective**  
  > “We discuss the temporal-difference learning algorithm, as applied to approximating the cost-to-go function of an infinite-horizon discounted Markov chain.”  

- **TD(λ) Framework**  
  For an irreducible, aperiodic Markov chain with discount factor \(\gamma\in(0,1)\), the cost-to-go function \(J^*\) satisfies  
  \[
    J^*(i) \;=\; \mathbb{E}\Bigl[\sum_{t=0}^\infty \gamma^t\,c(x_t,x_{t+1}) \,\Big|\; x_0 = i\Bigr],
  \]
  where \(x_t\) are states and \(c(\cdot,\cdot)\) are transition costs.

- **Function Approximation**  
  TD methods iteratively approximate \(J^*\) using a parameter vector \(\theta\) for either:
  1. **Linear** approximators:  
     \[
       \hat{J}_\theta(x) \;=\; \sum_{k=1}^d \theta_k\,\phi_k(x),  
     \]
     or vector form \(\hat{J}_\theta(x) = \phi(x)^\top \theta\).  
  2. **Nonlinear** approximators (e.g., neural networks), though the paper later shows potential divergence in certain nonlinear cases.

- **TD(λ) Update Rule**  
  In the linear case, define an eligibility vector \(z_t\in\mathbb{R}^d\). Then for each observed transition \((x_t,x_{t+1},c_t)\), the parameters \(\theta\) evolve via:
  \[
    z_{t+1} \;=\; \lambda\gamma\,z_t + \phi(x_t),
    \quad
    \theta_{t+1} \;=\; \theta_t + \alpha_t\,\delta_t\,z_{t+1},
  \]
  with  
  \[
    \delta_t \;=\; c_t + \gamma\,\hat{J}_{\theta_t}(x_{t+1}) \;-\; \hat{J}_{\theta_t}(x_t).
  \]
  This is referred to as TD(\(\lambda\)).

- **Convergence Theorem**  
  > “We present a proof of convergence (with probability one), a characterization of the limit of convergence, and a bound on the resulting approximation error.”  

- **Core Assumptions**  
  1. The Markov chain is irreducible and aperiodic with a unique stationary distribution \(\mu\). Transition costs \(c(\cdot,\cdot)\) have finite variance under this chain.  
  2. Basis functions \(\{\phi_k\}\) are linearly independent, and each \(\phi_k\) is in \(L^2(\mu)\) (roughly speaking, it is square-integrable w.r.t. the stationary distribution).  
  3. A “stability” assumption: roughly, certain weighted norms of the Markov chain and updates remain finite over time.  
  4. Step sizes \(\{\alpha_t\}\) are positive, nonincreasing, satisfy \(\sum \alpha_t = \infty\) and \(\sum \alpha_t^2 < \infty\).

- **Main Convergence Result**  
  **(Theorem 1)**: For linear function approximators and on-policy sampling of states from the chain’s stationary distribution:
  1. The algorithm converges almost surely to a unique limit point \(\theta^*\).  
  2. The limit \(\hat{J}_{\theta^*}\) solves a certain fixed-point equation \(\Phi \theta^* = P_\Phi (T_{\lambda}(\Phi\theta^*))\), where \(T_{\lambda}\) is the so-called “TD(\(\lambda\)) operator” plus projection.  
  3. A bounded error result:  
     \[
       \|\,J^* - \hat{J}_{\theta^*}\,\|_D 
       \;\le\; \frac{1}{1-\gamma}\,\|\,J^* - P_\Phi(J^*)\,\|_D,
     \]
     implying that \(\hat{J}_{\theta^*}\) is at most a factor \(\frac{1}{1-\gamma}\) worse than the best possible projection in that weighted norm.

- **Importance of On-Policy (i.e., On-Line) Sampling**  
  The paper shows that if states are **not** sampled from the Markov chain’s own dynamics (i.e., if the sampling distribution mismatches the chain’s stationary distribution), TD(\(\lambda\)) can diverge. This reconciles known negative results about “off-line” or arbitrary sampling distributions versus positive results about on-policy methods.

- **Nonlinear Approximation Issue**  
  > “We present an example illustrating the possibility of divergence when temporal-difference learning is used in the presence of a nonlinear function approximator.”  
  In Section X, the authors construct a simple Markov chain with three states and a discount factor, plus a contrived nonlinear approximator that leads to spiraling, unbounded parameter updates.

- **Key Intuitive Points**  
  1. **Weighted Norm**: The “\(\|\cdot\|_D\)” norm is crucial in the analysis, weighting state differences by their stationary distribution.  
  2. **Projection and Contraction**: The operator \(\Pi_\Phi \circ T_\lambda\) is shown to be a **contraction** in that norm, guaranteeing a unique fixed point that the algorithm converges to.  
  3. **Relevance of \(\lambda\)**: Smaller \(\lambda\) can accelerate early learning but can potentially yield a larger final approximation error. \(\lambda=1\) reduces to a kind of steepest-descent method that is guaranteed to converge to the best approximation in the chosen subspace but can be slower initially.

- **Technical Highlights**  
  - **Steady-State Argument**: By recasting TD(\(\lambda\)) in an “average update” sense, the authors analyze a deterministic counterpart to the stochastic algorithm, then invoke stochastic-approximation theorems (Benveniste–Météivier–Priouret theory).  
  - **Extensive Markov Chain Properties**: The irreducible, aperiodic conditions plus the unique stationary distribution ensure consistent sampling frequencies.  
  - **Functional Space**: For infinite state spaces, they consider the chain as lying in \(L^2(\mu)\) with basis functions, requiring certain stability conditions for the analysis.

---

### Concise Summary of the Article

Tsitsiklis and Van Roy analyze **temporal-difference (TD) learning** with **function approximation**—focusing on **linear** approximators—applied to **infinite-horizon discounted Markov chains**. Their principal results include:

1. **Convergence in Probability One**:  
   On-policy TD(\(\lambda\)) converges almost surely to a unique solution if (a) the Markov chain is irreducible and aperiodic, (b) basis functions are linearly independent and in \(L^2\), and (c) step sizes meet standard diminishing criteria.  
2. **Fixed-Point Equation and Error Bounds**:  
   The limit of convergence satisfies a linear fixed-point equation \(\Phi^\top D (\hat{J}_{\theta^*} - \gamma P \hat{J}_{\theta^*}) = \dots\), and the approximation error is bounded by \(\frac{1}{1 - \gamma}\) times the best projection error in the chosen subspace.  
3. **Necessity of On-Line Sampling**:  
   If states are sampled in a manner inconsistent with the chain’s stationary distribution—e.g., i.i.d. from a fixed distribution—TD methods can diverge for linear approximators.  
4. **Potential Divergence for Nonlinear Approximators**:  
   They provide an explicit three-state chain and a contrived nonlinear function class for which the TD(0) parameters spiral out to infinity. This warns that beyond linear architectures, convergence is not guaranteed without further restrictions.

Overall, the article **reconciles** prior negative counterexamples of TD learning by clarifying that **on-policy sampling** is crucial to ensure convergence. The resulting limit function is the unique fixed point of a contraction mapping in a weighted norm space, thus ensuring stable approximation to \(J^*\).

---

### Significance and Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Exploration-Driven Methods**  
  Many “adaptive curiosity” or “intrinsic motivation” algorithms build on top of TD learning to evaluate environment states or produce novelty signals. The paper’s main theorems highlight conditions under which TD-based updates remain stable.  
- **Partially Random Environments**  
  Ensuring that the agent’s sampling distribution matches the chain’s inherent transitions is crucial. If the environment is partially random, one must confirm that the exploration strategy still respects or tracks the actual steady-state dynamics. Otherwise, function approximation might diverge.  
- **Linear vs. Nonlinear**  
  The authors show a negative example of divergence with a nonlinear function class, suggesting that curiosity-driven approaches using complex networks must be carefully scrutinized to avoid unbounded updates—especially if partial randomness skews the input distribution and the learned model.  

Thus, this article is **highly relevant** for anyone designing curiosity-based or exploration-based RL systems in large or partially random domains. It underscores why on-policy data collection is vital in stable function approximation with TD methods, a principle that also extends to advanced exploration scenarios.

---

### Worth Citing?

**Yes.** This is a fundamental work in reinforcement learning theory regarding convergence of TD methods:

- It **provides** rigorous guarantees for **linear** function approximators.  
- It **explains** how certain negative examples arise from off-policy or artificially sampled states.  
- It **connects** contraction mappings, projection operators, and Markov chain theory in a unified analysis.  
- It **warns** about potential instability with nonlinear approximation—still a major open topic.

---

### How It May Inform Future Research

1. **On-Policy Exploration**: Highlights that off-policy or artificially forced sampling can break convergence. Future “adaptive curiosity” research must ensure that exploration policies remain sufficiently close to on-policy distributions or incorporate correction mechanisms.  
2. **Nonlinear Classes**: Stimulates deeper investigations into safe function approximation beyond linear basis expansions—particularly for partially random environments where stability can be fragile.  
3. **Variable \(\lambda\) Strategies**: Encourages exploration of how to schedule or adapt \(\lambda\) over time to balance faster convergence with final approximation quality.  
4. **Extension to Control**: The paper deals with policy evaluation. When the policy itself is being improved concurrently (as in full control tasks), can similar contraction arguments be established or do partial-randomness or nonstationary policies break the analysis?

---

### Open Questions or Possible Critiques

- **Rate of Convergence**: While the authors provide a bound on the *final* approximation error, deeper insight into convergence *speed* for large-scale or partially random tasks remains to be fully developed.  
- **Nonlinear Approximation**: The divergence example is somewhat contrived; it remains unclear how large neural networks or other function classes might systematically avoid or risk divergence in practice.  
- **Changing Policies**: The result is strictly for policy evaluation under a fixed Markov chain. Many RL tasks use approximate TD methods in tandem with ongoing policy updates, raising questions about theoretical convergence in those more general settings.  
- **Finite vs. Infinite Spaces**: The authors do handle infinite state spaces under certain integrability and bounding conditions. However, further exploration is warranted for real-world, partially observable, or continuous domains with partial randomness.
