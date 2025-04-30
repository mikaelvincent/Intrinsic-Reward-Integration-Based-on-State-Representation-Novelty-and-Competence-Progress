MuJoCo: A physics engine for model-based control

> **Link**: <https://doi.org/10.1109/IROS.2012.6386109>

> **Parenthetical**: (Todorov et al., 2012)
> **Narrative**: Todorov et al. (2012)

---

## Notes

### Selected Direct Quotes, Formulas, and Data

Below are quotations and paraphrased formulas preserving the article’s essential details. All text directly quoted retains spelling and punctuation from the source.

1. **Context and Motivation**

   > “Before presenting our work, we briefly discuss the requirements for controller design software. First and foremost, such software should be based on a suitable mathematical and algorithmic foundation. [...] In the context of robotic control, numerical optimization is the most powerful and generally applicable tool for automating processes that would otherwise require human intelligence.”

   - The authors argue that advanced robotic hardware warrants new software that supports *automatic controller design* through numerical optimization.  
   - “We needed a physics engine representing the system state in joint coordinates and simulating contacts in ways that are related to LCP but better.”

2. **Overview of MuJoCo**

   > “Thus the name MuJoCo– which stands for Multi-Joint dynamics with Contact. We developed several new formulations of the physics of contact [11], [12], [10] and implemented the resulting algorithms in MuJoCo. [...] We have decided to provide multiple mechanisms for modeling contact dynamics, and allow the user to select the one most suitable for a given system.”

   - **Target**: Speed and accuracy for *model-based control* (in contrast to approximate or game-oriented engines).  
   - **Focus**: Large numbers of rapid dynamics evaluations, crucial for tasks like trajectory optimization, reinforcement learning, or “de novo” controller synthesis.  
   - **Advantages**: 
     - Generalized coordinates;  
     - Efficient contact simulations using advanced velocity-stepping approaches;  
     - High-level or XML-based model specification, compiled into an optimized data structure for runtime.

   > “We already used the engine in a number of control applications. It will soon be made publicly available.”

3. **Algorithms and Numerical Foundation**

   The authors detail the engine’s *smooth multi-joint dynamics* and *contact solver algorithms*:

   - **State Representation**:  
     They use generalized coordinates \(\mathbf{q}\), \(\mathbf{v}\), with quaternions for 3D orientation. The inertia matrix \(\mathbf{M}\) is always invertible in generalized coordinates.

   - **Smooth Dynamics** (no contacts):  
     - \(\mathbf{M}(\mathbf{q}) \dot{\mathbf{v}} = \mathbf{b}(\mathbf{q}, \mathbf{v}) + \boldsymbol{\tau}\).  
     - Computed via “Composite Rigid Body (CRB)” for the inertia matrix and “Recursive Newton Euler (RNE)” for bias forces \(\mathbf{b}\).  

   - **Contact Simulation**:  
     The system adopts a **discrete velocity-stepping scheme**. Constraints appear as impulses \(\mathbf{f_C}\) in a discrete-time setting. The main steps each timestep:

     1. Compute forward kinematics, detect collisions, construct Jacobians.  
     2. Compute \(\mathbf{M}, \mathbf{b}\) (via CRB, RNE).  
     3. Solve equality constraints \(\boldsymbol{\phi}(\mathbf{q})=0\) if any.  
     4. Solve for contact impulses \(\mathbf{f_C}\) using specialized new solvers.  
     5. Integrate velocity and position.

   - **Contact Solvers**:  
     1. **Implicit Complementarity Solver**  
        > “Based on [11]. It aims to find an exact solution to (3,4,5). [...] The approach is a customized non-smooth Newton method.”  
        Minimizes residual between \(\mathbf{A f_C} + \mathbf{v_0} - \mathbf{v_C} = 0\) subject to friction constraints.

     2. **Convex Solver**  
        > “Defines a kinetic energy in contact space and solves a convex optimization problem... The friction cone is a hard constraint, while non-penetration is enforced with a cost \(\theta(\mathbf{v_C})\).”  
        Yields smooth, invertible contact dynamics—useful for control optimization.

     3. **Diagonal Solver**  
        A simpler, faster but less accurate approach. Acts like “mass-aware spring-dampers” in the contact space.  
        > “If we have access to the diagonal of \(\mathbf{A}\) we can tune spring-dampers online and always have critically-damped springs at contacts.”

4. **Implementation Details and Complexity**

   - The engine can compute forward dynamics (\(\mathbf{v}^{t+\Delta t}\)) or inverse dynamics (\(\boldsymbol{\tau}\)) with contacts.  
   - **Complexity**:  
     \(\mathbf{M}\) factorization is \(\mathcal{O}(n^3)\), contact solver is \(\mathcal{O}(k^3)\) for \(k\) contacts, etc.  
     > “However, counting the number of floating point operations used to be essential when floating point arithmetic was slow, but now the bottleneck is in memory access. The only way to assess performance reliably is to run extensive timing tests.”

5. **Modeling Approach**

   - Models can be built in a custom XML format (MJCF), or in code via a C++ API. The engine compiles these into an optimized C data structure.  
   - Bodies, joints, geoms, and constraints are described. Contacts occur between geoms.  
   - Tendons can wrap around geoms; actuators can include muscle or pneumatic dynamics.

6. **Timing and Benchmark Results**

   - Comparison with SD/FAST (no contacts):  
     > “Single-threaded MuJoCo is comparable to SD/FAST. [...] We have found the differences to be within the margin of round-off errors.”  
     They achieve ~130,000 to 150,000 dynamics evaluations per second on 30–34 DOF models.

   - Overall Performance in Trajectory Optimization:  
     The authors tested a 3D humanoid (18 DOFs, 30 timesteps) plus contact points on the feet in a direct trajectory optimization procedure.  
     > “We are able to run nearly 400,000 evaluations per second including contact dynamics on a single desktop machine. With fewer active contacts the speed is much higher.”

   > “We used an interior-point method for solving the convex optimization problem. Our new projected methods appear to be faster, although we have not yet done careful testing.”

7. **Examples and Applications**

   - The authors show usage in tasks like biped locomotion, ball dropping, multi-object contact, anthropomorphic finger design, etc.  
   - They emphasize that the approach is fast enough for model-based RL or direct trajectory optimization that needs 100,000s of dynamics evaluations.

8. **Conclusions and Future Work**

   > “MuJoCo was developed to enable our research in model-based control. [...] The code is thread-safe and is already multi-threaded. The next step is to implement a cluster version, where a central dispatcher will send subsets of states to individual machines. [...] GPU versions as well as additional functionality regarding numerical optimization will be released subsequently.”

   - Free for non-profit research.  
   - The authors highlight potential expansions to multi-machine or GPU acceleration and deeper integration with numerical optimization tools.

---

## Concise Summary of the Article

Todorov, Erez, and Tassa introduce **MuJoCo** (*Multi-Joint dynamics with Contact*), a physics engine designed explicitly for *model-based control* and high-performance robotics applications. Unlike many prior engines:

- It **represents dynamics in generalized coordinates**, allowing more accurate and efficient simulation of multi-joint systems without numerically enforcing joint constraints in Cartesian space.  
- It provides **novel contact solvers** (implicit complementarity, convex, diagonal) for velocity-stepping approaches, avoiding the stiffness and inaccuracies of spring-damper contact models.  
- A built-in compiler transforms a high-level XML or C++ model description into a runtime structure optimized for fast computation.  
- The engine can compute both **forward** and **inverse** dynamics, even with contacts, enabling direct usage in model-based controllers, trajectory optimization, and advanced reinforcement learning tasks.

Through extensive timing tests, the authors demonstrate that MuJoCo is *comparable* to SD/FAST for multi-joint (smooth) dynamics, while also handling *contacts* in a way that remains both accurate and significantly faster than typical game-oriented engines (like ODE). On a desktop machine with 12 cores, they achieve around **400,000** forward dynamics evaluations per second for a 3D humanoid with contacts. This high throughput is crucial for optimization-based control or sampling-based methods needing huge numbers of simulation calls.

MuJoCo’s **unique features** include:

- Efficient usage of sparse inertia factorizations;  
- Velocity-level impulse-based contact solvers with friction constraints;  
- A modeling system that supports tendons, complex actuators, joints, and optional user-defined constraints;  
- Thorough support for parallel or multi-machine usage.

**Conclusion**: The authors highlight that MuJoCo is both a *research tool* and a *platform for advanced model-based RL*. They plan to release it publicly, integrate GPU/cluster versions, and expand numerical optimization features. The paper’s results illustrate that accurate physics simulation for complex, contact-rich robotics can be *thousands* of times faster than real-time, making large-scale, automated controller design feasible.

---

## Relevance to "Adaptive Curiosity for Exploration in Partially Random Reinforcement Learning Environments"

- **Simulation Requirements**: Adaptive curiosity algorithms often require *massive parallel rollouts* or repeated state sampling to evaluate intrinsic rewards (e.g. novelty, information gain). A *fast and stable physics engine* like MuJoCo can greatly accelerate these algorithms, especially in contact-rich or high-DOF tasks.  
- **Model-Based RL**: The authors emphasize “model-based control,” which in a partially random environment might include learning environment dynamics or performing lookahead. A reliable and efficient dynamics simulator can facilitate *sample-based planning* or *internal rollouts* integral to curiosity-driven exploration.  
- **Partially Random**: While the article does not directly focus on exploration or curiosity signals, the engineering design (fast contact simulation, parallelization) is highly pertinent for large-scale reinforcement learning research where partial randomness is standard.  
- **Conclusion**: MuJoCo is not a direct method for curiosity or exploration, but it is a powerful *platform* that such methods can exploit.

Hence, the article is **relevant** in contexts where advanced curiosity-based RL needs a high-performance simulation environment, enabling the large numbers of evaluations typical of exploration-driven tasks.

---

## Is the Paper Worth Citing?

**Yes.** It is a foundational reference in the field of robotics simulation and model-based RL for these reasons:

1. **Technical Merit**: Defines key algorithms (implicit complementarity, convex solver) that avoid pitfalls of earlier engines.  
2. **Benchmark for Performance**: Demonstrates surprisingly high simulation rates for contact-rich systems.  
3. **Impact**: MuJoCo has become widely used in RL research, e.g. for continuous-control benchmarks (Humanoid, Ant, etc.) in open-source frameworks.

---

## Potential Influence on Future Work

1. **Combining High-Performance Simulation with Curiosity**: Researchers can incorporate MuJoCo in large-scale curiosity-driven RL or model-based exploration, exploiting its speed for *massive trajectory sampling* or *iterative improvements*.  
2. **GPU / Cluster Integration**: The planned GPU-based extension might enable real-time or faster-than-real-time exploration with *thousands* of parallel rollouts, accelerating partially random environment research.  
3. **Advanced Contact and Actuation**: MuJoCo’s flexible modeling of contact constraints and muscle/pneumatic actuators can help investigations into physically realistic curiosity tasks (like complex robotic hands or humanoid locomotion).  
4. **Inverse Dynamics**: The robust inverse dynamics solver, even with contacts, could be leveraged in *inverse RL* or in skill learning approaches that rely on computing “target torques” from desired motion patterns.

---

## Open Questions or Possible Critiques

- **Non-Physical Exploits**: The authors note that if a physics engine “allows cheating,” numerical optimizers might exploit it, producing unrealistic solutions. MuJoCo’s advanced contact modeling reduces but may not fully eliminate such exploits.  
- **Hyper-Parameter Tuning**: Tuning contact solver parameters and regularization \(\mathbf{R}\) for large or complex scenes might remain tricky.  
- **Parallel GPU Implementation**: The paper mentions future GPU acceleration but does not present experimental results. Actual performance in large distributed systems remains an open area.  
- **Generalization to Real Hardware**: While MuJoCo is highly accurate for simulation, the reality gap in partially random real environments might still require domain adaptation methods. Integration with hardware remains a separate challenge.  
- **Large N-Body**: The paper focuses mainly on moderately sized manipulator or humanoid tasks. How performance scales to massive multi-object scenes or granular media is open-ended.
