# Diversity is All You Need: Learning Skills without a Reward Function

> **Link**: <https://doi.org/10.48550/arXiv.1802.06070>

> **Parenthetical**: (Eysenbach et al., 2018)
> **Narrative**: Eysenbach et al. (2018)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Motivation**  
  > “Intelligent creatures can explore their environments and learn useful skills even without supervision, so that when they are later faced with specific goals, they can use those skills to satisfy the new goals quickly and efficiently.”

- **Key Objective**  
  The paper focuses on learning diverse, useful skills **without a reward function**. The authors propose a method called **DIAYN** (“Diversity is All You Need”), which frames skill discovery as maximizing an information-theoretic objective under a maximum-entropy policy. They aim to learn skills that:
  1. Are **distinguishable** from one another based on the states visited.
  2. Encourage **coverage** of large parts of the state space.
  3. Maximize **randomness** or entropy in their actions, so that each skill robustly explores “its own region” of the environment.

- **Information-Theoretic Formulation**  
  The method treats each skill as a latent variable \( z \). Let \( S \) be states, \( A \) be actions. The objective is to maximize (Equation 1 in the paper):
  \[
    F(\theta) \;=\; I(S; Z) \;+\; H[A \mid S] \;-\; I(A; Z \mid S),
  \]
  which can be rearranged in a simpler form:
  \[
    F(\theta) \;=\; H[Z] \;-\; H[Z \mid S] \;+\; H[A \mid S, Z].
  \]
  - \(\;H[Z] \;\): The fixed or uniform prior over skills (kept maximal).  
  - \(\;H[Z \mid S]\): Encourages each skill to produce state distributions from which \( z \) can be inferred.  
  - \(\;H[A \mid S, Z]\): Encourages maximum action entropy within each skill.

- **Variational Approximation**  
  To handle unknown \(\;p(z \mid s)\), DIAYN uses a learned **discriminator** \(\;q_\phi(z \mid s)\). Replacing the true posterior with \(q_\phi\) in a lower-bound expression gives the final training objective:
  \[
    \max_{\theta, \phi} \;\;\; \mathbb{E}_{z, s} \bigl[\log q_\phi(z \mid s)\bigr] + \alpha \, H[\pi_{\theta}(\cdot \mid s,z)],
  \]
  plus a baseline term \(\,-\log p(z)\). Here, \(\alpha\) scales the entropy regularization.

- **Practical Realization**  
  1. **Policy** \(\pi_\theta(a \mid s,z)\) is trained via an off-policy RL algorithm (Soft Actor-Critic).  
  2. **Discriminator** \(\;q_\phi(z \mid s)\) is updated to classify which skill \( z \) produced state \( s \).  
  3. **Skill Sampling**: The environment is reset each episode, sampling a skill \( z \sim p(z) \). The agent then acts under that skill’s policy for the entire episode.  
  4. **Pseudo-Reward**: At each timestep, the agent is rewarded with:
     \[
       r^i_t \;=\; \log q_\phi(z \mid s_{t}) \;-\; \log p(z),
     \]
     which fosters state distributions that are easy to discriminate. A term for action-entropy is also added.

- **Why Keep \( p(z) \) Fixed**  
  The authors emphasize that learning the skill prior \(p(z)\) can cause “collapse”: easily discovered or more diverse skills are sampled more often, further improving them at the expense of other skills. Fixing \(p(z)\) uniformly ensures exploration across all skill indices.

- **Empirical Findings**  
  - **Classic Control**: DIAYN learns skills that solve tasks (e.g., Mountain Car, Inverted Pendulum) without seeing the environment reward. Each skill implements a distinct solution strategy.  
  - **Locomotion**: On HalfCheetah, Hopper, and Ant, DIAYN discovers behaviors such as flipping, running forward or backward, hopping, etc. Interestingly, some behaviors match or exceed the standard RL baseline’s performance, *even though no external reward was used.*  
  - **Policy Initialization**: Taking a skill that already achieves high reward (on a known task) can be fine-tuned quickly to boost final performance.  
  - **Hierarchical RL**: A “meta-controller” can select among learned skills to address more challenging tasks (like navigation with obstacles), surpassing strong baselines in sparse-reward or exploration-heavy problems.  
  - **Imitation Learning**: They also show how to pick a skill that best matches an expert’s demonstrated states (no actions needed), effectively forming a feedback controller that reproduces the demonstration.

- **Interpretations**  
  1. **Diverse Coverage**: By forcing each skill to be state-distinguishable, the ensemble effectively covers many sub-regions.  
  2. **Entropy Encouragement**: Requiring each skill to maintain high action-entropy prevents trivial, deterministic solutions and encourages robust coverage.  
  3. **Bottleneck States**: In gridworld analysis, the paper shows skills often separate states by narrow transitions, partitioning the environment so each skill can remain distinguishable.

- **Open Questions**  
  - **Limiting the Number of Skills**: If the environment is very large, how many skill indices are needed to cover it effectively? The authors note a simple extension to incorporate prior knowledge (e.g., restricting the discriminator to part of the state).  
  - **Long-Horizon Sequencing**: Single-step or single-skill episodes can limit the behaviors learned. Hierarchical composition is proposed, but more complex tasks may require deeper skill nesting or multi-step skill scheduling.  
  - **Truly Random or Unlearnable Subsets**: The approach can still produce skill overlap or fail to exploit small but essential sub-regions. Additional refinements or focus might be needed for partially random or extremely large spaces.

---

### Concise Summary of the Article

**“Diversity is All You Need” (DIAYN)** is an unsupervised RL framework for **skill discovery**:
1. **Core Idea**: Maximize mutual information between states and a latent skill variable \( z \). Each skill is a maximum-entropy policy that visits a unique subset of states, enabling the discriminator to identify which skill is active from any visited state.
2. **Implementation**: 
   - Use an off-policy RL method (Soft Actor-Critic) to maximize a pseudo-reward for being “distinguishable” from other skills (\(\log q_\phi(z \mid s)\)), plus an action-entropy regularizer.  
   - Maintain a uniform skill prior to avoid skill collapse.
3. **Emergent Behaviors**: On 2D control or high-DOF locomotion tasks, the method yields skill sets that show running, flipping, bounding, balancing, or other visually distinct routines—without external reward.
4. **Practical Uses**:
   - **Direct Task Solving**: Some discovered skills solve a downstream environment, purely by chance.  
   - **Policy Fine-Tuning**: Skills that partially solve a task can be further trained with the real reward to quickly converge.  
   - **Hierarchical RL**: A meta-policy can sequence or select from the skill repertoire for improved performance on complex tasks.  
   - **Imitation**: Given state-only demonstrations, they pick the skill most likely to produce those states, forming a rough mimic policy.

The authors show extensive experiments illustrating that DIAYN robustly learns distinct behaviors, facilitating exploration, faster learning on new tasks, and solutions to tasks with minimal or no direct reward design.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Adaptive Curiosity Perspective**: DIAYN shares many features with curiosity-driven exploration, focusing on *discovering diverse behaviors that are easily distinguishable.* This can help systematically explore an environment, even if large parts are random or unlearnable.  
- **Partial Randomness**: Some discovered skills may wander into unlearnable or noisy states, but the objective encourages the skill to remain *distinguishable*, which typically requires that the environment transitions be somewhat predictable. This can, in principle, push the policy away from purely random transitions.  
- **Exploratory Benefits**: The method’s success in navigational tasks and high-dimensional locomotion suggests it could be integrated with or complement other curiosity-based techniques to handle partially random dynamics.

Hence, **DIAYN is indeed relevant** to researchers interested in adaptive or curiosity-driven RL, especially for skill discovery in partially random or complex environments.

---

### Worth Citing?

**Yes.** This paper is a key reference for:
1. **Unsupervised Skill Discovery**: Formalizes a successful information-theoretic approach.  
2. **Hierarchical RL**: Demonstrates how unsupervised skill learning can simplify subsequent tasks.  
3. **Practical Implementation**: Combines a standard RL algorithm (SAC) with a discriminative classifier to realize the theoretical objective in continuous, high-dimensional domains.

It strongly influences research on general exploration, skill acquisition, and reward-free RL pretraining.

---

### How It May Inform Future Research

1. **Hybrid Methods**: Combining DIAYN with other curiosity signals (e.g., ensemble disagreement, count-based exploration) might better handle partially random or high-stochasticity domains.  
2. **Skill Priors**: Although the authors fix \(p(z)\) to be uniform, advanced scheduling or shaping the skill prior could guide specialized sub-regions or tasks.  
3. **Deep Hierarchies**: The demonstration of a meta-controller for skill selection could be extended to multiple hierarchical layers or compositional skill usage in extremely sparse tasks.  
4. **Real-World Robotics**: DIAYN could drive novel behaviors in real robotics, offering unsupervised skill sets prior to any user-defined task, potentially mitigating reward-engineering or exploration difficulties.

---

### Open Questions or Possible Critiques

- **Skill Redundancy**: Some environments may yield many “near-duplicate” skills if they are only trivially different. Reducing overlap or enforcing skill coverage more explicitly might improve performance.  
- **State vs. Action**: The method uses state-based discrimination. In partially random environments, parts of the state space might be dominated by noise. Additional nuance (like partial state shaping or factoring out uncontrollable variables) could help.  
- **Scalability**: For environments with extremely large or entangled state spaces, simply increasing the number of skill indices might not suffice. Approaches to automatically grow or shrink skill sets remain underexplored.  
- **Long-Horizon Dependencies**: The method focuses on single-episode skill execution. More sophisticated approaches might partition an environment over multiple steps or incorporate memory for partially observable tasks.
