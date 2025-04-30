# Minigrid & Miniworld: Modular & Customizable Reinforcement Learning Environments for Goal-Oriented Tasks

> **Link**: <https://doi.org/10.48550/arXiv.2306.13831>

> **Parenthetical**: (Chevalier-Boisvert et al., 2023)
> **Narrative**: Chevalier-Boisvert et al. (2023)

## Notes

### Selected Direct Quotes, Data, and Formulas

1. **Core Focus**  
   > “We present the Minigrid and Miniworld libraries which provide a suite of goal oriented 2D and 3D environments. [...] The libraries were explicitly created with a minimalistic design paradigm to allow users to rapidly develop new environments for a wide range of research-specific needs.”

2. **Motivation**  
   > “Minigrid and Miniworld focus on providing users with the following features: easy installation, customizability, easy visualization, and scalable complexity. [...] They have already been used for research in safe RL, curiosity-driven exploration, and meta-learning.”

3. **Design Philosophy**  
   - Both libraries use Python and the Gym/Gymnasium RL interface.
   - Minimizing external dependencies fosters simpler installation and fewer compatibility issues.
   - Emphasize small, transparent codebases over more feature-heavy or complex game engines.

4. **Environment Details**  
   **Minigrid**  
   - “Each environment is a 2D GridWorld made up of n×m tiles. [...] The default observation is partially observable, capturing a small region in front of the agent plus the agent’s direction and a textual mission.”
   - Actions: 7 discrete actions: `[turn left, turn right, move forward, pickup, drop, toggle, done]`.
   - Default reward is sparse (non-zero only when the mission is accomplished).

   **Miniworld**  
   - “A 3D world with connected rooms and objects, but uses a flat floor plan. [...] Observations are RGB images of size 80×60 from the agent’s perspective, with a similar action space plus a ‘move back’ action.”
   - Also uses a sparse reward by default, but can be adapted.

5. **Environment Generation / API**  
   - Both libraries provide a `_gen_grid()` (Minigrid) or `_gen_world()` (Miniworld) function where users place walls, objects, and the agent.
   - This short script-based approach yields fully customized levels, with examples given in Listing 2 of the paper.

6. **Adoption in Research**  
   - The paper lists multiple usage examples:
     - **Curriculum Learning**: e.g., Dennis et al. (2020) automatically generate environment tasks.  
     - **Exploration**: sparse-reward setups used by Seo et al. (2021) and Zhang et al. (2021).  
     - **Meta-Learning & Transfer**: e.g., Igl et al. (2019), Liu et al. (2021) with flexible environment variation.

7. **Case Studies**  
   1. **RL Agent Transfer** between Minigrid and Miniworld:  
      - Trained a PPO agent on a “goto object” environment in Minigrid.  
      - Transferred partial policy weights (actor, critic, mission embeddings) to an equivalent environment in Miniworld.  
      - Found certain partial transfers can accelerate learning in Miniworld by 8–16%.

   2. **Human Subject Transfer**:  
      - Recruited 10 participants who first learned a 2D FourRooms environment (Minigrid) and then transferred to 3D FourRooms (Miniworld).  
      - Observed small performance gains (in average reward) vs. participants directly using the Miniworld environment.

8. **Implementation & Customization**  
   - Showcases how minimal code (∼100–150 lines) is needed to build new tasks or adapt existing ones.  
   - They highlight the unified API for mission text, environment definitions, top-down or first-person rendering, etc.

9. **Comparison with Other Libraries**  
   - MazeBase, Griddly: older or more complex 2D libraries, often not purely in Python or lacking a lightweight approach.  
   - DeepMind Lab, ViZDoom: more advanced 3D engines with steep customization overhead.  
   - Robot control libraries (dm_control, IsaacSim, etc.) can be overkill for pure RL tasks, as physics is more complicated to extend.

10. **Limitations and Future Plans**  
    - “The environment creation process prioritizes minimal functions, limiting environment types possible.”  
    - “Written in Python, so it’s slower than some C++-based engines.”  
    - They intend to expand capabilities for human-in-the-loop decision-making.  

11. **Open-Source & Usage Statistics**  
    - Hosted on GitHub with an Apache-2.0 license.  
    - ~2400 GitHub stars, ~620 forks, and ~470 citations for Minigrid (Google Scholar).  
    - Maintained by the Farama Foundation, with separate docs: <https://minigrid.farama.org> and <https://miniworld.farama.org>.

---

### Concise Summary of the Article

Chevalier-Boisvert *et al.* present **Minigrid** and **Miniworld**, two libraries that generate **lightweight, customizable** 2D and 3D RL environments. Both libraries share a minimalistic design philosophy: they avoid large dependencies, use Python, and adopt the Gym/Gymnasium API. Key features include:

- **GridWorld or 3D Maze**: Agents must navigate or interact with objects in partially observable settings.  
- **Sparse Rewards**: By default, the agent only receives a reward when completing a goal (reaching a location or picking an object). This fosters exploration strategies.  
- **Flexible Environment Generation**: A few lines of code define the layout, object placements, and agent spawn.  
- **Research Adoption**: Widely used for investigating safe RL, exploration heuristics, curriculum learning, meta-learning, and language-conditioned tasks. Examples include blending navigation with textual instructions (BabyAI).  
- **Case Studies**:  
  1. **RL Transfer** from Minigrid to Miniworld “GotoObject” tasks. They tested multiple ways to freeze or transfer the policy’s actor/critic and mission embedding. Some partial transfers improved sample efficiency in the 3D environment.  
  2. **Human Transfer** from 2D FourRooms to 3D FourRooms: 10 participants saw slight performance gains when doing Minigrid first, then Miniworld.

They highlight that the code is easily extensible (∼100–150 lines) for new tasks or modifications. The authors see Minigrid/Miniworld as an ideal middle ground between extremely simple 2D tasks and fully realistic 3D simulation, enabling flexible experimentation with goal-oriented RL or instruction-based tasks.

---

### Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Sparse Reward + Partial Observability**: Both libraries produce challenging exploration tasks. Agents often need curiosity or advanced exploration methods to succeed. Past works have specifically used Minigrid and Miniworld for **curiosity-driven** RL, taking advantage of the environment’s minimal design and easily variable complexity.  
- **Customizable**: Researchers studying partially random transitions can inject noise or random layout seeds. This fosters a wide array of semi-stochastic or random tasks, enabling evaluation of “adaptive curiosity” algorithms that handle partially random states.  
- **Conclusion**: The paper and libraries strongly support research on curiosity or exploration under partial randomness. By default, they are widely used to test exploration algorithms that must handle high-level tasks with minimal extrinsic reward.

Hence, this paper is **highly relevant** to any project investigating curiosity-driven or exploration-based RL in partially random or generative grid/3D domains.

---

### Worth Citing?

**Yes.** It provides a **core reference** for:

- Introducing the design philosophy behind Minigrid and Miniworld.  
- Clarifying environment generation and usage.  
- Showcasing real research cases where these libraries accelerate or focus exploration-based RL approaches.

For studies on environment design or new RL method benchmarks, it’s a prime source.

---

### How It May Inform Future Research

1. **Developing or Testing Intrinsic Rewards**: Users can produce partially random or multi-object tasks easily, enabling thorough testing of curiosity-based or self-supervised methods in both 2D and 3D.  
2. **Language + Navigation**: The libraries’ built-in text mission features open a path for investigating language-conditioned curiosity or instruction following.  
3. **Transfer Between Observations**: The authors show transferring from 2D top-down to 3D first-person can be studied systematically—like cross-modal adaptation or domain randomization experiments.  
4. **Human-in-the-Loop**: Potentially extend the “manual control” code to gather real-time demonstration or preference feedback, bridging interactive or collaborative RL with partial environment randomness.

---

### Open Questions or Possible Critiques

- **Complex Tasks**: The minimal engine design can limit advanced features, like multi-level physics or continuous object dynamics. Researchers needing advanced interactions might require expansions or different simulators.  
- **Performance / Speed**: Pure Python code can be slower than C++-based simulators for large-scale experiments. The authors note the trade-off for easier extensibility.  
- **Long-Horizon Goals**: Many tasks revolve around short navigation or single-step object usage. More advanced hierarchical tasks might need custom expansions, although the library’s flexible generation does help.  
- **Realistic Noise**: By default, transitions are deterministic (Minigrid) or simplified 3D (Miniworld). Additional design is needed to incorporate partial random dynamics or complex environment stochastics.  
