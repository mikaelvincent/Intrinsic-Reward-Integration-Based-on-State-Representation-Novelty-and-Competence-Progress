# Count-Based Exploration with Neural Density Models

> **Link**: <https://doi.org/10.48550/arXiv.1703.01310>

> **Parenthetical**: (Ostrovski et al., 2017)
> **Narrative**: Ostrovski et al. (2017)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **On Pseudo-Counts and Exploration**  
  > “Bellemare et al. (2016) introduced the notion of a pseudo-count, derived from a density model, to generalize count-based exploration to non tabular reinforcement learning.”

- **Pseudo-Count Definition**  
  For a density model \(\rho\), let \(\rho_n(x)\) be the probability assigned to state \(x\) after training on \(n\) data samples. Then define:
  \[
    \text{PG}_n(x) \;=\; \log \rho_{n+1}(x) \;-\; \log \rho_n(x)
  \]
  (the **prediction gain**). The pseudo-count \(N_n(x)\) for \(x\) is approximated from:
  \[
    N_n(x) \;\approx\; \frac{\rho_n(x)\,\bigl(1 - \rho_{n+1}(x)/\rho_n(x)\bigr)}{\rho_{n+1}(x)/\rho_n(x) - 1}.
  \]
  As in prior work, the agent uses a **bonus**:
  \[
    r^{+}(x) \;=\; \bigl(N_n(x)\bigr)^{-\tfrac12},
  \]
  which behaves like a classic count-based exploration reward.

- **PixelCNN-based Density Model**  
  The authors propose using a *slim* version of PixelCNN (van den Oord et al., 2016), a convolutional model that factorizes image likelihood pixel by pixel:
  > “It consists of a \(7\times7\) masked convolution, followed by two residual blocks (with \(1\times1\) masked convolutions), each with 16 feature planes.”

- **Online Training**  
  The paper emphasizes that to approximate pseudo-counts properly, the density model:
  1. Must be trained in a fully *online* fashion (one gradient update per new sample).  
  2. Should have a decaying step-size for the prediction gain to match the theoretical assumption of \(n^{-1}\) or \(n^{-1/2}\) scaling.  
  3. Must remain “learning-positive,” i.e., probability \(\rho_{n+1}(x)\) generally exceeds \(\rho_n(x)\) for the observed state \(x\).  

  In practice, they relax these constraints for PixelCNN, using a **constant learning rate** plus a decaying multiplier \(c \,n^{-1/2}\) on the prediction gain (PG). Negative PG is thresholded at 0 to avoid destabilizing the bonus.

- **Mixed Monte Carlo Update (MMC)**  
  The authors repeatedly highlight that mixing a Monte Carlo return:
  \[
    Q(x,a) \;\leftarrow\; (1-\alpha)\, Q(x,a) \;+\; \alpha\,\bigl(\text{Monte Carlo return}\bigr),
  \]
  with a standard Q-learning backup is crucial for effective exploration:
  > “One surprising finding is that the mixed Monte Carlo update is a powerful facilitator of exploration in the sparsest of settings, including Montezuma’s Revenge.”

- **Empirical Results**  
  They experiment in Atari 2600:
  - **Hard Exploration Games** like *Montezuma’s Revenge, Private Eye, Venture:* The PixelCNN-based pseudo-count significantly outperforms both baseline DQN and a previous CTS-based approach.  
  - **Easier Games**: PixelCNN’s bonus is less disruptive than CTS’s, often yielding stable or improved learning even when extrinsic rewards are dense.  

  In numerous plots, DQN-PixelCNN (with MMC) surpasses DQN-CTS on most of the 57 Atari games tested.

- **“Maximally Curious” Variant**  
  Increasing the PG scaling by 1–2 orders of magnitude leads to record-breaking scores in some extremely sparse environments, though sometimes it hinders long-term stability (agent keeps exploring at the expense of exploiting stable policies).

- **Curiosity-Only Agent**  
  The paper also tests an agent receiving *only* the PixelCNN exploration bonus (no extrinsic reward). Remarkably, it still learns nontrivial behaviors in games like *Private Eye*, highlighting the inherent exploration power of the pseudo-count approach.

- **Reactor-PixelCNN**  
  They further combine PixelCNN with a multi-step actor-critic method called Reactor, using Retrace(\(\lambda\)) for policy evaluation. This likewise boosts performance, especially in many dense-reward Atari domains. However, in *very* sparse tasks, DQN-PixelCNN with MMC remains stronger due to the direct, large-horizon Monte Carlo backup.

---

### Concise Summary of the Article

Ostrovski et al. build on prior work (Bellemare et al. 2016) that introduced the concept of **pseudo-counts** for exploration. Their main contribution is to replace the earlier context-tree-switching (CTS) density model with a **PixelCNN**-based model, which more effectively captures pixel-level dependencies in Atari frames. They address practical training constraints (e.g., constant learning rates, fully online updates) and demonstrate that **PixelCNN pseudo-counts** provide a robust **intrinsic reward** for exploration:

1. **Implementation**:  
   - A slim PixelCNN architecture is trained online.  
   - A “prediction gain” is derived for each state, scaled by a decaying factor to form pseudo-counts.  
   - The exploration bonus is combined with the environment’s extrinsic reward.

2. **Results**:  
   - On *hard exploration games* with sparse rewards (like Montezuma’s Revenge), the PixelCNN-based exploration bonus, together with a **mixed Monte Carlo** approach for Q-learning, achieves state-of-the-art or near state-of-the-art results.  
   - PixelCNN yields more stable or beneficial bonuses on easier games compared to previous approaches.

3. **Significance of Monte Carlo Mix**:  
   - The authors show that mixing Monte Carlo returns can be crucial to rapidly propagating intrinsic reward signals.  
   - Simply providing a strong exploration bonus is insufficient if the agent’s learning method cannot effectively leverage sparse and transient intrinsic rewards.

4. **Further Extensions**:  
   - Adopting the bonus in a multi-step actor-critic (Reactor) agent also sees widespread performance gains, though not as dramatically on extremely sparse tasks.  
   - A purely curiosity-driven agent, ignoring extrinsic reward, can still achieve substantial scores in certain complex Atari games.

Overall, the paper demonstrates that **PixelCNN-based pseudo-counts** can reliably guide exploration in challenging high-dimensional environments.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness and Exploration**  
  While this paper focuses on sparse reward Atari games, the authors highlight how the **PixelCNN model** dynamically adapts to states, continuing to assign mild “surprise” to less-frequent transitions. This approach naturally avoids indefinite high bonuses for purely random states, provided the network converges to an accurate predictive distribution.  
  In partially random environments, a well-trained model should reduce curiosity rewards in truly unlearnable transitions, so the agent is not trapped by noise.

- **Adaptive Curiosity**  
  PixelCNN’s “learning-positive” property (the distribution is continually updated online) and the use of a **transient** intrinsic reward aligns with the concept of *adaptive curiosity*. The agent is intrinsically motivated to explore novel states, while quickly lowering bonuses for states it has modeled well (including random transitions once recognized as noise).

Hence, the article’s approach is *highly relevant* to the theme of robust, scalable, curiosity-driven exploration that can handle partially random or high-dimensional tasks.

---

### Worth Citing?

**Yes.** This paper is a major milestone in leveraging advanced neural density models for exploration bonuses and demonstrates significant empirical success. It shows how carefully chosen density models and multi-step RL updates can tackle notoriously sparse exploration challenges. Researchers studying or developing *adaptive curiosity in partially random RL* will find strong methodological insights, especially about:

- Online training of generative models in RL loops.  
- Balancing a persistent curiosity signal with step-size decays or scale parameters.  
- Coupling curiosity with multi-step or Monte Carlo backups for faster reward propagation.

---

### How It May Inform Future Research

1. **Partial Randomness / Stochastic Observations**  
   Future work can adapt PixelCNN-based bonuses to environments where certain transitions are purely stochastic (e.g., partial random noise). One might examine how to distinguish ephemeral randomness from learnable structure—possibly augmenting PixelCNN with aleatoric uncertainty estimations.

2. **Continuous or 3D Domains**  
   The authors concentrate on discrete 2D Atari frames. Researchers can generalize PixelCNN-based pseudo-counts to continuous or 3D image inputs by exploring 3D CNN architectures or other generative models.

3. **Hybrid or Hierarchical Curiosity**  
   Merging PixelCNN-based pseudo-counts with other exploration signals (e.g., ensemble disagreement, transition prediction error, latent forward models) might yield even more robust methods.  
   The concept of mixing returns (Monte Carlo + Q-learning) suggests synergy with hierarchical RL or skill-discovery frameworks, especially in partially random tasks.

4. **Local vs. Global Novelty**  
   PixelCNN focuses on per-frame modeling. Additional mechanisms might track larger-scale novelty beyond immediate frames, further aiding exploration in extended or multi-room tasks with partially random elements.

---

### Open Questions or Possible Critiques

- **Overestimation in Very Stochastic Domains**  
  If environment transitions are highly noisy and PixelCNN partially “gives up” on modeling them, the predicted probability might remain low, producing a persistent reward for random states. More explicit “aleatoric noise” modeling or advanced scheduling of PG might be needed.

- **Stable Online Training**  
  Maintaining a stable, fully online training procedure for high-capacity generative models can be tricky in domains with abrupt shifts in state distribution. The authors demonstrate success but do not fully detail how to handle extremes of catastrophic forgetting or persistent distribution drift.

- **Compute Overhead**  
  Training PixelCNN for each state can be expensive in heavier tasks. Although the authors propose a lightweight architecture, real-world or 3D environments may strain computational resources.

- **Reliance on Monte Carlo**  
  The paper repeatedly shows that the mixed Monte Carlo update is crucial, especially for extremely sparse rewards. More sophisticated multi-step methods (like Retrace with large \(\lambda\)) or flexible on/off-policy mixing might replicate or improve upon these benefits, but the ideal approach is not exhaustively studied.
