# Large-Scale Study of Curiosity-Driven Learning

> **Authors**: Yuri Burda, Harri Edwards, Deepak Pathak, Amos Storkey, Trevor Darrell, Alexei A. Efros
> **Date**: 13 August 2018
> **Link**: <https://doi.org/10.48550/arXiv.1808.04355>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Motivation for Purely Curiosity-Driven RL**  
  > “Reinforcement learning algorithms rely on carefully engineering environment rewards that are extrinsic to the agent. [...] There has been no systematic study of learning with only intrinsic rewards.”  
  The authors conduct a **large-scale** empirical investigation where **no extrinsic reward** is used at training time.

- **Dynamics-Based Curiosity**  
  The paper adopts the method from Pathak et al. (2017), modeling a **forward dynamics** in an embedding space \(\phi(\cdot)\). The **intrinsic reward** is the prediction error of next-state features:
  \[
    r_{t}^i \;=\; \bigl\|\phi(x_{t+1}) - f\bigl(\phi(x_t),\, a_t\bigr)\bigr\|^2,
  \]
  or equivalently using a log-density interpretation:
  \[
    r_{t}^i \;=\; -\log p\!\bigl(\phi(x_{t+1}) \mid \phi(x_t),\, a_t\bigr).
  \]
  The agent is rewarded if the environment’s transitions in feature space are not yet well-predicted by its forward model.

- **Feature Spaces for Prediction**  
  The authors examine several ways to obtain \(\phi(\cdot)\):

  1. **Pixels** (\(\phi(x) = x\)):  
     - Sufficient but typically high-dimensional and **not** compact.  
     - Hard to learn forward dynamics at raw pixel level.
  
  2. **Random Features (RF)**:  
     - A randomly initialized CNN is fixed (no training).  
     - The embedding is stable and compact, but not guaranteed to be fully “sufficient.”  
     - Surprising result: performs well on many standard RL games.
  
  3. **Inverse Dynamics Features (IDF)**:  
     - Learned by predicting the action \(\hat{a}_t\) from consecutive states \((x_t, x_{t+1})\).  
     - Meant to capture agent-controllable aspects, robust to irrelevant distractors.  
     - Potentially not “sufficient” if environment contains important but uncontrollable elements.

  4. **Variational Autoencoder (VAE)**:  
     - Learns a latent representation by reconstructing raw observations.  
     - Typically lower-dimensional but can be unstable online.  
     - Observed to perform on par or below random features in many tested tasks.

  The authors highlight **stability** (features should not keep changing) as crucial in curiosity-driven RL, to avoid further non-stationary reward signals.

- **Implementation Details**  
  1. **No ‘done’ Signal**: They treat episodes as infinite-horizon with discounting. The agent must not rely on environment “episode ends” as a pseudo-reward.  
  2. **Reward Normalization**: The intrinsic reward distribution changes over time. Dividing by a running estimate of standard deviation helps stable value learning.  
  3. **Advantage Normalization**: Used within PPO to stabilize updates.  
  4. **Observation Normalization**: Pre-sampling 10k steps randomly for mean/std.  
  5. **Massive Parallelism**: Typically 128 parallel environments; up to 2048 in some experiments.

- **Pure Curiosity Across 54 Environments**  
  The authors run **no extrinsic reward** (or done signal) training on:

  1. **Atari Games (48)**:  
     - Compare IDF, RF, VAE, raw pixel approaches.  
     - **Outcome**: *Often*, the agent’s policy increases extrinsic game scores anyway. Many games have natural exploration “curricula” that align with novelty-seeking.  
     - RF is surprisingly strong, IDF outperforms RF in ~55% of games.  
     - Some games yield minimal or no extrinsic reward from pure curiosity (like “Atlantis,” “IceHockey,” etc.).  
  2. **Super Mario Bros.**  
     - The curiosity-driven agent passes multiple levels, purely from exploration.  
     - Large batch size (2048 parallel envs) drastically helps.  
  3. **Roboschool**  
     - “Ant” from pixel input: a walking gait emerges purely from curiosity.  
     - “Juggling”: agent learns to intercept two bouncing balls with a paddle.  
  4. **Two-Player Pong**  
     - Both players are curiosity-driven, leading to increasingly long rallies.  
     - The agent “enjoys” exploring new ball trajectories.

- **Generalization to Novel Levels**  
  The authors pre-train a curiosity-based agent on Super Mario Bros. Level 1-1, then transfer to new levels (1-2 or 1-3). They continue curiosity-based training from the pre-trained model (i.e., no extrinsic reward). Observations:

  - **IDF Features**: Transfer better across color or layout changes (day to night).  
  - **Random Features**: Transfer well if the environment’s visual domain is similar, but fail under more drastic changes.

- **Sparse/Terminal Reward**  
  They also test combining small extrinsic signals with curiosity. For a 3D Unity maze, the agent’s terminal reward is +1 for reaching a distant goal. Classic RL alone fails to find it, but curiosity+extrinsic reliably solves the maze. A brief set of results on some “sparse-reward Atari” shows curiosity helps in four out of five tested games.

- **Noisy-TV Problem**  
  A known pitfall of pure prediction-error-based curiosity is that *irreducible* environment randomness (like a “noisy TV” the agent controls) can produce unbounded “novelty.” The authors add a “noisy TV” state to the Unity environment. The agent can keep flipping channels to induce random transitions, generating persistent high prediction error. Indeed, **learning slows dramatically** in the presence of the noisy TV, though eventually the agent may overcome it. They highlight this as a major limitation for future research.

### Concise Summary of the Article

This work conducts the **first large-scale study** of **purely curiosity-driven RL** on a diverse set of 54 environments (Atari, Super Mario, Roboschool, 3D mazes, etc.). Using a **dynamics-based** intrinsic reward (prediction error in a chosen embedding space), the authors show:

1. **Pure Curiosity** can unexpectedly yield strong performance on many standard RL benchmarks, **despite** no extrinsic rewards. Indeed, many environment designs (video games) are “curriculum-like,” naturally aligning novelty-seeking with progress in extrinsic tasks.
2. **Feature Spaces** matter for stable forward dynamics: random CNN embeddings (RF) often work surprisingly well, although learned IDF features transfer better to new levels or domains.
3. **Performance Gains** are significantly enhanced by scaling the RL batch size (more parallel actors, bigger updates).
4. **Curiosity + Sparse Rewards** helps solve tasks that are unsolvable with extrinsic reward alone, e.g. a deep 3D maze with a single +1 goal.
5. **Limitation**: Unavoidable environment stochasticity—especially action-contingent randomness—can confound the predictor-based curiosity. The agent may get “stuck” in a “noisy TV” subtask.

Overall, the results highlight how pure novelty-seeking can discover complex skills, validating curiosity as a powerful exploration mechanism. Yet, mitigating the “noisy TV” effect remains an open challenge.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: The paper explicitly acknowledges the “noisy TV” failure mode, showing that **pure prediction-error** can be hijacked by random transitions. The authors confirm that in many conventional RL benchmarks, environment designers inadvertently align novelty with extrinsic progression. But in truly **partially random** setups, curiosity can degrade if large parts of the environment remain irreducibly unpredictable.
- **Adaptive Curiosity**: The approach is a prime example of using forward dynamics errors as an intrinsic reward. The large-scale evidence underscores the strengths and weaknesses of such methods in partially random domains. It strongly supports the need to refine curiosity signals that discount uncontrollable or random transitions.
  
Hence, **this paper is relevant** for any research seeking to robustify curiosity-based exploration in partially random RL tasks, providing both large-scale success stories and a cautionary note about uncontrolled stochastic environments.

---

### Worth Citing?

**Yes.** It is one of the most comprehensive studies on **pure intrinsic exploration** across numerous standard RL benchmarks. Key reasons:

1. **Empirical Depth**: The authors test 54 environments, carefully analyzing how curiosity alone can lead to complex behaviors.
2. **Methodological Insights**: They systematically compare different feature embeddings (random vs. learned) for forward-dynamics-based exploration.
3. **Highlighting Limitations**: They present the “noisy TV” problem under an actual 3D environment condition, demonstrating that raw prediction error can fail in the presence of irreducible randomness.

---

### How It May Inform Future Research

1. **Noise-Robust Curiosity**: Future work can address partial environment randomness by factoring out “aleatoric uncertainty,” ensuring curiosity focuses on learnable aspects.  
2. **Scaling and Transfer**: Their results show that large-batch training or “offline” random exploration data can help an agent converge to deeper behaviors. Researchers can further investigate how to leverage massive unlabeled environments for skill pre-training.  
3. **Hybrid Feature Spaces**: Since random features often suffice on many tasks but IDF features generalize better, a dynamic or hybrid approach might capture the best of both worlds.  
4. **Task-Agnostic Pretraining**: Explore systematic ways of combining large unlabeled domain sets with subsequent fine-tuning tasks (multi-level generalization, real robotics).

---

### Open Questions or Possible Critiques

- **Persistent Stochasticity**: The demonstration of slow learning near a “noisy TV” suggests that purely prediction-error-based curiosity can still be fooled by partial environment randomness. Could more advanced methods (e.g., ensembles, Bayesian uncertainty) mitigate this more robustly?
- **Generalization vs. Overfitting**: Random feature embeddings can excel in a given domain but may fail drastically if domain changes (like the “day/night” shift in Mario). How to consistently unify stable random embeddings with domain-adaptive or self-supervised learned features?
- **Long-Horizon Tasks**: Many tested tasks have relatively immediate transitions of interest. For extremely long horizon or multi-stage partial randomness, additional hierarchical or memory-based methods might be needed.
- **Incentive Misalignment**: Some tasks (like “Atlantis” or “IceHockey” in Atari) remain unsolved purely by curiosity. Are there systematic ways to incorporate minimal extrinsic guidance or avoid environment designs that overshadow novelty with irrelevant randomness?
