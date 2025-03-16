# Unified curiosity-Driven learning with smoothed intrinsic reward estimation

> **Authors**: Fuxian Huang, Weichao Li, Jiabao Cui, Yongjian Fu, Xi Li
> **Date**: March 2022
> **Link**: <https://doi.org/10.1016/j.patcog.2021.108352>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

1. **Motivation & Problem Statement**

   - *Sparse or Absent Rewards*  
     > “In reinforcement learning (RL), the intrinsic reward estimation is necessary for policy learning when the extrinsic reward is sparse or absent.”

   - *Partial State/Action Novelty Limitations*  
     > “Although these two methods (state novelty and state-action novelty) can alleviate the sparse extrinsic reward problem, there are still four limitations: 1) only utilizing partial information of the transition [...] 2) ignoring the learned policy [...] 3) ignoring the state distribution [...] 4) high variance of estimated intrinsic reward.”

   - *Goal:*  
     > “We further propose state distribution-aware weighting method and policy-aware weighting method to dynamically unify two mainstream intrinsic reward estimation methods. In this way, the agent can explore the environment more effectively and efficiently.”

2. **Unified Intrinsic Reward**  
   The article unifies:
   - **State Novelty Estimation**: e.g. RND-like approach.
   - **State-Action Novelty Estimation**: e.g. ICM-like approach.

   Let the transition be \((s_t, a_t, s_{t+1})\). They define:
   \[
     r^C_t = g(s_{t+1}; \theta_C), \quad ( \text{intrinsic reward for next state} )
   \]
   \[
     r^N_t = g(s_t; \theta_N), \quad ( \text{intrinsic reward for current state} )
   \]
   \[
     r^F_t = f(s_t, a_t, s_{t+1}; \theta_F), \quad ( \text{forward-model path novelty} )
   \]
   The **unified** intrinsic reward is:
   \[
     r^{\mathrm{int}}_t \;=\; \eta_t \, r^C_t \;+\; \eta_{t+1}\,r^N_t \;+\; \beta_t\,r^F_t.
   \tag{11}
   \]

3. **Adaptive Weights**  
   They propose two weighting schemes:
   
   - **Distribution-Aware Weighting (DAW)**:  
     > “We define the cluster sizes in the state space and assign larger weights for transitions in underrepresented clusters.”
     \[
       \eta_t = 1 - \frac{n_i - 1}{\sum_{i=1}^{K} n_i}, 
       \quad \text{if $s_t$ is in cluster $i$ with $n_i$ states.}
     \tag{12}
     \]
     Clusters with fewer states (rare states) get a higher weight.

   - **Policy-Aware Weighting (PAW)**:  
     > “We propose to utilize the entropy of the action distribution to dynamically adjust the weight of exploration bonus.”
     If the policy’s output distribution over actions is \(A=[p_1,\dots,p_Z]\), then
     \[
       \beta_t = -\sum_{i=1}^Z p_i \ln(p_i).
     \tag{13}
     \]

4. **Smoothed Intrinsic Reward**  
   - *Neighbor-based Smoothing*:  
     They define a small \(\delta\)-neighborhood \(B_\delta(s_t)\) to gather similar states, retrieve transitions in memory \(E\), and compute a weighted average:
     \[
       r^N_t \;=\;\sum_{j=1}^D w_j \,r_{t,j}, 
       \quad
       w_j \;=\;\frac{\exp(-d(s_{t,j},s_t))}{\sum_{j=1}^D \exp(-d(s_{t,j},s_t))}.
     \tag{15,16}
     \]
     Similar smoothing applies to \(r^C_t\) and \(r^F_t\). 
     Thus the final (unified + smoothed) intrinsic reward is:
     \[
       r^{\mathrm{int}}_t = \beta_t\,r^F_t \;+\;\eta_t\,r^C_t \;+\;\eta_{t+1}\,r^N_t.
     \tag{17}
     \]

5. **Attention Module**  
   - *Random CNN Features + Learned Attention*:  
     > “We find the feature map can be more representative if the random feature is selected by an attention module.”
     The final embedding for a state is \(\tilde{H} = H \odot M\), where \(H\) is the random CNN feature map, and \(M\) is the learned attention mask.

6. **Implementation with PPO**  
   - They incorporate the unified, smoothed intrinsic reward \(r^{\mathrm{int}}_t\) plus extrinsic reward \(r^{\mathrm{ext}}_t\) to train a policy with Proximal Policy Optimization. Algorithm 1 outlines the steps.

7. **Experiments & Key Findings**  
   - **Benchmarks**: Atari 2600 with two scenarios:
     1. *No extrinsic reward* (12 games: Breakout, Pong, RoadRunner, etc.).  
     2. *Sparse extrinsic reward* (Gravitar, MontezumaRevenge, Freeway, Pitfall).
   - **Comparisons**: ICM, RND, Count-based, Novelty Search GA/ES.
   - **Results**:
     > “We find that our approach converges much faster and achieves higher game scores. [...] On Montezuma’s Revenge and Gravitar, we outperform baselines by a large margin.”
   - **Ablation**:
     - Removing the attention or smoothing or the distribution/policy weighting each degrades performance.
     - The weighting for state-novelty or path-novelty tends to be higher in early training, then decreases as exploration saturates.

8. **Complexity Discussion**  
   - Additional overhead: ~67% for unifying module, ~4% for attention, ~linear overhead for smoothing. Overall ~11% more training time than ICM.  
   - Still more efficient than RND or novelty-search methods in total runtime.

9. **Conclusions & Future Work**  
   > “In practice, our method may suffer from unstable learning on some games, because it involves a lot of learning about these three different modules. In future, we will explore more approaches to improve the stability by effectively fusing different modules to reduce the learning burden.”

---

## Concise Summary of the Article

Huang *et al.* tackle **sparse-reward reinforcement learning** by proposing **UCLSE** (Unified Curiosity-Driven Learning with Smoothed Intrinsic Reward Estimation). Their key insight is to **combine** both *state novelty* (like RND) and *state-action novelty* (like ICM) into a single exploration bonus that uses two adaptive weighting techniques:

1. **Distribution-Aware Weighting (DAW):** Increases the state-novelty component for underexplored clusters in the state space.
2. **Policy-Aware Weighting (PAW):** Increases the path-novelty component if the current policy has high entropy on the chosen action (i.e., the policy is uncertain).

They further **smooth** the intrinsic rewards by averaging over a small set of neighboring transitions, reducing variance and stabilizing the agent’s training. An **attention module** focuses on task-relevant features derived from random CNN embeddings, making the novelty estimation more robust.

Experimental results on multiple Atari games, in both zero-extrinsic and sparse-extrinsic setups, show that UCLSE outperforms previous curiosity-driven methods (ICM, RND, count-based, novelty search) in terms of sample efficiency, stability, and final scores—particularly on hard-exploration games like **Montezuma’s Revenge** and **Gravitar**. The authors highlight that dynamic weighting (DAW + PAW) and reward smoothing mitigate the pitfalls of partial or inconsistent novelty estimates in large state spaces.

---

## Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness Handling**: By smoothing intrinsic rewards and adaptively weighting both state and path novelty, UCLSE aims to reduce high variance in the bonus due to unbalanced or random transitions. This approach can help avoid the “noisy TV” trap or random-state loops by discounting irrelevant or oversampled states.
- **Unified Curiosity**: The paper explicitly unifies different novelty signals (like RND and ICM) under a single framework, addressing one of the known issues in partially random settings: ignoring either state novelty or path novelty alone may hamper exploration.
- **Worth Citing?**  
  **Yes**. UCLSE introduces a *comprehensive, robust, and adaptive* approach to intrinsic rewards that effectively improves exploration under sparse or missing extrinsic rewards. It may be particularly relevant for partially random or large-scale RL tasks that need stable, multi-faceted novelty signals.

---

## How It May Inform Future Research

1. **Expanded Smoothing or Batching**: The neighbor-based smoothing approach could be extended to multi-step transitions or hierarchical state-grouping to handle dynamic or partially random domains more effectively.
2. **Adaptive Clustering**: The authors rely on SimHash for cluster formation. Future work might refine or auto-tune the hashing and cluster thresholds, especially under heavier environment noise.
3. **Combining Unification with Other Curiosity Signals**: Researchers might explore synergy between this unified method and uncertainty-based signals (like ensemble disagreement) to handle partially random transitions more reliably.
4. **Stability & Scalability**: The authors mention potential instability due to multiple learning modules. Future directions could investigate novel ways to fuse or coordinate these modules, focusing on stable multi-objective optimization in large or continuous tasks.

---

## Open Questions or Possible Critiques

1. **Stability of Multiple Modules**: The authors acknowledge that combining state novelty, path novelty, weighting factors, smoothing, and attention can introduce complexity. How best to tune or unify these submodules remains an open question.
2. **True Randomness**: The paper shows strong results on standard Atari. Additional tests in domains with explicit, unlearnable stochastic transitions (e.g. heavily randomized labyrinths) could further validate how effectively the approach discounts noise or meaningless transitions.
3. **Choice of Distance and Hashing**: The smoothing relies on a distance metric (in feature space) plus SimHash-based clustering. Are these expansions robust to large domain shifts or realistic 3D tasks?
4. **Overhead in Real-World Settings**: While overhead is ~11% in Atari, the method’s performance and resource demands in more complex robotics or partially observed 3D domains require further study.
