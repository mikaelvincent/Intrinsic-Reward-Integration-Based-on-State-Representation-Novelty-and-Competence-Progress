# Curiosity-driven Exploration by Self-supervised Prediction

> **Authors**: Deepak Pathak, Pulkit Agrawal, Alexei A. Efros, Trevor Darrell
> **Date**: 15 May 2017
> **Link**: <https://doi.org/10.48550/arXiv.1705.05363>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Formulation of Intrinsic Curiosity**  
  > “We formulate curiosity as the error in an agent’s ability to predict the consequence of its own actions in a visual feature space learned by a self-supervised inverse dynamics model.”  

  **Key objective**: The agent’s intrinsic reward \( r_t^i \) is the prediction error of a forward dynamics model in a learned feature space:  
  \[
    r_t^i = \| \hat{\phi}(s_{t+1}) - \phi(s_{t+1}) \|^2,
  \]  
  where \(\phi(s)\) is a learned embedding of raw observations \(s\), and \(\hat{\phi}(s_{t+1})\) is the predicted embedding for next state \(s_{t+1}\).

- **Forward and Inverse Models**  
  The approach, named **ICM** (Intrinsic Curiosity Module), uses:
  1. **Inverse Dynamics**:  
     \[
       a_t = g(\phi(s_t), \phi(s_{t+1}); \mathbf{I}),
     \]  
     to learn a feature space that focuses on aspects of the environment relevant to the agent’s actions.  
  2. **Forward Dynamics**:  
     \[
       \hat{\phi}(s_{t+1}) = f\bigl(\phi(s_t), a_t; \mathbf{F}\bigr).
     \]
  The agent is rewarded by the forward model’s error in this feature space:
  \[
    r_t^i = \|\hat{\phi}(s_{t+1}) - \phi(s_{t+1})\|^2.
  \]

- **Pixel-Based Curiosity vs. Feature-Based**  
  They compare a naive version that predicts raw pixels \(\hat{s}_{t+1}\) versus the proposed feature-based approach that factors out irrelevant noise:
  > “If there is a source of variation in the environment that is inconsequential for the agent, then the agent has no incentive to learn it.”

- **VizDoom 3D Navigation Setup**  
  Sparse reward tasks tested:
  - **Dense**: multiple spawn points, agent is sometimes close to the goal.
  - **Sparse**: fixed spawn in a room far from the goal (270 steps).
  - **Very Sparse**: spawn in an even farther room (350+ steps).
  
  **Performance**:
  - Feature-based ICM + A3C outperforms baseline A3C and pixel-based curiosity in these navigation tasks, especially when the extrinsic reward is extremely sparse.

- **Super Mario Bros**  
  No extrinsic reward, only curiosity:
  > “Without any extrinsic rewards, the agent learns to cross more than 30% of Level-1. It also discovers behaviors like avoiding or killing enemies so that it can explore further.”

- **Generalization Experiments**  
  - Transfer to new levels in Mario:  
    > “A policy pre-trained with only curiosity on Level-1 is able to explore Level-2 or Level-3 faster than a policy trained from scratch.”  
  - Transfer in VizDoom to a new map with different textures. Feature-based curiosity fine-tuned on the new map quickly learns exploration, whereas pixel-based curiosity fails.

- **Robustness to Noise**  
  Adding a large block of white noise to the agent’s observations (40% of the image) disrupts pixel-based curiosity. The feature-based ICM approach remains stable because the inverse model discards uncontrollable distractors.

- **Comparison to VIME**  
  They compare with VIME (a prior method for curiosity based on information gain in parameter space). The ICM approach converges faster and can solve extremely sparse tasks where VIME+TRPO fails.

- **Key Equations**  
  1. **Inverse Model Loss**:  
     \[
       \min_{\mathbf{I}} L_I \bigl(a_t,\, g(\phi(s_t), \phi(s_{t+1}); \mathbf{I})\bigr).
     \]  
  2. **Forward Model Loss**:  
     \[
       \min_{\mathbf{F}} \frac{1}{2} \|\hat{\phi}(s_{t+1}) - \phi(s_{t+1})\|^2.
     \]  
  3. **Curiosity Reward**:  
     \[
       r_t^i = \|\hat{\phi}(s_{t+1}) - \phi(s_{t+1})\|^2.
     \]

---

### Concise Summary of the Article

Pathak et al. introduce an **Intrinsic Curiosity Module (ICM)** that scales to high-dimensional visual state spaces. Instead of predicting raw pixels, the module learns an **inverse dynamics model** to create a latent feature space focusing on controllable aspects of the environment, then uses a **forward dynamics model** in this feature space to compute an intrinsic reward. The key benefits are:

1. **Avoiding Noisy Distractions**: Because the inverse model only encodes features relevant to the agent’s actions, irreducible environment noise (moving leaves, random backgrounds) does not inflate curiosity.
2. **Sparse Reward Settings**: In 3D navigation (VizDoom) with extremely sparse extrinsic rewards, an agent guided by the ICM significantly outperforms baseline A3C or pixel-based curiosity. It learns to traverse multiple rooms or corridors, find distant goals, and avoid local minima.
3. **Reward-Free Exploration**: Without any external reward, the ICM-driven agent exhibits robust exploration: in Super Mario Bros, it explores ~30% of Level-1 purely by curiosity. In VizDoom, it roams multiple rooms or floors.
4. **Generalization**: The feature-based policy transfers better to new tasks or levels (e.g., new Mario levels, new VizDoom maps) than pixel-based curiosity or random exploration, showing that the learned representation and behaviors are not memorized but somewhat general.

Overall, the paper demonstrates a strong approach for curiosity-driven exploration in complex, high-dimensional environments, highlighting that ignoring uncontrollable aspects of the environment is crucial for stable exploration.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partially Random Elements**: ICM deliberately avoids focusing on unpredictable noise (e.g. random backgrounds or distractors) since its embedding is learned by an inverse model that only encodes action-relevant content. This aligns well with the notion of adaptive curiosity in partially random settings, where the agent must ignore unlearnable or irrelevant environment features.
- **Robust Exploration**: The forward model’s error in latent space drives exploration towards *controllable novel states*—a key aspect of handling partially random domains without being trapped by noise or large unlearnable subspaces.

Thus, the paper provides an effective method for **intrinsic motivation** that can robustly handle scenarios with partial randomness.

---

### Worth Citing?

**Yes.** The work is influential, often cited for demonstrating robust curiosity-driven exploration in pixel-based 3D or game environments without extrinsic rewards. It introduces an elegant solution to the “noisy TV” problem by learning a latent space that discards uncontrollable environment factors.

---

### How It May Inform Future Research

1. **Integrating Inverse Model Features**: Future methods might combine ICM’s learned features with other exploration signals (e.g., ensemble disagreement, random distillation) to handle even more complex tasks or partial observability.
2. **Hierarchical Exploration**: ICM can be a building block in a hierarchical scheme. Agents might use the learned curiosity module as a lower-level skill for navigation, while an upper-level policy focuses on larger tasks.
3. **Real-World Robotics**: Applying ICM in real robots could let them explore their environment robustly—learning from camera inputs while ignoring uncontrollable factors like flickering lights or backgrounds.
4. **Combining with Offline Data**: For tasks with limited online interactions, partial offline data might be used to bootstrap the inverse model, enabling faster curiosity-based exploration with fewer environment samples.

---

### Open Questions or Possible Critiques

- **Long-Horizon Dependencies**: The approach might struggle with extremely long sequences of specific actions (like crossing a big pit in Mario). Once curiosity saturates in nearby states, it may not discover the subtle multi-step path needed to proceed further.
- **Reliance on Action-Conditioned Learning**: The inverse model might degrade if actions have ambiguous effects or if the environment can drastically change without agent control. The method assumes environment changes are mostly agent-driven or relevant to the agent.
- **Stalling When No New States Are Reachable**: If the environment has no additional reachable states, the curiosity can drop to zero and the agent might stop exploring. Mechanisms for “escape from local boredom” might be needed.
- **Large Action Spaces**: For tasks with combinatorial or continuous actions, the inverse model might face challenges, and further architectural design or constraints may be required to handle them efficiently.
