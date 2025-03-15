# #Exploration: A Study of Count-Based Exploration for Deep Reinforcement Learning

> **Authors**: Haoran Tang, Rein Houthooft, Davis Foote, Adam Stooke, Xi Chen, Yan Duan, John Schulman, Filip De Turck, Pieter Abbeel
> **Date**: 5 December 2017
> **Link**: <https://doi.org/10.48550/arXiv.1611.04717>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

- **Key Motivation**  
  > “Count-based exploration algorithms are known to perform near-optimally when used in conjunction with tabular reinforcement learning (RL) methods [...] It is generally thought that count-based methods cannot be applied in high-dimensional state spaces, since most states will only occur once.”

- **Core Contribution**  
  > “We describe a surprising finding: a simple generalization of the classic count-based approach can reach near state-of-the-art performance on various high dimensional and/or continuous deep RL benchmarks. [...] States are mapped to hash codes, which allows to count their occurrences with a hash table.”

- **Hash-Based State Counting**  
  The authors discretize states with a hash function \(\phi: S \to \mathcal{Z}\), then define a bonus reward:
  \[
    r^{+}(s) \;=\; \frac{\beta}{\sqrt{n(\phi(s))}},
  \]
  where \(n(\phi(s))\) is the visitation count for the hashed code \(\phi(s)\), and \(\beta\) is a hyperparameter.

- **SimHash**  
  A popular Locality-Sensitive Hashing (LSH) approach used in the paper:
  \[
    \phi(s) = \operatorname{sgn}\bigl(A\,g(s)\bigr)\in \{-1,+1\}^k,
  \]
  with \(A\in \mathbb{R}^{k\times D}\) drawn from \(\mathcal{N}(0,1)\) and \(g\) an (optional) state preprocessor. Larger \(k\) yields finer granularity; smaller \(k\) merges more states.

- **Learned Hash (Autoencoder Approach)**  
  Instead of using raw SimHash on pixels, the paper also proposes training an autoencoder with a special dense layer of sigmoids. By rounding activations \(\lfloor b(s)\rfloor\) to \(\{0,1\}^D\), one obtains a binary code. Noise injection in that bottleneck layer forces it to learn more separable latent features. Then they randomly project the code again via SimHash to produce the final hash for counting.

- **Selected Empirical Findings**  
  1. **Continuous Control (rllab)**:
     - Tasks with sparse rewards like *MountainCar*, *CartPoleSwingup*, *SwimmerGather*, *HalfCheetah*. 
     - A simple hash-based exploration bonus (“SimHash+TRPO”) yields strong improvements over vanilla TRPO and performs comparably or better than VIME in some tasks.
  2. **Atari 2600**:
     - Games tested: *Freeway*, *Frostbite*, *Gravitar*, *Montezuma’s Revenge*, *Solaris*, *Venture*.
     - Even a straightforward pixel-based SimHash bonus often significantly outperforms baseline TRPO.  
     - Using *BASS* (a domain-informed static image preprocessor) or a learned autoencoder hash can further improve results on challenging tasks like *Montezuma’s Revenge* and *Venture*.

- **Bloom Filters / Count-Min Sketch**  
  To manage the large hash table, they use counting Bloom filters (or Count-Min Sketch) for efficient state-count bookkeeping. The probability of collisions can be made low with multiple prime-modulus hash functions.

- **Importance of Hash Granularity**  
  They highlight a crucial trade-off:  
  > “Having appropriate granularity and encoding information relevant to solving the MDP is key for good performance.”

- **Comparison with Pseudocounts**  
  The authors relate their approach to pseudo-count methods (e.g., Bellemare et al.) but note that in their method:  
  > “A density model has to be designed and learned to achieve good generalization for pseudo-count, whereas in our case generalization is obtained by a wide range of simple hash functions.”

- **Notable Performance Outcomes**  
  - On *Frostbite*, TRPO + pixel-based SimHash outperforms many advanced baselines, achieving scores well above 4000 after 50 million timesteps.  
  - On *Freeway*, *Gravitar*, and *Solaris*, both learned autoencoder hashing (AE-SimHash) and BASS-based hashing surpass the baseline significantly.  
  - For *Montezuma’s Revenge*, they show gains over the baseline, although not matching specialized exploration algorithms like pseudo-count-based or off-policy DQN variants.  
  - The method consistently excels whenever exploration is critical, showcasing how an “approximate count” can drive the agent to discover sparse rewards.

### Concise Summary of the Article

Tang et al. revisit **count-based exploration** in Reinforcement Learning (RL) and show that, despite conventional wisdom, classical counting methods can scale to large or continuous state spaces if the agent **hashes** states appropriately. The algorithm:

1. **Hashing**: A function \(\phi\) maps states to discrete “bins.”  
2. **State Counts**: Maintain a visitation count \(n(\phi(s))\).  
3. **Bonus Reward**: Provide the agent with an intrinsic bonus \(\beta / \sqrt{n(\phi(s))}\).  
4. **Integration into Deep RL**: Combine with TRPO (or other RL algorithms) to encourage systematic exploration of rarely visited states.

The paper explores two main hashing strategies:
- **SimHash** on raw pixels (or RAM) to group similar states.
- **Learned** hashing via an autoencoder-based latent binary code, then further random projection.

Empirical evaluations on challenging continuous-control tasks (rllab) and Atari 2600 games demonstrate:
- Strong improvements over baseline TRPO with naive noise-based exploration.
- Results competitive or superior to some advanced exploration algorithms (e.g., VIME, certain DQN variants).
- The approach is relatively straightforward to implement, computationally efficient (especially using count-min sketches), and flexible in how states are hashed.

### Relevance to "Adaptive Curiosity for Exploration in Partially Random RL Environments"

- **Partial Randomness**: The hash-based method treats states that map to the same hash code as “similar.” If transitions are highly noisy or contain partially random elements, collisions and repeated counting will eventually drive the exploration bonus toward zero for fundamentally unlearnable states. The method does not inherently keep chasing random transitions—once a hashed bin is “filled,” the agent’s curiosity decreases.  
- **Adaptive Curiosity**: The count-based bonus approximates “novelty.” Combined with a suitable hash function, the agent is nudged toward less-visited areas while ignoring states that have been thoroughly explored (even if they are stochastically noisy). Thus, it aligns well with the idea of focusing on learnable novelty rather than random noise.  
- **Practical Implementation**: This approach is simpler than many complex intrinsic-motivation or forward-model-based algorithms, which can be beneficial in partially random environments where a robust, easy-to-tune baseline is valuable.

**Worth Citing?** Absolutely. This work is highly relevant for explorative RL in large or high-dimensional environments. The authors show that even a minimalist extension of classical counting via hashing can produce competitive exploration performance—offering a clear reference point for curiosity-driven or count-based methods.

### How It May Inform Future Research

1. **Advanced Hash Functions**: Future studies can explore more sophisticated or domain-adaptive hashing strategies to capture environment-specific structure—particularly relevant if partial randomness requires carefully distinguishing subregions of state space.  
2. **Combine with Other Intrinsic Rewards**: Methods like Random Network Distillation or ensemble disagreement might be fused with hash-based counting to handle diverse exploration challenges (noisy transitions, partial observability, hierarchical tasks).  
3. **Adaptive Granularity**: Dynamically adjusting the granularity of the hash based on learning progress or region density could refine which states are considered “novel.”  
4. **Real-World Robotics**: Hash-based counting might offer a simpler alternative to learned density models or complex forward dynamics in partially random real-world scenarios (camera noise, sensor drift).

### Open Questions or Critiques

- **Optimal Hashing**  
  Determining the perfect hash granularity remains partly ad hoc, requiring hyperparameter tuning. Automated or self-adaptive hashing is an open challenge.  
- **Noisy Observations**  
  If observations are extremely high-dimensional and heavily stochastic, robust hashing might need domain knowledge or advanced representation learning.  
- **Long-Horizon Exploration**  
  The approach still depends on propagating the bonus through standard RL rollouts. Methods for faster credit assignment in tasks requiring multi-step planning could further improve exploration in very large or partially random MDPs.  
- **Off-Policy Data**  
  The authors note that TRPO does not reuse off-policy data, whereas many count-based or pseudo-count methods can thrive with replay buffers. Incorporating a hash-based bonus in an off-policy algorithm (like DQN variants) might yield further gains.
