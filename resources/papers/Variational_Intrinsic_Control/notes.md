# Variational Intrinsic Control

> **Authors**: Karol Gregor, Danilo Jimenez Rezende, Daan Wierstra
> **Date**: 22 Nov 2016
> **Link**: <https://doi.org/10.48550/arXiv.1611.07507>

---

## Selected Direct Quotes, Data, and Formulas

1. **Intrinsic Options / Goals**  
   > “We define options as policies with a termination condition, and we are primarily concerned with their consequences—what states in the environment they reach upon termination. [...] The purpose of this work is to provide an algorithm that aims to discover as many intrinsic options as it can, using an information theoretic learning criterion and training procedure.”

2. **Mutual Information as the Objective**  
   The key principle is to maximize the mutual information between the *option* and the *final state*. Let \(\zeta\) be an “option” variable, and let \(s_f\) be the termination state. Then:
   \[
   I(\zeta; s_f \mid s_0) \;=\; H(s_f \mid s_0) \;-\; \mathbb{E}_{\zeta\sim p_C,\,s_f\sim p_J}[H(s_f \mid s_0,\zeta)].
   \]
   Equivalently:
   \[
   I(\zeta; s_f \mid s_0) 
   \;=\; \mathbb{E}_{p(\zeta, s_f)}\bigl[\log p(\zeta\mid s_f) - \log p_C(\zeta\mid s_0)\bigr].
   \]
   The authors use a **variational lower bound** with a function \(q(\zeta \mid s_f)\) approximating \(p(\zeta \mid s_f)\).

3. **Two Algorithms**  

   - **Algorithm 1**: *Intrinsic Control with Explicit Options*  
     - Maintains a discrete or continuous set of options \(\zeta\), each with its own policy \(\pi^\zeta\).  
     - Trains an inverse model \(q(\zeta \mid s_f)\) so that final states can predict which option was used.  
     - Intrinsic reward:  
       \[
         r_I \;=\; \log q(\zeta \mid s_f) \;-\; \log p_C(\zeta \mid s_0),
       \]
       used to update the policy for each option and also the prior over options \(p_C\).

     > “If a particular option is inferred correctly and with confidence, then \(\log q\) is close to 0 (less negative), and the reward is large. If it is wrong, the reward is small.”

     The authors note **training instability** with function approximation and exploration difficulties, especially for large or continuous option spaces.

   - **Algorithm 2**: *Intrinsic Control with Implicit Options*  
     - Collapses the “option space” to **action sequences** in a policy \(p\). Then the inverse function \(q\) attempts to reconstruct the agent’s action choices from the final state.  
     - This simplifies training because the agent’s actions themselves become the “latent variable.”  
     - They define a policy \(p(a_t \mid s_t^p)\) and an inverse policy \(q(a_t \mid s_t^q)\). The intrinsic reward each time step is:
       \[
         r_I^t \;=\; \log q(a_t \mid s_t^q) \;-\; \log p(a_t \mid s_t^p).
       \]
       Summed over the trajectory, it measures the “number of distinct action sequences” the final state can identify.

     > “We show that using closed-loop policies (actions conditioned on states) significantly improves the empowerment estimate compared to open-loop sequences. [...] In practice, the agent can handle partial observability with a recurrent network, extracting final representation for the termination state.”

4. **Closed-Loop vs. Open-Loop**  
   > “Using open loop options (sequence of actions fixed in advance) leads to a severe underestimation of empowerment in stochastic domains. [...] We demonstrate this in a ‘dangerous grid world’ environment, where open-loop agents prefer a safe but low-empowerment region.”

5. **Empowerment**  
   The authors connect their objective to the notion of **empowerment**—the agent’s ability to reach many different final states reliably.  
   > “The average of the intrinsic reward is on par with the agent’s estimate of how many states it can reliably reach from a given state. Taking \(\exp\) of the average reward is akin to the agent’s count of effectively distinct states it can control.”

6. **Experiments**  

   - **Grid Worlds**:  
     - The agent learns to navigate different rooms and produce extended, purposeful trajectories that pass through narrow doors.  
     - Achieves near-uniform coverage of final states across reachable areas, verifying high empowerment.  

   - **“Dangerous” Grid World**:  
     - Some sub-lattice actions cause the agent to get “stuck.”  
     - **Open-loop** approaches overvalue the “safe corner.”  
     - **Closed-loop** policy can adapt to partial noise, achieving higher empowerment in the large open region.

   - **3D Simulated Maze**:  
     > “From purely visual 40×40 color images, the agent learns wide sweeping trajectories. We measure ~54 nats of empowerment—\(\exp(54) \approx 2.51\times10^{23}\) states, ignoring unreachable parts and noise.”

   - **Blocks Pushing**:  
     - The agent can move around a grid and push blocks that cannot pass each other.  
     - The agent learns complicated multi-push sequences, controlling block arrangements. Achieved ~71 nats (\(\approx\exp(71)\) states).

   - **MNIST Pairs**:  
     - Each environment state is a 2×28 vertical stacking of MNIST digits. Five actions shift the digit classes up/down for each digit. The final digit shape is random within the chosen class.  
     - The agent learns to ignore the uncontrollable variations and obtains nearly the maximum possible empowerment for controlling the digit classes (\(\approx 100\) states effectively reached).

7. **Unsupervised -> Reward**  
   > “An agent can spend time discovering how to control the environment (intrinsic control). Then, upon receiving an external reward, it can quickly incorporate that reward and find a solution using the already learned skills.”

8. **Conclusions**  
   > “We present a formalism of intrinsic control, with two new algorithms that maximize mutual information between options and final states. We show closed-loop policies are essential for realistic tasks and highlight how learned empowerment can aid extrinsic reward tasks.”

---

## Concise Summary of the Article

Gregor, Rezende, and Wierstra propose a **mutual-information-based approach** to learn “intrinsic options” or **goals** in a fully *unsupervised* manner. The central idea: an agent should discover a set of policies (options) that produce **maximally distinct final states**—i.e., states from which one can infer which option was executed.

They derive two algorithms:

- **Explicit Options (Algorithm 1):** Maintain a prior distribution over options and a parametric inverse model \(q(\zeta \mid s_f)\). Each option \(\zeta\) has its own policy. The agent gets an **intrinsic reward** if the final state can accurately identify which option was used. This approach, while conceptually straightforward, proved difficult to scale with large function approximators and continuous option spaces.

- **Implicit Options (Algorithm 2):** Collapses the idea of an “option” into the agent’s *action history*. The agent’s final state must be able to predict which sequence of actions it took. This method is simpler to implement, requiring a single universal policy \(p\) plus an inverse model \(q\). Empirically, it scales better, encouraging wide coverage across the environment and achieving higher “empowerment.”

They show that **closed-loop** options (where each action depends on the current state) yield drastically higher empowerment in stochastic domains than **open-loop** sequences. Through examples (grid worlds, 3D maze, pushing blocks, MNIST digit classes), the agent learns sophisticated, extended behaviors *without any extrinsic reward*. Additionally, the authors demonstrate that these unsupervised skills can accelerate subsequent *extrinsic-reward tasks* since the agent already “knows” how to navigate or manipulate states in many ways.

---

## Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Mutual-Information-Based Intrinsic Motivation**: The paper introduces a robust method for discovering controllable subspaces in an environment—aligning with *adaptive curiosity* to seek states the agent can influence.
- **Handling Partial Randomness**: The approach explicitly discounts environment noise or uncontrollable aspects, focusing only on final states that the policy can reliably differentiate. They highlight how closed-loop policies mitigate random transitions. 
- **Empowerment**: The concept of measuring an agent’s capacity to produce distinct outcomes resonates with partially-random tasks, where identifying truly controllable aspects is crucial.

**Worth citing?** Definitely. The paper provides a novel unsupervised skill-discovery scheme that aligns with advanced curiosity-driven exploration. It clarifies the necessity of closed-loop policies for empowerment in stochastic domains and yields practical algorithms for skill representation.

---

## How It May Inform Future Research

1. **Merging with Existing Curiosity Signals**: Their mutual-information objective can integrate with other curiosity or uncertainty signals, potentially improving exploration in partially random domains.

2. **Hierarchical RL**: Future work might incorporate the learned “intrinsic control” options as building blocks for hierarchical planners, bridging large timescales or complex tasks.

3. **Continuous Control and Real Robotics**: The implicit options algorithm suggests a path to robust skill discovery in real-world tasks, especially if combined with safe exploration or domain-randomization.

4. **Multi-Step or Multi-Goal Transfers**: Demonstrations that “pretrained” empowerment speeds up extrinsic tasks. Extending that to multi-task or meta-learning scenarios could produce even broader capabilities.

---

## Open Questions or Possible Critiques

1. **Training Stability**: Algorithm 1 with explicit options can be unstable under deep neural approximations. The paper partially addresses this with Algorithm 2, but additional experiments on large-scale continuous tasks remain needed.

2. **Exploration**: Even with an information-theoretic objective, if certain states remain unvisited, the agent might never discover potential new “options.” More advanced exploration heuristics or auxiliary signals could be crucial in high-dimensional or extremely stochastic worlds.

3. **State vs. Observation**: The approach frequently uses final **observations** rather than environment states. If partial observability is severe, the approach might over- or under-estimate controllability. Additional recurrent or memory-based architectures might be essential.

4. **Purely Intrinsic vs. Mixed Reward**: The authors show a demonstration of adding extrinsic rewards post-hoc. More systematic tests on large tasks or complex 3D physics might reveal further synergy or new obstacles (e.g., catastrophic forgetting of discovered skills).

5. **Granularity of Termination**: The approach picks final states after a fixed time horizon or a termination condition. Additional research might investigate variable-horizon options or multiple termination triggers.
