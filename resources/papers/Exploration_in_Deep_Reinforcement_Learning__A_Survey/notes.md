# Exploration in Deep Reinforcement Learning: A Survey

> **Link**: <https://doi.org/10.1016/j.inffus.2022.03.003>

> **Parenthetical**: (Ladosz et al., 2022)
> **Narrative**: Ladosz et al. (2022)

---

## Notes

### Selected Direct Quotes and Formulas

- **Sparse Rewards and the Need for Exploration**  
  > “In numerous real-world problems, the outcomes of a certain event are only visible after a significant number of other events have occurred. [...] It is challenging for reinforcement learning to learn rewards and actions association. Thus more sophisticated exploration methods need to be devised.”

- **Definition of Exploration**  
  > “Exploration can be defined as the activity of searching and finding out about something [24]. [...] In the context of reinforcement learning, something is a reward function, and the searching and finding is an agent’s attempt to try to maximize the reward function.”

- **Noisy-TV Problem**  
  > “In a noisy-TV problem, the agent is stuck in exploring an infinite number of states which lead to no reward. [...] The agent will experience novelty all the time. This keeps the agent’s attention high infinitely but clearly leads to no meaningful progress.”

- **Reward Novel States**  
  The paper defines an intrinsic reward approach where the agent gets an additional reward \(r_\mathrm{int}\) for visiting novel states:
  \[
    r_\mathrm{int} = f\bigl(z(s_{t+1}) - M\bigl(z(s_t, a_t)\bigr)\bigr),
  \]
  where \(z\) is an optional representation function, \(M\) is a predictive model, and \(f\) is a reward-scaling function.  

- **Count-Based Exploration**  
  The review highlights a key method:
  \[
    \text{Intrinsic Reward} \, \propto \,\frac{1}{N(s)},
  \]
  where \(N(s)\) is the count of visits to state \(s\). For large state spaces, a reduced representation or density estimation is used instead of raw state counts.

- **Reward Diverse Behaviors**  
  > “In reward diverse behaviours, the agent collects as many different experiences as possible, making exploration an objective rather than a reward finding.”

- **Goal-Based Methods**  
  The article emphasizes two main categories:
  1. **Goals to Explore From**: selecting or storing states/trajectories (e.g., in a buffer) to revisit as a starting point for new exploration.  
  2. **Exploratory Goal**: meta-controllers, sub-goal discovery, and uncertain-state targeting to guide exploration.

- **Optimistic vs. Uncertainty Approaches**  
  The survey distinguishes these probabilistic methods:  
  - **Optimistic**: rely on the optimism-under-uncertainty principle, e.g., upper confidence bounds on rewards.  
  - **Uncertainty**: maintain a distribution over states/actions (Bayesian or ensembles) and reduce uncertainty by visiting unknown or uncertain regions.

- **Imitation for Exploration**  
  Two main branches:  
  1. **Imitations in Experience Replay**: mixing demonstration data with agent-collected data in a shared buffer.  
  2. **Imitation with an Exploration Strategy**: using demonstrations to kick-start exploration or to shape intrinsic reward/auxiliary objectives.

- **Safe Exploration**  
  Approaches include:  
  1. **Human Designer Knowledge**: explicit constraints or baseline safe policies.  
  2. **Prediction Models**: agent learns to predict unsafe outcomes and avoids them.  
  3. **Auxiliary Rewards**: punishing behaviors that lead to catastrophic states.

- **Random-Based Exploration Enhancements**  
  - **Exploration Parameters**: dynamically tuning \(\epsilon\)-greedy or other random rates based on learning progress.  
  - **Parameter Noise**: injecting noise in network parameters to encourage exploration.

- **Future Challenges**  
  1. **Evaluation and Metrics**: lack of standardized benchmarks, inconsistent reporting of results.  
  2. **Scalability**: real-world tasks often demand millions of samples, a bottleneck for real robotic or large-scale scenarios.  
  3. **Exploration-Exploitation Dilemma**: balancing them remains an open question, especially in complex or continuous domains.  
  4. **Intrinsic Rewards**: automatically learned self-rewards might be more powerful than manually engineered forms.  
  5. **Noisy-TV Problem**: partially addressed by memory or clustering approaches but not definitively solved.  
  6. **Safety**: truly safe exploration with minimal reliance on hand-designed constraints is still largely unsolved.  
  7. **Transferability**: many methods overfit to their training domain and fail to generalize to new tasks.

---

### Concise Summary of the Article

This survey provides a thorough examination of *exploration* techniques in deep reinforcement learning (DRL). It begins with a discussion of why exploration is challenging (sparse rewards, the “noisy-TV” trap), then systematically categorizes existing exploration strategies:

- **Reward Novel States**: Intrinsic motivation via prediction error, state counts, or memory-based novelty.  
- **Reward Diverse Behaviors**: Evolving or learning multiple policies/skills that differ substantially from one another.  
- **Goal-Based**: Explicitly setting intermediate or exploratory goals to push the agent toward underexplored states.  
- **Probabilistic**: Bayesian or ensemble-based approaches that exploit optimism or uncertainty.  
- **Imitation-Based**: Leveraging demonstration data for jump-starting exploration or shaping additional learning objectives.  
- **Safe Exploration**: Limiting catastrophic outcomes with rule-based constraints, baseline safe policies, or negative penalties.  
- **Random-Based**: Modifying standard random exploration (e.g., adaptive \(\epsilon\)-greedy, noisy parameters).

The paper concludes that while some methods (like goal-based or intrinsic curiosity) achieve impressive results in hard-exploration Atari tasks, fundamental challenges persist—especially in large, real-world scenarios. The authors propose research directions including more rigorous evaluation, better state-space representations, and novel ways to handle the exploration-exploitation trade-off without extensive hand-designed heuristics.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: The survey’s discussion of the “noisy-TV” problem and other purely stochastic scenarios is highly relevant for partially random RL environments. The authors outline how memory, uncertainty, or clustering can (partially) mitigate the agent’s infinite attraction to meaningless noise.
- **Adaptive Curiosity**: Many methods described—particularly those in “Reward Novel States” and “Uncertainty-Based” exploration—overlap with adaptive curiosity concepts, where intrinsic rewards focus on *information gain* or *novelty*. The survey’s coverage of count-based, prediction-error-based, and ensemble disagreement methods ties directly to robust exploration in environments with inherent randomness.
- **Worth Citing**: **Yes.** This survey organizes a wide range of exploration algorithms from foundational to advanced. Its theoretical discussion of common pitfalls (sparse rewards, couch-potato problem) is extremely relevant for any research or project dealing with partially random or stochastic transitions.

---

### How It May Inform Future Research

1. **Advanced Intrinsic Reward Schemes**  
   Researchers interested in partially random or noisy tasks might design new self-supervised signals that better discriminate between *truly stochastic states* versus *novel informative states*.
2. **Combining Methods**  
   The survey highlights that many approaches can be combined (e.g., goal-based + count-based, imitation + curiosity). For adaptive curiosity, synergy across methods may improve resilience to random transitions.
3. **Safe Exploration Under Noise**  
   The paper notes that safe exploration frameworks are still immature, especially in unpredictable domains. Future work could extend “adaptive curiosity” with safety constraints that specifically address partial randomness.

---

### Open Questions or Possible Critiques

- **Long-Term vs. Short-Term Novelty**  
  Balancing immediate novelty (which might be random noise) with more strategic or *longer-term* exploration remains an unresolved challenge.  
- **Scalability and Transfer**  
  Many algorithms in the survey excel in specific benchmarks but are untested in large-scale or real-world tasks with partial observability and domain shifts.  
- **Sparse Evaluations**  
  The paper calls for standardized metrics and consistent reporting. The varying scope of tasks and incomplete performance measures hamper direct method-to-method comparisons.
