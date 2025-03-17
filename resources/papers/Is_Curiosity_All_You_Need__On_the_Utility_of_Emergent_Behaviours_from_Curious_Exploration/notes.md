# Is Curiosity All You Need? On the Utility of Emergent Behaviours from Curious Exploration

> **Authors**: Oliver Groth, Markus Wulfmeier, Giulia Vezzani, Vibhavari Dasagi, Tim Hertweck, Roland Hafner, Nicolas Heess, Martin Riedmiller
> **Date**: 17 September 2021
> **Link**: <https://doi.org/10.48550/arXiv.2109.08603>

---

## Notes

### Selected Direct Quotes, Data, and Formulas

1. **Core Motivation**  
   > “Curiosity-based reward schemes can present powerful exploration mechanisms which facilitate the discovery of solutions for complex, sparse or long-horizon tasks. [...] However, as the agent learns to reach previously unexplored spaces and the objective adapts to reward new areas, many behaviours emerge only to disappear due to being overwritten by the constantly shifting objective.”

   The authors note that while curiosity can yield diverse emergent behaviors (e.g., in robotics), these behaviors often vanish once the curiosity-driven policy updates further. They propose harnessing and retaining such self-discovered behaviors for future tasks.

2. **Off-Policy Curiosity (SelMo) Architecture**  
   - **Forward Model**: A neural network \(f_{\mathrm{dyn}}\) predicts the next state \(\hat{s}_{t+1} = f_{\mathrm{dyn}}(s_t, a_t)\).  
   - **Curiosity Reward**: Defined by the *prediction error* \(\|f_{\mathrm{dyn}}(s_t, a_t) - s_{t+1}\|^2\), scaled by a factor \(\eta_r\) and bounded by a \(\tanh\).  
   - **Two Replay Buffers**: 
     1. **Model Replay** \(D_M\): Stores newly collected trajectories. Batches from this buffer train the forward model and then get labeled with curiosity rewards.  
     2. **Policy Replay** \(D_\pi\): Stores these labeled trajectories for off-policy learning of the exploration policy \(\pi\).  

   This design decouples forward-model updates from policy updates, potentially capturing a broader range of data. See their Figure 2 for an overview.

3. **Emergent Behaviors**  
   The authors run *only curiosity-based training* for 100k episodes in two continuous-control environments:

   - **JACO (9-DoF Arm + Two Cubes)**:  
     - The arm discovers pushing cubes, sliding them along slanted walls, eventually learning lifting and moving multiple objects over large distances.  
     - Emergent sub-behaviors: picking objects reliably, balancing a cube on its edge, manipulating two cubes simultaneously.

   - **OP3 (20-DoF Humanoid)**:  
     - The robot first learns to avoid “death” (falling) due to curiosity’s positive reward structure.  
     - It later discovers basic forward/backward stumbling, uses its arms for counterbalance, sits down safely, transitions to more advanced stepping and leaps.

   These complex behaviors appear *without* any extrinsic reward, purely from maximizing prediction error of the forward model.

4. **Behavior Changes over Time**  
   - Because the curiosity objective always seeks novel, unpredictable transitions, once a certain behavior is “mastered,” the agent’s forward model can predict it well, reducing curiosity reward. This leads to a shift in policy to new behaviors.  
   - They illustrate “timelines” showing how, e.g., the robotic arm devotes ~15k episodes to learning reliable object lifting, then transitions to “long-distance moves,” then “balancing poses,” etc. The behaviors appear and vanish in cycles.

5. **Retaining Emergent Behaviors**  
   - The authors highlight that these short-lived “useful skills” could benefit future tasks if preserved.  
   - They propose a simple snapshot approach: *store policy checkpoints* from various training stages as potential “skills.” A new hierarchical RL method can load these snapshots as sub-policies for a downstream task.  
   - In the JACO environment, they demonstrate that using these curiosity-based snapshots as sub-policies in a hierarchical framework can perform on par with a carefully engineered curriculum (SAC-X) for the *lift_red* task.

6. **Discussion**  
   - Current curiosity methods may quickly overwrite previously learned behaviors.  
   - The authors suggest building more sophisticated solutions to identify, store, and reuse the emergent behaviors in a never-ending, curiosity-driven learning loop.  
   - They also mention related works on skill discovery from diversity or empowerment. Their approach specifically highlights *forward-model error* but might integrate with these alternative signals in the future.  
   - Finally, they note the importance of a “distributed” or decoupled architecture (model replay vs. policy replay) for data efficiency in large-scale robotic tasks.

7. **Key Contributions**  
   1. **SelMo**: An off-policy curiosity method that yields complex, meaningful manipulation and locomotion behaviors in 3D environments.  
   2. **Behavior Snapshot**: A simple but effective technique for reusing emergent behaviors in hierarchical RL, matching performance of hand-engineered multi-task curricula.  
   3. **Empirical Evidence**: Detailed timelines, examples, and tasks (lift, walking) confirm that emergent skills appear purely from maximizing curiosity.

---

### Concise Summary of the Article

Groth *et al.* focus on how curiosity-based RL policies exhibit continually shifting behaviors—some of which can be highly sophisticated but then vanish after the forward-model no longer finds them surprising. The authors introduce **SelMo**, an off-policy curiosity architecture that separately updates a forward predictive model and the exploration policy from replay buffers. In complex simulated robotics tasks (a 9-DoF arm with cubes, a 20-DoF humanoid), **pure** curiosity alone induces elaborate manipulations and locomotion patterns without extrinsic rewards.  

They emphasize that intermediate behaviors—like steady object lifting or one-foot balancing—are eventually lost because the dynamic curiosity objective pushes the policy toward *new* high-error transitions. However, these ephemeral behaviors might be *valuable skills* for future tasks. They demonstrate a straightforward approach: store policy snapshots as sub-policies, then reuse them in a hierarchical method for a new goal (e.g. lifting a cube). This simple pipeline outperforms training from scratch and even rivals a specialized multi-auxiliary reward method (SAC-X).  

Hence, the authors argue that curiosity should not be viewed merely as a “bonus reward” for standard RL but rather as an “independent aspect” of the agent’s learning pipeline. They advocate deeper solutions for robustly identifying, saving, and reusing emergent behaviors in endless learning scenarios.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Partial Randomness**: The environment could contain random or unpredictable transitions (e.g., collisions, noisy dynamics). The forward-model-based curiosity in SelMo tends to discount transitions once they become predictable, thus it can remain robust if truly random aspects are recognized as “noise” after enough data.  
- **Adaptive Curiosity**: The paper underscores a crucial challenge in curiosity-based RL: once a skill is learned, the agent abandons it for new novelty. They propose capturing these ephemeral behaviors as “snapshots,” demonstrating how these can significantly accelerate *related tasks*. This approach is highly relevant to the theme of maintaining an ever-growing repertoire of learned skills in partially random domains.  

Therefore, the paper **is relevant**. It demonstrates that “curiosity alone” can yield valuable, nontrivial skills (like object balancing or backward leaps) in a highly parametric environment, but these skills vanish if not actively retained. That perspective strongly aligns with “adaptive curiosity” approaches that aim to accumulate stable competencies despite environmental randomness or constantly shifting intrinsic objectives.

---

### Worth Citing?

**Yes.** The article offers:

1. **Empirical Insights** into how curiosity alone can yield advanced, physically plausible behaviors in 3D robotics—beyond simpler tasks often explored in prior curiosity works.  
2. **Discussion** of ephemeral skill emergence and the necessity of an approach to preserve them.  
3. **Demonstration** that a naive “snapshot-based” approach can effectively reuse emergent behaviors for new tasks, matching specialized multi-task methods.

Their emphasis on preserving ephemeral skills to build a “curiosity-driven skill library” is an important direction for open-ended or continual learning research.

---

### How It May Inform Future Research

1. **Skill Identification & Retention**: The authors propose storing entire policy checkpoints. More advanced methods might identify skill boundaries automatically, store them, and compose them in hierarchical RL for future tasks.  
2. **Unified Intrinsic and Extrinsic**: Combining curiosity with small extrinsic signals might accelerate multi-object or multi-stage robotics tasks.  
3. **Noisy or High-Dimensional**: Further investigation can see how well the approach copes with partial randomness in real-world or higher-dimensional domains. Perhaps additional discounting or robust modeling is needed to filter out truly unpredictable transitions.  
4. **Continual / Lifelong Learning**: This work suggests a potential pipeline for never-ending skill discovery: curiosity to generate ephemeral behaviors, an automated system to “snapshot” and incorporate them. More robust system designs could yield a layered skill library for open-ended tasks.

---

### Open Questions or Possible Critiques

- **Automatic Skill Extraction**: Storing entire policy snapshots is coarse. A more refined approach might split or compress discovered behaviors into re-usable partial skills.  
- **Conflicts in Multi-Snapshot Usage**: If multiple policy snapshots are included as sub-policies, how does the agent coordinate them? The authors show a simple hierarchical method, but scaling to many sub-policies might cause confusion or redundancy.  
- **Truly Random Transitions**: If some environment transitions are heavily stochastic, does the forward-model-based approach produce ephemeral exploitative behaviors or degenerate loops? Additional experiments with stronger partial randomness might clarify.  
- **Sample Efficiency & Real-World**: The method uses a large number of episodes (100k) in simulation. Deploying this curiosity approach on real robots could be more challenging. The paper does not fully address real-world constraints.  
- **Stability in Off-Policy Curiosity**: Off-policy curiosity might face replay data from older forward-model states, leading to mislabeled transitions or delayed labels. The authors mitigate with a two-buffer approach, but more thorough analysis might be needed.
