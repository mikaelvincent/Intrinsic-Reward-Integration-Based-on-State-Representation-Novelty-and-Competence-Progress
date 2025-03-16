# Unifying Count-Based Exploration and Intrinsic Motivation

> **Authors**: Marc G. Bellemare, Sriram Srinivasan, Georg Ostrovski, Tom Schaul, David Saxton, Remi Munos
> **Date**: 7 Nov 2016
> **Link**: <https://doi.org/10.48550/arXiv.1606.01868>

---

## Notes

### Selected Direct Quotes, Formulas, and Data

- **Core Focus**  
  > “We consider an agent’s uncertainty about its environment and the problem of generalizing this uncertainty across states. Specifically, we focus on the problem of exploration in non-tabular reinforcement learning. Drawing inspiration from the intrinsic motivation literature, we use density models to measure uncertainty, and propose a novel algorithm for deriving a pseudo-count from an arbitrary density model.”

- **Count-Based Exploration in Tabular MDPs**  
  - Visit counts \(N(x, a)\) guide exploration via a bonus term \(\propto \bigl(N(x, a)\bigr)^{-1/2}\).  
  - However, in large or continuous domains, states seldom repeat, so direct counts are rarely useful.

- **Intrinsic Motivation**  
  - “Explore what surprises you”: a reward bonus for novelty or unexpected events.  
  - Typically uses *prediction error* or *learning progress* (e.g., changes in compression or forward-model error).  
  - The authors unify these ideas with count-based bonuses by proposing **pseudo-counts** derived from density models.

#### Defining Pseudo-Counts
1. **Recoding Probability**  
   - Let a density model \(\rho\) map histories \(x_{1:n}\) to a probability \(\rho_n(x)\).  
   - The *recoding probability* \(\rho_n^+(x)\) is the probability after the next occurrence of \(x\):
     \[
       \rho_n^+(x) := \rho\bigl(x; x_{1:n}\,x\bigr).
     \]

2. **Pseudo-Count System**  
   The authors define two unknowns: a function \(N_n(x)\) and a “pseudo-count total” \(n\), satisfying:
   \[
     \rho_n(x) = \frac{N_n(x)}{n}, 
     \quad
     \rho_n^+(x) = \frac{N_n(x)+1}{n+1}.
   \]
   Solving yields:
   \[
     N_n(x) = \frac{\rho_n(x)\,\bigl(1-\rho_n^+(x)\bigr)}{\rho_n^+(x) - \rho_n(x)}, 
     \quad
     n = \frac{\rho_n(x)}{\rho_n^+(x)-\rho_n(x)}.
   \]
   - If the density model is *learning-positive* (probabilities increase when a state recurs), \(N_n(x)\ge 0\).

3. **Exploration Bonus**  
   - They adapt the MBIE-EB approach (Strehl & Littman) using \(\bigl(N_n(x)\bigr)^{-1/2}\).  
   - This yields an intrinsic reward akin to count-based bonuses but generalizes to non-tabular settings.

#### Relation to Intrinsic Motivation

- **Information Gain** (\(\mathrm{IG}\)): Kullback-Leibler difference between prior/posterior after seeing \(x\).
- **Prediction Gain** (\(\mathrm{PG}\)): difference in negative log probabilities (\(\log \rho_n\) vs. \(\log \rho_n^+\)).
  \[
    \mathrm{PG}_n(x) \;=\; \log \rho_n(x) \;-\; \log \rho_n^+(x).
  \]
- **Key Theorem**  
  1. \(\mathrm{IG}_n(x) \;\le\; \mathrm{PG}_n(x)\).  
  2. \(\mathrm{PG}_n(x)\;\le\; N_n(x)-1\).  
  \[
    \mathrm{IG}_n(x) \;\le\; \mathrm{PG}_n(x)\;\le\; N_n(x)-1.
  \]
  Thus **pseudo-count** \(\sim\) exponent of “prediction gain,” bridging tabular counts and intrinsic motivation methods.  
  > “Maximizing immediate information (or prediction) gain is insufficient for near-optimal exploration; pseudo-count-based bonuses remain more powerful.”

#### Empirical Evaluation

1. **Pseudo-Counts in Atari**  
   - They use a **CTS** (Context-Tree Switching) density model over downsampled 42×42 grayscale frames.  
   - Pseudo-counts approximate how “familiar” the model is with a new state (frame).  
   - Intrinsic bonus \( \propto \bigl(N_n(x)+0.01\bigr)^{-1/2}\).  

2. **Atari “Hard Exploration” Games**  
   - \(\text{DQN}+\text{PseudoCount}\) dramatically improves exploration in MONTEZUMA’S REVENGE, VENTURE, etc.  
   - Reaches 15 rooms in Montezuma’s Revenge vs. only 2 rooms for standard DQN.  
   > “Within 50 million frames our agent learns a policy which consistently navigates through 15 rooms and achieves scores significantly higher than previously published agents.”

3. **Actor-Critic** (A3C) with Pseudo-Count Bonus  
   - Called A3C+. Applied to all 60 Atari games.  
   - Achieves better median performance vs. vanilla A3C, especially on the “hard” or “sparse reward” titles.

4. **Comparisons of Different Bonuses**  
   - They compare: no bonus, \(N(x)^{-1/2}\), \(N(x)^{-1}\), and **prediction-gain**-based.  
   - \(\bigl(N_n(x)\bigr)^{-1/2}\) emerges best in the long run; pure prediction-gain often saturates and explores less effectively.

### Key Theoretical and Practical Contributions

- **Pseudo-count**: A unified measure bridging tabular count-based exploration and generic density-model-based novelty.  
- **Proof**: They connect pseudo-count to information gain, plus show a mismatch if only “immediate” prediction gain is used.  
- **Density Models**: They adopt a basic CTS model to demonstrate feasibility; advanced generative models might yield richer pseudo-counts.  
- **Empirical Gains**: Large improvements in famously difficult Atari tasks (esp. Montezuma’s Revenge).

---

## Summary of the Article

Bellemare *et al.* propose **pseudo-counts** as a means to generalize classical count-based exploration algorithms (e.g., MBIE-EB) to high-dimensional or non-tabular RL domains. Drawing on **intrinsic motivation**, they interpret “novelty” in terms of a density model’s evolving probability for newly encountered states:

1. **Pseudo-Count Definition**  
   A next-state probability \(\rho_n^+(x)\) is compared to the pre-update probability \(\rho_n(x)\). A single “fictitious count” increment emerges from the ratio. This constructs a “visit count” that can be used in exploration bonuses.

2. **Link to Information/Prediction Gain**  
   They prove that the new *prediction gain* arises from changes in the model’s assigned probability. A small difference implies the model is confident (like having many visits), while a large difference implies novelty. They show how pseudo-counts align with “intrinsic motivation” methods based on learning progress or information gain, yet remain more powerful in guaranteeing near-optimal exploration.

3. **Experiments**  
   On Atari 2600, using a CTS-based pixel-density model, they transform pseudo-counts into an exploration bonus \(\bigl(N_n(x)+\alpha\bigr)^{-1/2}\). This approach outperforms baselines in several challenging “sparse reward” games, notably **Montezuma’s Revenge**, where it explores many rooms and achieves higher scores than prior RL methods.

4. **Conclusions**  
   Pseudo-counts unify a theoretically grounded extension of count-based exploration, bridging forward-model-based curiosity and Bayesian bonuses. The authors highlight future directions: improving state embeddings, deeper synergy with function approximators, and bridging continuous-state forms of count-based exploration.

---

## Relevance to “Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments”

- **Partially Random Domains**: By relying on a density model (rather than repeated exact states), the pseudo-count approach can discount purely random states if the model quickly adapts. This helps avoid the “noisy TV” trap—once the model identifies stochastically unlearnable states, pseudo-count increments remain small.
- **Adaptive Curiosity**: The article directly addresses how to measure *novelty* via changes in probability. This approach resonates with curiosity-driven exploration, focusing on states that reduce model uncertainty.  
- **Worth Citing?** Absolutely. It is a seminal paper reconciling count-based exploration, information gain, and practical deep RL methods. Highly relevant for those studying robust exploration or curiosity in complex, partially random tasks.

---

## How It May Inform Future Work

1. **Advanced Generative Models**  
   Using more sophisticated image density networks (e.g., VAE, PixelCNN) might produce richer pseudo-counts, clarifying partial environment randomness vs. truly learnable structure.
2. **Continuous Domains**  
   The authors hint at extending pseudo-counts to continuous spaces, possibly combining with approximate nearest neighbors or manifold embeddings.
3. **Long-Horizon vs. Immediate Info Gain**  
   They highlight that maximizing immediate prediction gain is suboptimal; future efforts could study multi-step info gain to handle partial randomness.
4. **Hybrid with Ensemble Approaches**  
   Combining ensemble disagreement (for dynamics) with pixel-based pseudo-counts might further disambiguate noise from novelty in partially random RL.

---

## Open Questions or Critiques

- **Density Model Choice**: CTS is basic and can misrepresent complex frames (leading to approximate counts). Future results hinge on better-likelihood neural networks.  
- **Stochastic Transitions**: If an environment has large, irreducible noise, model adaptation alone may not always prevent artificially high counts in ephemeral states.  
- **Full Theoretical Guarantees**: The authors show tabular-like theoretical bridging, but real high-dimensional tasks remain subject to approximation error.  
- **Implementation Complexity**: Real-time training with large-scale density estimation can be computationally intensive. More optimized or specialized model approaches might be needed in bigger RL domains.
