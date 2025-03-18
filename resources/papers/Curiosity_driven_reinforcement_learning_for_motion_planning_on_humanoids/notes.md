# Curiosity driven reinforcement learning for motion planning on humanoids

> **Authors**: Mikhail Frank, Jürgen Leitner, Marijn Stollenga, Alexander Förster, Jürgen Schmidhuber
> **Date**: 6 January 2014
> **Link**: <https://doi.org/10.3389/fnbot.2013.00025>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Motivation**  
  > “To study AC in a more realistic setting, we embody a curious agent in the complex iCub humanoid robot. [...] To the best of our knowledge, this is the first ever embodied, curious agent for real-time motion planning on a humanoid.”

- **Artificial Curiosity (AC) and Learning Progress**  
  > “Artificial Curiosity (AC) refers to directed exploration driven by a world model-dependent value function designed to direct the agent toward regions where it can learn something. [...] the reward should actually be based on the learning progress, as the previous agent was motivated to fixate on inherently unpredictable regions of the environment.”

- **Core Formulation**  
  The authors model the robot’s configuration space as a discrete **Markov Decision Process (MDP)**:
  \[
  \langle S,\ A,\ T,\ R,\ \gamma \rangle,
  \]
  where \(S\) is a finite set of states, \(A\) the action set, \(T\) the state transition probabilities, \(R\) a reward function, and \(\gamma\) a discount factor. Here,
  1. **States** (\(s \in S\)) are defined via Voronoi regions around a set of sampled configurations \(q_j \in Q\).  
  2. **Actions** move the robot from a current state \(s\) toward a goal state \(s_{g(a)}\) by setting an “attractor” in a low-level controller.  
  3. **Transition probabilities** \(T(s,a)\) can be deterministic or non-deterministic if constraints (e.g., collisions) vary or if the robot’s internal mechanics behave unpredictably.  
  4. **Intrinsic Reward** is based on **information gain**, computed via a Kullback-Leibler (KL) divergence:
     \[
       R_{\text{intrinsic}}(s,a) \;=\; D_{\mathrm{KL}}\bigl(P\;\|\;T(s,a)\bigr),
     \]
     capturing how much the model of state-action transitions changes after a new observation.

- **Optimistic Initialization**  
  The authors define a dynamic, sparse representation for transition distributions, incrementally appending bins to track newly observed outcomes. They initialize each action with a small uniform prior or empty distribution, ensuring a one-time nonzero reward after the first novel outcome (thus accelerating early exploration).

- **Low-Level Control (MoBeE)**  
  The iCub’s attractor-based controller is described by a second-order dynamical system:
  \[
    M \ddot{q}(t) + C \dot{q}(t) + K \bigl(q(t) - q^*\bigr) \;=\; f_i(t),
  \]
  where \(q^*\) is the “attractor” (goal configuration), and \(f_i(t)\) imposes real-time constraint forces to avoid collisions, joint limit violations, or cable length issues.

- **Experimental Setup**

  1. **Single-Arm Experiment**  
     - States sample 4 DOFs (three shoulder joints, one elbow).  
     - 81 states (3 samples per joint) each with 16 nearest neighbors (total 1296 state-actions).  
     - The robot must learn to avoid self-collisions and cable-length constraints.  
     - *Comparison of exploration strategies*:  
       - **AC** (information gain) vs. **RAND** (random) vs. **LT** (“least tried” action).  
     - Observations:  
       - AC explores much more efficiently (covers space sooner, more uniform coverage).  
       - AC focuses on interesting transitions (where constraints are encountered) and quickly becomes “bored” with repeated, predictable transitions.

  2. **Multi-Agent (Arms + Torso) Experiment**  
     - 3 separate RL agents: left arm, right arm, torso. Each manages its own smaller MDP.  
     - *Parallel learning*: none of the agents sees the other’s state, but they indirectly affect each other by moving the shared body.  
     - The environment includes a table. Sometimes an arm can collide with the table if the torso is bent forward.  
     - *Emergent behavior*: The robot systematically explores the table surface. Collisions with the table produce interesting or surprising transitions for the arms, prolonging curiosity.  
     - Demonstrates potential for partial environment “dynamics” (the torso motion changes what is feasible for the arms).

- **KL Divergence for Intrinsic Reward**  
  The reward for a state-action \( (s,a) \) changes as the transition probability distribution \(T(s,a)\) updates with new outcomes:
  \[
    R(s,a) \;=\; D_{\mathrm{KL}}\bigl(P \,\|\, T(s,a)\bigr).
  \]
  This ensures that repeated outcomes reduce curiosity, while truly new or more uncertain transitions keep the agent exploring.

- **Implementation Details**  
  - Uses **Value Iteration** with discount factor \(\gamma = 0.9\).  
  - Intrinsic reward decays as transitions become predictable (like “boredom”).  
  - Real-world iCub experiments last several hours or days due to physical motion times.  
  - The controller enforces collisions/joint-limit constraints at a high frequency, while RL transitions occur at a much slower rate (on the order of seconds per action).

### Concise Summary of the Article

Frank et al. present a **curiosity-driven RL method** for motion planning on the high-DOF iCub humanoid robot. They discretize the robot’s configuration space into states (Voronoi cells around chosen joint configurations) and define actions by setting an attractor for a low-level, reactive, physics-based controller (MoBeE). The RL agent learns a Markov Decision Process capturing transition probabilities—essentially discovering a “roadmap” to reach configuration goals while respecting dynamic constraints (collisions, cable limitations).

**Key Insight**:  
They use **artificial curiosity**—an intrinsic reward defined via **KL divergence** between predicted and updated transition distributions. This motivates the robot to explore transitions that yield the greatest learning progress (information gain). Over repeated trials:

- **Single-Arm** scenario: the agent quickly identifies self-collision constraints and invests minimal repeated exploration time on predictable transitions.  
- **Multi-Agent** (both arms + torso): partial observability across agents leads to emergent table interaction (bending forward changes reachable states for the arms, making collisions with the table “interesting”).  

The experiments validate that **AC-based exploration** significantly accelerates coverage of the state-action space while focusing on novel or uncertain regions. The resulting MDP effectively functions as a robust path planner that can adapt to the iCub’s nonlinearity and unpredictability, unlike classical “plan first, act later” approaches which can fail for flexible, cable-driven robots.

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partially Random Transitions**: The authors highlight that even in a nominally “static” environment, the iCub’s internal mechanics can introduce nondeterministic transitions. The approach systematically identifies these uncertain or surprising transitions and invests learning effort there—*exactly* what adaptive curiosity seeks to do in partially random contexts.  
- **Continuous High-DOF Robot**: Demonstrates how curiosity-driven exploration can scale to multi-DOF humanoids. The robot naturally zeroes in on “unusual” constraints or collisions, ignoring repetitive or trivial configurations. This parallels partial randomness, where some transitions may be inherently unpredictable, warranting special attention.

Hence, the paper is **strongly relevant**: it shows how an intrinsic reward shaped by information gain can handle unpredictability in a complex robotic system, effectively bridging AC with real-world challenges.

### Worth Citing?

**Yes.** This work is among the few that applies *intrinsic motivation/curiosity-based RL* to a **high-dimensional humanoid** in **real-time**. It directly addresses scaling concerns, embodying AC in an advanced robotic platform. Its demonstration of emergent table exploration underscores AC’s ability to discover interesting constraints automatically. Researchers exploring “adaptive curiosity in partially random RL” will find a valuable reference for real-world, high-DOF scenarios.

### How It May Inform Future Research

1. **Hierarchical Agents**  
   - The authors mention potential hierarchical layers, where “interesting” actions become the parent agent’s sub-actions. This concept can unify multi-agent or multi-level exploration across many DOFs.  
2. **Automatic State-Space Generation**  
   - They handpicked uniform samples for states. Future efforts might adaptively refine or expand the sample set based on measured curiosity signals (high KL divergence regions).  
3. **Task-agnostic vs. Task-focused**  
   - Integrating extrinsic goals with curiosity-based exploration can allow the system to pivot quickly from open-ended exploration to purposeful tasks.  
4. **Non-Static Constraints**  
   - They note the approach works even as the workspace changes. Expanding on partially or fully random environmental factors could deepen the synergy with adaptive curiosity in dynamic settings.

### Open Questions or Possible Critiques

- **State Space Bootstrap**  
  The method relies on a manually chosen discrete state lattice. It is unclear how the agent might refine or expand states online to capture more nuanced sub-regions.  
- **Long Learning Times**  
  Physical experiments took hours or days, which might be prohibitive for more complex tasks or additional DOFs. Methods to accelerate real-world data collection—simulation pre-training, more efficient exploration—remain open challenges.  
- **Hierarchical Communication**  
  While multiple agents controlling different body parts is scalable, the formal approach to coordinate or share partial states between them is not fully explored. Sub-goal discovery might further improve synergy across DOFs.  
- **Handling Repeated Intrinsic Rewards**  
  They focus on single-step transitions, but a multi-step curiosity approach (longer horizon planning) might reveal deeper partial randomness or synergy among constraints.
