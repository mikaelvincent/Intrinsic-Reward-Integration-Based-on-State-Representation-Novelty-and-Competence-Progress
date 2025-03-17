# What is intrinsic motivation? A typology of computational approaches

> **Authors**: Pierre-Yves Oudeyer, Frederic Kaplan
> **Date**: 2 November 2007
> **Link**: <https://doi.org/10.3389/neuro.12.006.2007>

---

## Selected Direct Quotes, Formulas, and Data

Below are direct excerpts and paraphrased formulas preserving the article’s essential details.

1. **General Concept of Intrinsic Motivation**  
   - *“Intrinsic motivation is defined as the doing of an activity for its inherent satisfaction rather than for some separable consequence.”* (Ryan and Deci, 2000, p.56)  
   - *"When intrinsically motivated, a person is moved to act for the fun or challenge entailed rather than because of external products, pressures, or rewards.”*  
   - The authors highlight that in psychology, *intrinsic* vs. *extrinsic* motivation is about whether an activity is done “for its own sake” or to reach a separate outcome.

2. **Computational Reinforcement Learning (CRL) Framework**  
   - The paper adopts the notion that a reward is just a numerical signal to be maximized, *without prescribing how or where it is generated.*  
   - *Extrinsic* motivations: The reward is externally imposed or measures external performance.  
   - *Intrinsic* motivations: The reward is internally computed to reflect aspects like novelty, surprise, predictive error, competence, etc.

3. **Typology of Intrinsic Motivation**  
   The authors propose three major computational classes:

   **(A) Knowledge-Based Models**  
   Focus on dissonances or resonances between *experience* and the agent’s *internal knowledge/expectations*.  
   - **Information-Theoretic / Distributional**  
     - *Uncertainty Motivation (UM)*  
       \[
         r(e_k) = C \cdot \frac{1}{P(e_k)},
       \]
       encouraging the agent to visit low-probability (novel) events.  
     - *Information Gain Motivation (IGM)*  
       \[
         r(e_k) = C \cdot [ HE_t - HE_{t+1} ],
       \]
       i.e., the decrease in entropy about event distributions.  
     - *Distributional Surprise (DSM)*  
       \[
         r(e_k) = C \cdot \frac{P(e_k)}{1 - P(e_k)},
       \]
       awarding events that strongly violate prior probabilities.  
     - *Distributional Familiarity (DFM)*  
       \[
         r(e_k) = C \cdot P(e_k),
       \]
       awarding frequently observed states (inverse of novelty).

   - **Predictive**  
     - The agent uses a predictor \(\Pi\) to forecast next states or outcomes:
       \[
         \Pi(\text{context}) = \hat{e}_{t+1}.
       \]
       Then measure errors or improvements in these predictions.  
     - *Novelty Motivation (NM)*:  
       \[
         r(\mathbf{SM}(t)) = C \cdot \text{Error}(\Pi),
       \]
       awarding large predictive errors.  
     - *Intermediate Level Novelty (ILNM)*  
       \[
         r(\mathbf{SM}(t)) = C_1 \exp\Bigl(-C_2 (\text{Error}(\Pi) - \sigma)^2\Bigr),
       \]
       awarding mid-range errors.  
     - *Learning Progress (LPM)*:  
       \[
         r(\mathbf{SM}(t)) = \text{Error}_{\text{old}} - \text{Error}_{\text{new}},
       \]
       or a region-based average of error reductions. Encourages states where the agent is *improving* predictions.  
     - *Predictive Surprise (SM)*:  
       \[
         \text{surprise} \;=\; \frac{\text{Error}(\Pi)}{\text{ExpectedError}(\Pi)},
       \]
       awarding events that are unexpectedly mispredicted.  
     - *Predictive Familiarity (FM)*:  
       \[
         r(\mathbf{SM}(t)) = \frac{C}{\text{Error}(\Pi)},
       \]
       awarding well-predicted states (low error).

   **(B) Competence-Based Models**  
   The agent sets *self-determined goals*, then measures competence or improvement in achieving them.  
   - The agent picks a goal \(g_k\) and tries to reach it with a known-how module \(\text{KH}\).  
   - After a goal-reaching attempt, the agent measures a *level of achievement* \(\ell_a(g_k)\). Intrinsic reward is a function of that achievement or its improvement.  
     - *Maximizing Incompetence (IM)*:  
       \[
         r \;\propto\; \ell_a(g_k)\quad\text{(low competence → high reward)}
       \]
     - *Maximizing Competence Progress (CPM / Flow)*:  
       \[
         r \;\propto\;\bigl[\ell_a(g_k)\bigr]_{\text{new}} - \bigl[\ell_a(g_k)\bigr]_{\text{old}},
       \]
       awarding improved competence (akin to “optimal challenge” or Flow).  
     - *Maximizing Competence (CM)*:  
       \[
         r \;\propto\;\ell_a(g_k),
       \]
       awarding highly mastered goals.

   **(C) Morphological Models**  
   Based on *direct “shape” or correlation properties* of the sensorimotor flow itself (no reference to internal knowledge or goals).  
   - *Synchronicity (SyncM)*: awarding high short-term correlation among channels.  
   - *Stability (StabM)*: awarding states close to some average (i.e., minimal variation).  
   - *Variance (VarM)*: awarding states with maximal variation.

4. **Non-Intrinsic Motivations**  
   The paper also clarifies that certain internal drives (like energy maintenance or social presence drives) are *internal but not intrinsic*, as they revolve around specific sensorimotor variables with “meaningful” references, rather than being about knowledge-based or competence-based channels.

5. **Further Observations and Summary Table**  
   - The paper compiles a table (their Figure 7) listing each type of motivational model (UM, IGM, LPM, CPM, StabM, etc.), categorizing them along multiple dimensions: 
     - *Intrinsic vs. Extrinsic*,  
     - *Adaptive vs. Fixed*,  
     - *Knowledge-based vs. Competence-based vs. Morphological*,  
     - *Homeostatic vs. Heterostatic*.  
   - The table also rates each model’s *exploration potential*, *organization potential*, computational cost, and whether any example models exist in the literature.

6. **Conclusions and Future Directions**  
   - The authors argue a single “universal” definition of intrinsic motivation is elusive.  
   - They propose investigating systematically each approach’s influence on learning and exploration in various environments.  
   - *Adaptive, heterostatic, knowledge-based or competence-based motivations* show the greatest promise for open-ended development.  
   - They highlight the importance of embodiment: the same “agnostic” reward function can produce very different behaviors depending on the agent’s body and environment.  
   - They foresee that combining these formal frameworks with real-world robotic experiments can help clarify psychological and neuroscientific theories regarding exploration and curiosity.

---

## Concise Summary of the Article

**Oudeyer and Kaplan** review how *intrinsic motivation* has been conceptualized in psychology (e.g., curiosity, novelty-seeking, optimal challenge) and highlight the vagueness or inconsistencies of such definitions when translated into computational terms. They situate intrinsic motivation within a *computational reinforcement learning* (CRL) framework, analyzing how numerical rewards can be generated *internally* based on novelty, prediction error, learning progress, or competence progress—rather than externally by a human-defined task.

They propose a **formal typology** to categorize potential intrinsic motivation systems in robots or artificial agents:

1. **Knowledge-Based** systems:  
   - Either measure *information-theoretic* qualities (e.g., Shannon surprises, distributional novelty) or *predictive* qualities (prediction error, surprise, learning progress).  

2. **Competence-Based** systems:  
   - Agent self-generates goals or challenges, then calculates intrinsic rewards from how well (or how *improved*) the agent satisfies these goals (e.g., “Flow” via increasing mastery).

3. **Morphological** systems:  
   - Award properties directly from the sensorimotor stream’s structure (like correlation, variance, or stability), *ignoring* explicit internal knowledge or competence.

Additionally, they illustrate some **non-intrinsic** motivations that are purely homeostatic (like maintaining an energy level). The authors provide a summary table, clarifying each approach’s potential for exploration and organization, approximate computational cost, and whether it has precedents in the literature.

In closing, they emphasize that these architectures are “meaning-agnostic”; the same curiosity formula can yield varied emergent behaviors depending on the agent’s embodiment and environment. They encourage a systematic investigation of which types of intrinsic motivation lead to open-ended, organized developmental trajectories, and propose that further robotic experiments can refine psychological and neuroscientific theories about curiosity-driven learning.

---

## Significance and Relevance to “Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments”

- **Significance**:  
  This article is one of the earliest and most comprehensive attempts to *systematically formalize* intrinsic motivation in computational terms. It highlights how *learning progress, predictive error, competence improvement, and other signals* can drive exploration, all purely from *internal reward signals.*  

- **Relevance**:  
  - *Partially Random RL*: Many knowledge-based or competence-based measures aim at focusing the agent on states or goals where it can *reduce uncertainty*, thus ignoring or discounting irreducibly random transitions. This notion is central to “adaptive curiosity,” which must avoid infinite loops on noise-laden states.  
  - *Adaptive Curiosity*: The authors explore “learning progress” (LPM) or “Flow” (CPM) as prime drivers for progressive, organized exploration—ideas that are central to advanced partially random RL tasks where naive novelty might fail.  
  - Their *unifying typology* helps clarify which approach best handles partial randomness and fosters structured, open-ended skill acquisition.

Thus, the paper is *very relevant* for investigators studying “Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments.” It both offers a taxonomy of reward definitions and underscores how certain families of intrinsic rewards can systematically drive curiosity and learning in uncertain domains.

---

## Worth Citing?

**Yes.** This paper remains a foundational resource for:
- Clarifying the difference between *internal vs. external* and *intrinsic vs. extrinsic* motivations in computational terms.
- Providing a structured typology of *knowledge-based*, *competence-based*, and *morphological* intrinsic rewards.
- Tracing theoretical links between psychological concepts (novelty, surprise, flow) and formal RL reward design.

Its thoroughness and systematic approach make it a key reference in the literature on curiosity-driven or self-motivated exploration.

---

## How It May Inform Future Research

1. **Testing Each Approach in Noisy or Partially Observed Settings**  
   The authors suggest that many morphological or predictive novelty measures could produce distinct behaviors depending on environment structure. Researchers could systematically implement, e.g., *learning progress*, *competence progress*, *morphological correlation*, in partially random tasks and compare which yields stable, progressive exploration.

2. **Blending Competence-Based and Knowledge-Based Approaches**  
   Combining the agent’s drive to learn accurate models with a drive to set and master self-generated goals might be especially powerful in random or high-dimensional domains.

3. **Hierarchical or Multi-Goal Curiosity**  
   The competence-based perspective can be expanded to multi-level skill discovery, where the agent tries increasingly complex goals, harnessing partial randomness for deeper exploration without stalling on noise.

4. **Developing Theories for Neural/Brain Circuits**  
   As the authors highlight, bridging these computational frameworks with neuroscience data might illuminate how the human brain (e.g., dopaminergic systems) implements curiosity or novelty detection.

5. **Applications in Educational Technologies**  
   Systems that adaptively set tasks at the learner’s “optimal challenge level” could be guided by *learning progress* signals, relating to the “Flow” concept for tutoring or personalized learning.

---

## Open Questions or Possible Critiques

- **Behavioral Outcome vs. Reward Mechanism**: Some definitions (like “Flow” or “optimal incongruity”) remain subject to interpretation. The article’s emphasis on *mechanistic definitions of reward* helps but raises open challenges of how best to measure success or progress in unstructured tasks.
- **Scalability**: Many proposed forms (e.g., distribution-based, region-splitting, forward-model error) might be computationally expensive in large continuous spaces with partial randomness, requiring advanced function approximators or hierarchical learning.
- **Long-Horizon Dependencies**: The immediate or short-term error-based signals (e.g., novelty or surprise at time t) might not capture multi-step dependencies crucial in many tasks.  
- **Embodiment**: While the authors stress the importance of the robot’s body and environment, clarifying how to systematically incorporate morphological constraints into intrinsic reward remains an open frontier.  
- **Which Combination of Mechanisms?**: The article proposes a set of potential formulas. In practice, multiple forms of curiosity might co-occur. Determining the “best mix” under partial randomness or real-world complexities is still an open research area.
