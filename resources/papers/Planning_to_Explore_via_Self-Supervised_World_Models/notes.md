# Planning to Explore via Self-Supervised World Models

> **Link**: <https://doi.org/10.48550/arXiv.2005.05960>

> **Parenthetical**: (Sekar et al., 2020)
> **Narrative**: Sekar et al. (2020)

---

## Notes

### Selected Direct Quotes and Formulas

- **Motivation**  
  > “We present Plan2Explore, a self-supervised reinforcement learning agent that tackles both [task generality and sample efficiency] through a new approach to self-supervised exploration and fast adaptation to new tasks, which need not be known during exploration.”  

- **Retrospective vs. Expected Novelty**  
  > “Instead of maximizing intrinsic rewards in retrospect, we learn a world model to plan ahead and seek out the expected novelty of future situations.”  

- **Latent World Model**  
  The authors build on a recurrent latent dynamics model (RSSM) where images are encoded into feature vectors \(h_t\), which form part of a hidden state \(s_t\). The agent then predicts future states and decodes them back into images and/or rewards:
  \[
  h_t = e_\theta(o_t), \quad
  q_\theta(s_t \mid s_{t-1}, a_{t-1}, h_t), \quad
  p_\theta(s_t \mid s_{t-1}, a_{t-1}), \quad
  p_\theta(o_t \mid s_t), \quad
  p_\theta(r_t \mid s_t).
  \]
  This model is trained jointly via a variational lower bound, akin to a VAE.

- **Ensemble Disagreement as Intrinsic Reward**  
  To implement **latent disagreement**, the authors train an ensemble of one-step predictive models \( q(h_{t+1} \mid w_k, s_t, a_t) \) for \( k \in \{1,\dots,K\}\). Each model in the ensemble predicts the next latent embedding \(h_{t+1}\). The **intrinsic reward** at time \(t\) is:
  \[
  r_t^i \;=\; D(s_t, a_t) \;=\; \text{Var}_{k}[\,w_k(s_t, a_t)\,],
  \]
  i.e., the variance (disagreement) across the ensemble’s predicted means.

- **Information Gain Interpretation**  
  The paper connects disagreement-based exploration to expected information gain:
  \[
  I(h_{t+1}; w \,\mid\, s_t, a_t) 
  = H(h_{t+1}\,\mid\,s_t,a_t) \;-\; H(h_{t+1}\,\mid\,w,s_t,a_t),
  \]
  where the second term is seen as aleatoric uncertainty that does not reduce with more data. Maximizing the ensemble’s disagreement approximates maximizing the above information gain.

- **Zero-Shot and Few-Shot Adaptation**  
  After collecting exploration data without any extrinsic reward, Plan2Explore trains a policy on the learned world model by imagining rollouts for a newly provided task reward function. The method supports:
  1. **Zero-Shot**: Directly train a task policy in latent space using only the self-supervised model.  
  2. **Few-Shot**: Optionally gather a small amount of task-specific data (100–150 episodes) to refine or “distill” the reward predictor and world model.

- **Key Empirical Findings**  
  1. **State-of-the-art Zero-Shot**: Plan2Explore outperforms other unsupervised exploration methods (Curiosity, MAX) on DM Control tasks from high-dimensional pixel inputs.  
  2. **Near Oracle**: On many tasks, Plan2Explore’s zero-shot performance rivals Dreamer, which sees full reward signals during training.  
  3. **Task Generality**: A single self-supervised world model adapts to multiple tasks (e.g., run forward, run backward, flipping) in a zero or few-shot setting—unlike a reward-specific model that fails to generalize.  
  4. **Expected Novelty vs. Retrospective**: Planning using the expected future disagreement achieves higher exploration efficiency than retrospective novelty estimation.

---

### Concise Summary of the Article

The paper introduces **Plan2Explore**, a self-supervised RL technique that learns a latent world model and uses **planning** to explore states that promise high future novelty. Its core innovation is *latent disagreement*: an ensemble of one-step predictors that provides an *intrinsic reward* based on the variance of next-state predictions, approximating the *expected information gain*. Crucially, Plan2Explore uses an RSSM-based model to plan in a compact latent space, enabling:
- **Task-agnostic Exploration**: The agent collects data guided by model disagreement, without any extrinsic reward.  
- **Task Adaptation**: Upon receiving a new reward function for a task, the agent plans within its learned model to solve the task in zero or few additional environment interactions.  

Experiments on the DeepMind Control Suite (pixel-based continuous control) show that Plan2Explore outperforms other unsupervised approaches and competes with fully supervised RL methods (like Dreamer). It also generalizes well to multiple new tasks in the same environment—unlike a single-task agent that struggles beyond its training objective.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Adaptive Curiosity and Disentangling Noise**: Though the paper does not focus explicitly on partial randomness, its approach to measuring *epistemic* uncertainty in a latent space can help avoid purely stochastic transitions that do not reduce uncertainty. By focusing on ensemble disagreement rather than raw prediction error, Plan2Explore addresses aspects of random environment transitions.  
- **Efficient Self-Supervised Exploration**: The concept of planning for *expected* novelty (rather than retrospective) is highly relevant for adaptive curiosity. Plan2Explore’s method can inform strategies to robustly handle uncertain or partially random dynamics.  

Yes, citing this work would be beneficial. It extends model-based curiosity to high-dimensional observations and demonstrates generalizable exploration that could be transferred or adapted to partially random RL tasks.

---

### How It May Inform Future Research

1. **Ensemble-Based Bayesian Methods**: Expanding ensemble disagreement to better model both aleatoric and epistemic uncertainties might further refine exploration signals, especially when randomness is partial and structured.  
2. **Integrating with Other Curiosity Approaches**: Plan2Explore’s approach can be combined with methods that explicitly model or detect “stochastic transitions,” potentially improving performance in highly noisy environments.  
3. **Scaling to Real-World Robotics**: The zero-shot/few-shot paradigm is promising for real-world deployments where collecting large, reward-labeled data is difficult, but broad unsupervised interactions are feasible.  
4. **Hybrid Exploration Objectives**: Merging planning-based novelty with other forms of intrinsic motivation (e.g., skill discovery, state coverage) might further boost adaptability under partial randomness or complex tasks.

---

### Open Questions or Critiques

- **Handling Heteroscedastic Noise**  
  The ensemble-based approach estimates disagreement over mean predictions but uses a fixed variance assumption. In environments with complex or state-dependent noise, the system may still overestimate or underestimate the inherent stochasticity.
- **Long-Horizon Planning**  
  While the paper shows advanced lookahead in latent space, tasks with intricate partial observability or extended multi-step dependencies might require additional memory architectures or hierarchical planning.
- **Performance in Highly Stochastic Domains**  
  The experiments focus on DM Control Suite, which has limited random transitions. Additional evaluations on more chaotic or partially random environments could illuminate the method’s robustness to noise.
- **Computational Complexity**  
  Maintaining an ensemble and training policies in imagination can be demanding; further analysis on how Plan2Explore scales to extremely high-dimensional or real-time tasks would be valuable.
