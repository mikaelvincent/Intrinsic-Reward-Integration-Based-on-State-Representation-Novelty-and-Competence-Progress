### 3.1 Markov Decision Processes

The control problem was formulated as an episodic Markov decision process (MDP), where the agent interacted with an environment over discrete time steps. At time step t, the policy received an observation o_t, sampled an action a_t from a stochastic policy π_θ(a|o), transitioned to a new observation, and received an extrinsic reward r_t^ext. The objective of this formulation is to maximize expected discounted return over trajectories induced by the policy and environment dynamics [19].

This MDP formulation was used consistently across the benchmark environments in the repository. A shared formalization allowed exploration methods to be compared under the same policy optimization backbone and environment-defined reward structure.
