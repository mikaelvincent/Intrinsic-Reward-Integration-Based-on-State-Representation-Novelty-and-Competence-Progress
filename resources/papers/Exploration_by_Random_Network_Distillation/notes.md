# Exploration by Random Network Distillation

> **Authors**: Yuri Burda, Harrison Edwards, Amos Storkey, Oleg Klimov
> **Date**: 30 October 2018
> **Link**: <https://doi.org/10.48550/arXiv.1810.12894>

---

## Notes

### Selected Direct Quotes and Formulas

- **Problem Statement**  
  > “Reinforcement learning (RL) methods work well when the environment has dense rewards [...] but tend to fail when the rewards are sparse and hard to find. [...] In these situations methods that explore the environment in a directed way are necessary.”

- **Definition of Random Network Distillation (RND)**  
  The authors introduce a two-network setup:
  1. A **randomly initialized target network** \( f(\cdot) \), whose parameters remain fixed.  
  2. A **predictor network** \( f_\phi(\cdot) \), which is trained via gradient descent to **predict** the random features produced by the target network.

  The **intrinsic reward** at time \( t \) is:
  \[
    i_t \;=\; \| f_\phi(s_{t+1}) \;-\; f(s_{t+1}) \|^2,
  \]
  where \( s_{t+1} \) is the next observation and \( \|\cdot\|^2\) denotes mean-squared error (MSE).  
  High prediction error signals novelty, because the predictor has seen few similar states.

- **Non-Episodic vs. Episodic Intrinsic Rewards**  
  > “We argue that treating the stream of intrinsic rewards as non-episodic can be beneficial [...] enabling the agent to remain curious beyond episode boundaries.”

- **Combining Intrinsic and Extrinsic Returns**  
  The authors propose maintaining **two separate value functions**:
  \[
    V(s) \;=\; V_E(s) \;+\; V_I(s),
  \]
  where \( V_E \) corresponds to extrinsic returns (episodic) and \( V_I \) corresponds to intrinsic returns (possibly non-episodic). Each value function is fit with its own target returns, which can have different discount factors (\(\gamma_E \neq \gamma_I\)).

- **Avoiding the “Noisy TV” Problem**  
  By having the target network be deterministic, RND aims to avoid excessive reward from purely stochastic transitions (such as random noise).  
  > “RND obviates factors of aleatoric uncertainty in the environment since the target function can be chosen to be deterministic and inside the model-class of the predictor.”

- **Summary of Main Equations**  

  - **RND Loss** (distillation):  
    \[
      \min_{\phi} \;\mathbb{E}_{x \sim D}\,\bigl\|\,f_\phi(x)\,-\,f(x)\bigr\|^2,
    \]  
    where \( f \) is the fixed, randomly initialized target network, and \( f_\phi \) is the predictor.

  - **Overall Reward**:  
    \[
      r_t \;=\; e_t \;+\; i_t,
    \]
    with \( e_t \) as extrinsic reward from the environment, and \( i_t = \|f_\phi(s_{t+1}) - f(s_{t+1})\|^2 \).

  - **Separate Value Heads**:  
    \[
      R \;=\; R_E \;+\; R_I, \quad
      V \;=\; V_E \;+\; V_I,
    \]
    fitting each with its own discount factor.

- **Practical Implementation Details**  
  - They normalize observations and intrinsic rewards to maintain a stable scale across environments and training stages.  
  - The predictor and target networks share the same CNN-based architecture, but only the predictor is trained.  
  - They use PPO (Proximal Policy Optimization) with 128 parallel environment copies and update the predictor to minimize the MSE.  
  - They further analyze the effect of increasing parallel rollouts (256, 1024) on exploration performance.

- **Key Experimental Findings**  
  1. **Pure Exploration**: Using only RND-based intrinsic rewards on Montezuma’s Revenge (without extrinsic signals) still drives exploration and yields non-zero game scores because some environment interactions (e.g., collecting keys) unlock new areas.  
  2. **Non-Episodic Intrinsic Rewards** outperform episodic intrinsic signals in terms of discovering more rooms in Montezuma’s Revenge.  
  3. **Two Value Heads**: Splitting value estimation for extrinsic and intrinsic streams can help handle differing discount factors (extrinsic \(\gamma_E\) vs. intrinsic \(\gamma_I\)).  
  4. **Scaling Up**: More parallel environments (and correspondingly careful batch-size management for the predictor) improves exploration coverage.  
  5. **Comparison to Forward Dynamics Prediction**: A standard forward-dynamics-based exploration bonus struggles with partial observability and inherent environment stochasticity (the “noisy TV” effect). RND avoids these pitfalls more effectively.  
  6. **Hard Atari Games**: RND achieves new state-of-the-art or near-state-of-the-art performance on Montezuma’s Revenge, Venture, and Gravitar in a pure RL setting (no expert demonstrations, no direct access to emulator states).

### Concise Summary of the Article

The authors propose **Random Network Distillation (RND)** as a simple yet powerful approach for **exploration** in deep reinforcement learning. A **fixed, randomly initialized network** maps states to feature embeddings. A **trainable predictor** network is then penalized for failing to replicate these features, creating an **intrinsic reward** signal reflective of a state’s novelty.

One key aim is to **avoid extraneous exploration** caused by environment noise. Because the target network is deterministic, purely random or stochastic environment transitions do not indefinitely produce high intrinsic rewards—unlike forward-dynamics prediction. The authors integrate RND into **PPO**, a standard on-policy RL method, and train both extrinsic (episodic) and intrinsic (non-episodic) value functions separately for flexibility in discounting.

Experiments focus on **hard exploration Atari 2600 games**—notoriously dominated by sparse rewards. RND outperforms vanilla PPO on Montezuma’s Revenge, Venture, and Private Eye and matches or exceeds leading baselines on Gravitar. Notably, it surpasses average human performance on Montezuma’s Revenge without specialized demonstrations or emulator-state features. Further ablations reveal that **non-episodic curiosity** fosters deeper, more persistent exploration across episodes, while **scaling up parallel training** quickens policy adaptation to ephemeral intrinsic rewards.

### Relevance to "Adaptive Curiosity for Exploration in Partially Random RL Environments"

- **Partial Randomness**: RND specifically aims to reduce excessive exploration bonus from stochastic transitions (e.g., random noise). This is directly applicable to partially random environments where some transitions are uncontrollable noise.  
- **Adaptive Curiosity**: By focusing on novel states that yield high prediction error in the **deterministic** latent embedding, RND helps the agent adaptively seek real novelty rather than random or uninformative outcomes.  
- **Design Simplicity**: The RND approach is relatively lightweight (just one forward pass in a predictor network) and can scale to large or parallel training scenarios, aligning well with real-world or high-dimensional tasks that exhibit partial randomness.

Hence, RND is **worth citing** for methods that address “noisy” or partially random domains since it avoids many of the pitfalls of forward-dynamics prediction, primarily the “noisy TV” effect.  

### How It May Inform Future Research

1. **Long-Horizon Exploration**: The paper notes RND’s limit when an agent must sacrifice immediate gains (like using or not using keys early) for higher future returns. Future work might explore hierarchical or goal-conditioned versions of RND.  
2. **Hybrid Intrinsic Rewards**: RND could be integrated with other curiosity signals (e.g., count-based or Bayesian approaches) in a multi-head design, to see if synergy emerges in partially random tasks.  
3. **Combined Model-Based and Model-Free**: Extending RND in model-based RL frameworks might reduce environment interactions by planning in novel latent states.  
4. **Real-World Robotics**: Observing how RND deals with sensor noise, partial observability, and domain shift may inspire new “robust” curiosity modules.

### Open Questions or Critiques

- **Global vs. Local Exploration**  
  The paper shows that local novelty-seeking works well for certain tasks, but handling global or long-horizon exploration tasks remains challenging, especially where delayed, sparse signals require strategic “key usage” or skipping local rewards to unlock bigger novel areas later.
  
- **Sensitivity to Normalization**  
  The authors stress the importance of carefully normalizing observations and intrinsic rewards. Future research can probe how crucial these hyperparameters are and whether fully automatic normalization or dynamic scaling can further enhance reliability.

- **Potential Over-Fitting of Predictor**  
  While the authors note that standard gradient-based methods do not trivially overgeneralize to unseen states, more extensive studies could explore corner cases or extremely large state spaces (e.g., complex 3D environments).

- **Recurrent Policies**  
  Performance differences between CNN-only and RNN-based architectures were sometimes inconsistent. Additional systematic evaluation might clarify in which partially observable environments RND genuinely benefits from recurrent state tracking versus simpler feedforward policies.
