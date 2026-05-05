### 3.1 Markov Decision Processes

The learning problem was formulated as an episodic Markov decision process (MDP). At time step \(t\), the agent received observation \(o_t\in\mathcal{O}\), sampled action \(a_t\in\mathcal{A}\) from stochastic policy \(\pi_\theta(a\mid o_t)\), transitioned according to environment dynamics, and received extrinsic reward \(r_t^{\mathrm{ext}}\). The policy objective was to maximize expected discounted return over trajectories induced by interaction with the environment {{CIT:19}}.

This formulation was applied consistently across benchmark tasks so that algorithmic differences were attributable to exploration strategy rather than to changes in the base control problem definition.
