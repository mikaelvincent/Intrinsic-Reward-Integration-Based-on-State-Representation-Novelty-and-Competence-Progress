# Variational Option Discovery Algorithms

> **Link**: <https://doi.org/10.48550/arXiv.1807.10299>

> **Parenthetical**: (Achiam et al., 2018)
> **Narrative**: Achiam et al. (2018)

---

## Notes

### Selected Direct Quotes, Data, and Formulas

1. **Motivation and Setup**  
   > “We explore methods for option discovery based on variational inference and make two algorithmic contributions.”  
   The authors focus on discovering *options* (skills or modes of behavior) in reinforcement learning environments *without* relying on a specific extrinsic reward. Instead, they employ an unsupervised, information-theoretic objective that partitions the agent’s behavior space into distinct modes.

2. **Variational Option Discovery**  
   - The core principle is to sample a **context** \(c\) from a distribution \(G\), then run a *policy* \(\pi\) that conditions on \(\bigl(s_t, c\bigr)\) to generate a trajectory \(\tau\).  
   - A **decoder** \(D\) tries to recover the original context \(c\) from \(\tau\).  
   - The agent is *rewarded* for making \(\tau\) easily distinguishable from other trajectories associated with different contexts.  
   - The objective (Eq. 2 in the paper) is to maximize \(\mathbb{E}[\log P_D(c \mid \tau)]\) plus an entropy regularization term on the policy.  
   \[
     \max_{\pi,D}\;\;\mathbb{E}_{c \sim G,\;\tau \sim \pi(\cdot \mid c)}\bigl[\log P_D(c \mid \tau)\bigr] \;+\; \alpha\,H(\pi).
   \]  
   This resembles a **\(\beta\)-VAE** objective, with the policy as the “encoder” and the decoder as the “decoder.”

3. **Connections to Previous Works**  
   - **Variational Intrinsic Control (VIC)** (Gregor et al. 2016): focuses on mutual information between the *final state* \(s_T\) and the context \(c\).  
   - **Diversity is All You Need (DIAYN)** (Eysenbach et al. 2018): maximizes mutual information between *all states* \(s_t\) and \(c\). Minimizes mutual information between \(\{a_t\}\) and \(c\) given \(s_t\).  
   Both VIC and DIAYN are special cases of this general autoencoding objective, but decode from partial trajectories (e.g., final states) rather than *full* trajectories.

4. **VALOR (Variational Autoencoding Learning of Options by Reinforcement)**  
   The authors introduce **VALOR**:  
   - The *decoder* sees the entire trajectory (or selected frames/deltas) rather than just single states.  
   - This encourages “dynamical modes” (e.g., *move in a circle*) instead of simply “goal states.”  
   - They use a bidirectional LSTM to decode a small set of spaced observations (or transitions) from the trajectory.

5. **Curriculum Trick**  
   - In many tasks, training with a large number of possible contexts \(K\) is difficult from the start.  
   - They propose a schedule: start with a small \(K\), then *increase* \(K\) whenever the agent’s decoder can reliably distinguish the existing contexts (i.e., if \(\log P_D(c \mid \tau)\) is high enough).  
   \[
     K \leftarrow \min\bigl(\lfloor1.5 \times K + 1\rfloor,\; K_{\max}\bigr).
   \]
   - This stabilizes learning and allows an agent to discover *many more* distinct behaviors.

6. **Comparisons and Findings**  
   - The paper compares **VALOR**, **VIC**, and **DIAYN** on continuous control tasks (2D point, HalfCheetah, Swimmer, Ant) plus more complex setups (a robotic hand environment and a humanoid “toddler” model).  
   - **All** methods can discover diverse locomotion or manipulation behaviors in moderately sized tasks.  
   - The *curriculum approach* significantly stabilizes training and expands the number of learnable modes from tens to hundreds in simpler domains.  
   - In a very high-dimensional “toddler” humanoid environment, *purely* information-theoretic methods produce “unnatural” behaviors. The authors argue that additional priors or constraints might be necessary for truly complex tasks.  
   - They show a preliminary test in an **Ant-Maze** environment, reusing a fixed VALOR-trained policy as a lower-level skill. Performance was comparable to training from scratch or using a non-hierarchical agent.

7. **Open Challenges**  
   - **Trivial signposting**: Agents can “encode” contexts in small changes or remain in a narrow region, cheaply fooling the decoder.  
   - **Complex, High-DoF** tasks (like humanoid) do not yield physically intuitive behaviors if guided only by information-theoretic novelty.  
   - **Hierarchies**: Using discovered options for subsequent downstream tasks is a natural direction, but results on the authors’ Ant-Maze experiment do not show large advantages over baseline methods.

---

### Concise Summary of the Article

**“Variational Option Discovery Algorithms”** thoroughly examines and extends unsupervised RL approaches that use a variational inference perspective to learn distinct modes of behavior (options). The authors:

1. **Unified Framework**: They show how prior works like VIC and DIAYN fit into a general *autoencoding objective* where a policy “encodes” contexts into trajectories, and a decoder tries to recover those contexts.  
2. **VALOR**: Introduce a new method, **Variational Autoencoding Learning of Options by Reinforcement (VALOR)**, which decodes entire trajectories (via a recurrent model) rather than individual states.  
3. **Curriculum Approach**: Propose gradually increasing the number of contexts when the decoder has “mastered” the current set, stabilizing training and enabling an agent to discover *many* distinct behaviors.  
4. **Experiments**:  
   - In MuJoCo locomotion tasks (Cheetah, Swimmer, Ant), all variational methods produce interesting multi-modal behaviors.  
   - In a simpler 2D Point environment, the curriculum allows learning up to hundreds of distinct modes.  
   - In a more challenging *robot hand* environment, VALOR finds natural finger motions.  
   - In a *humanoid toddler* environment, purely “information-based” skill discovery is insufficient to produce natural crawling or walking.  
   - A test on **Ant-Maze** shows that a pre-trained VALOR skill policy works as well as training from scratch, albeit not surpassing it.  
The authors conclude that while *variational option discovery* is a promising direction for unsupervised skill learning, additional domain priors or constraints may be required to produce truly human-like or systematically beneficial options in large complex tasks.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Multi-Mode Discovery**: The approach’s mutual-information-based objective fosters *diverse* behaviors (options) that might be relevant for *adaptive curiosity*, where an agent tries to systematically discover novel (but stable) ways to interact with the environment.  
- **Partial Randomness**: The authors highlight pitfalls when environment noise (or narrow signposting) can cheaply encode contexts. Additional constraints or shaping might be needed to differentiate truly *controllable novelty* from random transitions.  
- **Big Picture**: While not explicitly about “curiosity in partially random domains,” the *variational approach* to skill discovery has overlap with curiosity-driven methods. The same mutual-information logic can help the agent avoid infinite exploration of purely random states—once the context-labeled trajectory is recognized as random, the decoder can’t reliably identify it.

Hence, **this article is certainly relevant** to advanced curiosity research. It explores *information-based skill learning*, clarifies limitations, and proposes solutions for stable multi-mode training.

---

### Worth Citing?

**Yes.** The paper:

1. **Formalizes** a broad “autoencoder” view unifying VIC, DIAYN, and their newly introduced **VALOR** approach.  
2. **Demonstrates** the importance of a *curriculum for context distributions*, significantly improving stability and enabling large numbers of discovered modes.  
3. **Highlights** open challenges: naive information-based objectives can yield suboptimal or “unnatural” behaviors in high-dimensional or partially random domains.

Researchers investigating unsupervised RL, skill discovery, or curiosity-based exploration will find the authors’ analysis and methods highly instructive.

---

### How It May Inform Future Research

1. **Hybrid Curiosity + Option Discovery**: Combining *variational skill discovery* with *intrinsic rewards* that discount uncontrollable randomness or prioritize agent-meaningful transitions might produce more robust exploration in partially random tasks.  
2. **Hierarchical or Multi-Task**: The authors’ preliminary success in reusing VALOR’s skill policy suggests further multi-task or meta-RL experiments where learned modes accelerate downstream training.  
3. **Domain Priors**: For complex robotics (e.g., humanoids), adding physics-based or morphological priors might guide the learned options toward more natural, stable behaviors.  
4. **Adaptive Decoding**: Reducing trivial solutions or “narrow signposting” could involve dynamic constraints on the decoder or environment interactions, ensuring discovered options remain globally distinguishable.

---

### Open Questions or Possible Critiques

- **“Trivial” Trajectories**: Like other skill-discovery methods, VALOR can produce behaviors that encode contexts cheaply, e.g. micro-jitters or localized signposting. Additional constraints or shaping might be needed to ensure globally meaningful options.  
- **Handling Environment Noise**: The approach does not explicitly discount irreducible randomness. Over repeated training, if the environment has partial randomness, the agent might struggle to maintain distinct, stable trajectories for each context.  
- **Humanoid Complexity**: The authors note that “purely information-theoretic” objectives fail to produce natural walking or crawling in the toddler environment. Further research on combining domain knowledge with the unsupervised objective is necessary.  
- **Scaling and Sample Efficiency**: Large-scale tasks with high dimensional action/state spaces might require more advanced or data-efficient RL backends than vanilla policy gradient to make unsupervised discovery feasible at scale.  
- **More Hierarchical Evaluations**: Using discovered options for complex tasks remains an open research frontier—some tasks might require specialized or heavily guided skill sets beyond general coverage.  
