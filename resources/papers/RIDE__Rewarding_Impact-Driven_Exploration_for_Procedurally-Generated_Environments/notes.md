# RIDE: Rewarding Impact-Driven Exploration for Procedurally-Generated Environments

> **Authors**: Roberta Raileanu, Tim Rocktäschel
> **Date**: 29 February 2020
> **Link**: <https://doi.org/10.48550/arXiv.2002.12292>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **High-Level Motivation**  
  > “Instead of solely relying on extrinsic rewards provided by the environment, many state-of-the-art methods use intrinsic rewards to encourage exploration. However, we show that existing methods fall short in procedurally-generated environments where an agent is unlikely to visit a state more than once.”

- **Novel Exploration Bonus**  
  The authors propose **RIDE** (Rewarding Impact-Driven Exploration):  
  > “We propose a novel type of intrinsic reward which encourages the agent to take actions that lead to significant changes in its learned state representation.”

- **Procedurally-Generated vs. Singleton Environments**  
  A **singleton** environment has the same layout/initial conditions across episodes. Hard-exploration domains like Montezuma’s Revenge or Mario often use a single environment instance. By contrast, **procedurally-generated** environments vary each episode (e.g., random maze layouts in MiniGrid).  
  > “In such settings, [existing] agents are less effective because they rarely see the same state more than once, weakening typical novelty-based or forward-dynamics-based intrinsic bonuses.”

- **Core Definitions**  
  1. **Embedding**: A learned representation \(\phi(s)\) using both forward and inverse dynamics losses (similar to ICM in Pathak et al. 2017).  
     - Forward dynamics: predict \(\phi(s_{t+1})\) from \(\phi(s_t)\) and \(a_t\).  
     - Inverse dynamics: predict \(a_t\) from \(\phi(s_t)\) and \(\phi(s_{t+1})\).
  2. **Intrinsic Reward**:  
     \[
       r^i_t \;=\; \frac{\|\phi(s_{t+1}) - \phi(s_t)\|_2}{N_{\text{ep}}(s_{t+1})}
     \]
     where \(N_{\text{ep}}(s_{t+1})\) is the number of times \(s_{t+1}\) has been visited **in the current episode**. This discounting by episode-level visitation aims to prevent back-and-forth toggling between two states that produce large embedding differences.

- **Key Equations**  
  - **Forward Loss**:  
    \[
      L_{\mathrm{fw}} = \bigl\|\phi(s_{t+1}) - f_{\mathrm{fw}}\bigl(\phi(s_t), a_t\bigr)\bigr\|_2^2
    \]
  - **Inverse Loss** (for discrete actions):  
    \[
      L_{\mathrm{inv}} = \mathrm{CrossEntropy}\bigl(a_t,\; f_{\mathrm{inv}}(\phi(s_t), \phi(s_{t+1}))\bigr)
    \]
  - **Overall RL Objective**:  
    \[
      \min \Bigl[L_{\mathrm{RL}}(\theta)\;+\;\alpha_{\mathrm{fw}}\,L_{\mathrm{fw}}+\;\alpha_{\mathrm{inv}}\,L_{\mathrm{inv}}\Bigr]
    \]
    with \(\theta\) as the policy parameters. The embedding parameters are not updated by RL’s reward gradient.

- **Advantages Over Curiosity-Driven** (ICM)  
  > “One problem with [standard curiosity] is that the bonus vanishes once the forward model becomes accurate. By contrast, RIDE’s impact-based reward remains meaningful—even if the forward model is well trained—because it measures the difference in representations of consecutive states.”

- **Experiments**  
  1. **MiniGrid**: A collection of procedurally-generated 2D grid mazes with partial observations.  
     - Hard tasks: MultiRoomN12S10, ObstructedMaze2Dlh, KeyCorridorS3R3, etc.  
     - RIDE outperforms baselines (ICM, RND, Count, IMPALA) on final success rates and sample efficiency.  
     - Especially in large or locked mazes, RIDE is the only method that can consistently solve them.  
  2. **Noisy TV**: Adding a “ball” whose color changes randomly. Curiosity (ICM) is attracted to it because it remains unpredictable, but RIDE is robust (the color does not truly shift the agent’s controllable representation).  
  3. **Singleton Settings**: In tasks with a single environment layout (e.g., some Maze or Mario level), standard exploration methods can eventually succeed. But in **procedurally-generated** tasks (each new episode randomizes the environment layout), RIDE maintains a strong advantage.  
  4. **High-Dimensional Visual Tasks**: On VizDoom or Mario, RIDE often performs on par or better than ICM and other exploration bonuses, though these tasks may not be as challenging as some large MiniGrid mazes.
- **Analysis of Intrinsic Reward**  
  - RIDE consistently rewards *interactive actions* (e.g., opening doors, picking up keys) more than turning or moving in open space.  
  - Distributions of per-action intrinsic rewards for RIDE remain relatively higher and do not collapse to near-zero, unlike curiosity-based approaches.  
  - RIDE also helps reduce “reward diminishing” phenomena as training progresses.

- **Open-World or Procedural Setting**  
  > “Existing methods typically assume a limited or deterministic environment, so states may reoccur. But with large randomization, novelty-based or forward-error-based methods become less discriminative, or their bonus saturates. RIDE focuses on agent-controllable changes in state representation, thus remains a reliable signal over long training.”

---

### Concise Summary of the Article

**"RIDE"** is an **intrinsic motivation** technique intended for **sparse reward** and **procedurally-generated** environments, where standard novelty or curiosity methods often fail:

1. **State Embedding**  
   Learned via forward and inverse dynamics (similar to ICM) to focus on controllable aspects of the environment.  
2. **Impact-Driven Reward**  
   The agent’s intrinsic bonus is the distance between consecutive state embeddings, discounted by an episodic visitation count. Thus, repeated toggling of the same states yields diminishing rewards, while impactful, environment-altering actions remain appealing.  
3. **Results**  
   - Solves significantly harder MiniGrid tasks than prior baselines.  
   - Robust to “noisy TV” effects because truly random or uncontrollable changes in the environment do not produce large embedding differences.  
   - On single-environment tasks like Mario or VizDoom, performs on par or better than standard curiosity methods (ICM, RND).  
4. **Key Insight**  
   RIDE’s design ensures the intrinsic reward remains high whenever the agent takes actions that meaningfully alter the environment in a controllable way, avoiding the quick decay in novelty-based exploration or the infinite loop at random noise sources.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: RIDE explicitly addresses the “noisy TV” pitfall that plagues naive curiosity. It discounts uncontrollable or purely random changes in the agent’s learned representation.  
- **Adaptive Curiosity**: By focusing on *agent-controllable environment changes*, RIDE’s exploration bonus remains relevant through training and across diverse environment seeds. This is highly applicable to partially random domains where naive novelty signals might be swamped by ephemeral noise.  
- **Worth Citing?** Yes. The method stands out for robust exploration in large, randomized tasks; it also demonstrates strong performance on tasks where prior methods degrade.

---

### How It May Inform Future Research

1. **Longer-Horizon Impact**: RIDE currently measures immediate changes in representation. Future research might extend “impact-driven exploration” to multi-step or cumulative environment transformations, possibly combining with hierarchical RL.  
2. **Selective Impact**: Current RIDE lumps all controllable changes into a single measure. One could refine “desirable” vs. “undesirable” impact or incorporate domain knowledge to limit exploring destructive changes.  
3. **Safe Exploration**: By focusing on environment changes, RIDE might inadvertently encourage risky or high-impact actions. Incorporating safety constraints or penalty signals could yield safer, targeted exploration in partially random real-world tasks.  
4. **Combining with Other Intrinsic Rewards**: A synergy might arise by adding a small novelty or curiosity bonus on top of RIDE to ensure coverage of unseen areas, while still prioritizing controllable transitions.

---

### Open Questions or Possible Critiques

- **Entropy vs. Impact**: RIDE relies on standard policy entropy to avoid trivial loops. Without that, the agent might exploit large representational differences. Further analysis could clarify the interplay between policy entropy and RIDE’s episodic discount.  
- **Fully Stochastic Subregions**: If certain environment sections are entirely random yet accessible, RIDE might give zero intrinsic incentive to investigate them. Could that hamper exploration of states that are partially random but still relevant?  
- **Representation Collapse**: Although less likely than with pure forward-error methods, the representation could in principle learn to flatten some differences. Additional constraints or regularizers might ensure it encodes truly controllable aspects.  
- **Complex 3D or Real Robot**: While the authors show results on VizDoom, real robotics tasks might have more nuanced partial observability or continuous action spaces. Additional design (e.g., modeling partial random transitions) might be needed for robust real-world performance.
