# Curiosity-Driven Recommendation Strategy for Adaptive Learning via Deep Reinforcement Learning

> **Link**: <https://doi.org/10.48550/arXiv.1910.12577>

> **Parenthetical**: (Han et al., 2019)
> **Narrative**: Han et al. (2019)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Main Objective**  
  > “In this paper, a curiosity-driven recommendation policy is proposed under the reinforcement learning framework, allowing for a both efficient and enjoyable personalized learning mode.”  

- **Adaptive Learning and Recommendation**  
  > “The design of recommendations strategies in the adaptive learning system focuses on utilizing currently available information to provide individual-specific learning instructions for learners.”  

- **Curiosity as Intrinsic Motivation**  
  > “Recognized as a critical impetus behind human behaviors, curiosity is a desire of our nature towards complete knowledge and information-seeking in terms of learning.”

- **Curiosity Reward Model**  
  The authors propose a predictive model \(f(\cdot)\) to forecast the learner’s next knowledge state. The **intrinsic (curiosity) reward** at time \(t\) is the squared error between the predicted next state \(\tilde s(t+1)\) and the observed next state \(\hat s(t+1)\):  
  \[
    R(t) \;=\; \bigl\|\hat s(t+1)\;-\;\tilde s(t+1)\bigr\|^2_2 \quad \text{where} \quad \tilde s(t+1) \;=\; f(\hat s(t), a(t);\, \theta_p).
  \]
  This reward signals how “surprising” the transition is. High error means the recommended learning action leads the learner into less-familiar territory.

- **Actor-Critic Framework**  
  The recommendation policy \(\pi(a\mid s;\theta_\pi)\) is learned via an actor-critic scheme:
  1. **Actor** approximates \(\pi(a \mid \hat s)\) using a feed-forward network with parameters \(\theta_\pi\).  
  2. **Critic** learns a value function \(V^\pi(\hat s;\theta_v)\). The advantage function is:
     \[
       A(\hat s(t),a(t)) \;=\; \bigl[R(t) + V^\pi(\hat s(t+1))\bigr] \;-\; V^\pi(\hat s(t)).
     \]
  Policy gradients are computed by:
  \[
    \nabla_{\theta_\pi} J(\theta_\pi) \;=\; \mathbb{E}_\pi \Bigl[\nabla_{\theta_\pi}\log\pi(a(t)\mid \hat s(t);\theta_\pi)\;A(\hat s(t),a(t))\Bigr].
  \]

- **Assessment Model**  
  The learner’s knowledge state \(\hat s(t)\) is measured by an external assessment model (e.g., item response theory or cognitive diagnosis models) that can be noisy. This assessment updates after each action.

- **Discrete vs. Continuous Knowledge States**  
  1. **Discrete Case**: A small chain of knowledge points (0 or 1 mastery). Transition matrices define the probabilities of mastering the next point.  
  2. **Continuous Cases**: Larger, more realistic space. The authors model knowledge evolution with a parametric function that depends on “learning materials” (actions) and hierarchical prerequisites.  
  3. In all cases, the unknown state transition is simulated but not known to the policy. The curiosity reward is derived purely from the predictive error.

- **Example of the Transition Model**  
  For the continuous environment, they use:
  \[
    s(t+1) \;=\; 1 \;-\; \Bigl(1 - s(t)\Bigr) \;\odot\;\exp\Bigl\{-\,\xi\cdot W_{a(t)}\;\odot\;P\bigl(s(t)\bigr)\Bigr\},
  \]
  where \(\xi \sim \chi^2_2\) is a random variable, \(W_{a(t)}\) is a vector of training weights for each knowledge point, and \(P(\cdot)\) encodes prerequisite constraints.

- **Simulation Studies**
  1. **Discrete**: 4 knowledge points in a strict chain; a small 5-state MDP; they compare the proposed curiosity policy (with DINA-based assessment) vs. a random policy.  
  2. **Continuous Case I**: 10 knowledge points, certain hierarchical constraints, 15 learning materials, and an M3PL IRT assessment.  
  3. **Continuous Case II**: 16 knowledge points, multi-prerequisite structure, 22 learning materials, and a longer horizon.  

  In all settings, the curiosity-driven policy significantly outperforms a random strategy in final knowledge mastery scores.

- **Implementation Details**  
  - They train a separate feed-forward predictor \(\theta_p\) to model \(f\bigl(\hat s(t), a(t)\bigr)\).  
  - The actor/critic networks each have 3 hidden layers, using ReLU activation.  
  - They use asynchronous parallel training (A3C), memory replay, Adam optimizer, and typical RL hyperparameters (batch size = 64, memory capacity = 6000, etc.).

---

### Concise Summary of the Article

Han, Chen, and Tan present a **curiosity-driven recommendation strategy** for personalized (adaptive) learning environments. The algorithm:

1. **Predictive Model**: A neural network \(\tilde s(t+1) = f(\hat s(t), a(t))\) yields the next knowledge state estimate. Its **prediction error** drives an **intrinsic reward**, encouraging the agent to explore unmastered or unpredictable knowledge points.  
2. **Actor-Critic RL**: A policy \(\pi\) is learned via actor-critic, using the curiosity reward to guide exploration. This approach bypasses the need for direct hand-tuned extrinsic rewards at every step.  
3. **Assessment Noise**: Each time the learner takes an action (learning material), a psychometric or IRT model estimates the updated knowledge state \(\hat s(t+1)\). The approach remains robust to moderate assessment noise.  
4. **Experiments**: Across discrete and continuous knowledge spaces with hierarchical prerequisites, the curiosity-driven policy consistently outperforms random selection. Even with large action/state spaces and partial measurement errors, it effectively guides learners to higher final mastery levels.

The method highlights how **intrinsic curiosity** can be leveraged to keep learners engaged and exploring new knowledge effectively, without heavily engineering extrinsic reward signals.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Adaptive Curiosity**: The paper explicitly uses an **intrinsic reward** (prediction error) to drive exploration. This aligns well with curiosity-based RL frameworks where the agent focuses on uncertain or novel transitions.  
- **Handling Randomness**: While the focus is on assessment noise and unknown transitions, the approach can also address partially random dynamics in an educational context—ensuring the agent remains engaged when transitions are unpredictable.  
- **Outcome**: Demonstrates how curiosity-driven strategies can adapt efficiently to large or uncertain state spaces, a key challenge in partially random or partially observable RL tasks.

Hence, this work is **worth citing** for researchers dealing with curiosity-driven or intrinsic exploration in domains that combine human learning or partially random transitions. It offers a practically motivated method that integrates RL with psychological insights on curiosity.

---

### How It May Inform Future Research

1. **Hybrid Reward Structures**: Combining this curiosity-based reward with a final extrinsic reward (e.g., final exam score) might accelerate convergence in more challenging tasks, balancing short-term exploration with ultimate mastery.  
2. **Robustness to Higher Noise**: Future studies could incorporate more complex or time-varying assessment noise, investigating how well curiosity-driven policies adapt in even more stochastic or partially random educational settings.  
3. **Feature Extraction**: Adapting the approach of transforming raw states into a latent or lower-dimensional representation may improve stability when knowledge spaces become extremely large or have high noise.  
4. **Multi-Agent or Group Learning**: Studying curiosity-driven recommendations in group learning tasks where multiple learners share overlapping knowledge points might yield interesting synergy or conflict in recommended material.

---

### Open Questions or Possible Critiques

1. **Over-Exploration Risk**: In purely curiosity-driven settings, the learner may spend excessive time on rarely tested knowledge points, potentially neglecting final mastery goals if no extrinsic signals exist.  
2. **Transition Model Complexity**: The approach heavily relies on the quality of the learned predictive model. In extremely large or partially observed knowledge spaces, efficiently updating \(\theta_p\) might be challenging.  
3. **Scaling to Real-World Education**: The authors simulate up to 16 knowledge points with hierarchical constraints. Real courses might have hundreds of skills or dynamic learner behaviors requiring further scaling strategies (e.g., hierarchical RL).  
4. **Potential Integration with Skilled Knowledge**: If a learner already masters certain knowledge points, the method might quickly yield near-zero curiosity. Mechanisms for refreshing or advanced extension tasks might maintain engagement.

---

### Worth Citing?

**Yes.** The paper demonstrates that curiosity-driven exploration can be successfully integrated into personalized recommendation for adaptive learning. Its reinforcement learning approach—particularly the use of a predictive model for intrinsic reward—directly aligns with core ideas of **curiosity-based RL** and is relevant for any research that combines intrinsic motivation with partially or fully unknown transition dynamics. 
