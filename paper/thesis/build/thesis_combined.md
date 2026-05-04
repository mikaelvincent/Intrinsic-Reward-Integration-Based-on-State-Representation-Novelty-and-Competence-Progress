## Gated Learning-Progress Exploration

## Abstract

Intrinsic-reward exploration has been used to improve reinforcement learning performance when extrinsic feedback is sparse, delayed, or weakly informative. Existing novelty-driven and prediction-error-driven methods can over-prioritize transitions in high-uncertainty regions where model error remains high but policy-relevant learning progress is limited. To address this limitation, a Gated Learning-Progress Exploration framework was designed and evaluated under a shared Proximal Policy Optimization backbone.

The framework combined a feature-space impact signal with a region-local learning-progress signal computed from short-horizon and long-horizon exponential moving averages of forward-model prediction error within an online partition of latent feature space. Two variants were evaluated: GLPE (no gate) and gated GLPE. The gated variant suppressed intrinsic shaping in regions that remained high-error and low-progress, with the objective of reducing unproductive curiosity.

Evaluation was conducted on MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5, with comparisons against Vanilla PPO, ICM, RND, RIDE, and RIAC. Results indicated that GLPE (no gate) remained competitive with strong baselines across the benchmark suite, while gated GLPE was most beneficial in sparse-reward settings where ungated intrinsic rewards could destabilize training. Step-normalized and wall-clock-normalized analyses further indicated that the proposed framework retained practical training efficiency while preserving a clear learning-progress interpretation of intrinsic reward design.

## 1. Introduction

Deep reinforcement learning performs effectively when extrinsic rewards are dense and informative, but performance degrades when rewards are sparse, delayed, or weakly aligned with early exploration behavior (Barto, 2012; Singh et al., 2005). Intrinsic motivation methods addressed this issue by augmenting task rewards with auxiliary signals that encouraged exploration when external feedback was limited (Oudeyer, 2007; Oudeyer et al., 2007; Singh et al., 2005).

Existing intrinsic objectives include count and density based novelty, information gain, prediction error, and impact driven signals (Baranes & Oudeyer, 2009; Bellemare et al., 2016; Burda, Edwards, Storkey, et al., 2018; Houthooft et al., 2016; Ostrovski et al., 2017; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Tang et al., 2016). These approaches improved exploration in many settings, but they also showed a recurring failure mode in which high novelty or prediction error persisted in regions that did not support policy improvement. This behavior is commonly described as unproductive curiosity and is particularly problematic in sparse reward tasks (Mavor-Parker et al., 2021).

Learning progress based exploration offered a complementary criterion. Under this view, experience is useful when predictive performance improves over time, not only when transitions are surprising (Oudeyer et al., 2007; Schmidhuber, 1991). This perspective motivated mechanisms that identify regions where model learning is active and distinguish them from regions where error remains high but progress is minimal.

The present work implemented and evaluated Gated Learning Progress Exploration (GLPE), including a gated variant and a non gated variant, with a shared Proximal Policy Optimization backbone. The intrinsic score combined feature space impact and region local learning progress estimated from short and long horizon prediction error trends in an online latent space partition. The gated variant suppressed intrinsic shaping in persistently high error and low progress regions, while the non gated variant preserved the same base score without suppression.

Evaluation was conducted on MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5. Comparisons were performed against Vanilla PPO, ICM, RND, RIDE, and RIAC using a common training and evaluation protocol. Performance was analyzed using both step normalized and wall clock normalized criteria to capture exploration effectiveness and practical computational cost.

### 1.1 Rationale of the Study

Exploration remains a central challenge in reinforcement learning because data collection decisions directly affect convergence speed, policy quality, and training stability when external rewards are limited (Barto, 2012; Oudeyer, 2007). Novelty and prediction error based intrinsic rewards can accelerate discovery, but these signals may remain high in stochastic or poorly modeled regions that contribute little to long term task improvement (Burda, Edwards, Storkey, et al., 2018; Mavor-Parker et al., 2021; Pathak et al., 2017).

Learning progress provides a more selective criterion by prioritizing regions where predictive capability is improving (Oudeyer et al., 2007; Schmidhuber, 1991). However, practical application in high dimensional deep RL requires a mechanism that localizes progress, remains computationally lightweight, and integrates with standard policy optimization.

The study was motivated by this methodological need. GLPE was designed to combine representation change sensitivity, region local progress estimation, and optional suppression of unproductive intrinsic shaping through a simple gate. This design targeted unproductive curiosity while preserving compatibility with PPO based training.

The rationale also included an evaluation concern. Step based return alone does not fully represent method utility in real training pipelines. For this reason, the study assessed both environment step performance and wall clock performance, together with thresholded reliability summaries across benchmark tasks.

#### 1.2.1 General Objective

To design, implement, and evaluate a learning progress aware intrinsic reward framework for deep reinforcement learning that reduces unproductive curiosity while maintaining competitive exploration performance across representative control environments.

#### 1.2.2 Specific Objectives

1. To formulate an intrinsic reward score that combines feature space impact and region local learning progress from online latent space partitioning and forward model error trends.
2. To implement GLPE and GLPE (no gate) within a shared PPO training pipeline and aligned model architecture.
3. To define a region specific gating mechanism that suppresses intrinsic shaping in persistently high error and low progress regions, and to compare it with the non gated variant.
4. To compare the proposed variants with Vanilla PPO, ICM, RND, RIDE, and RIAC under consistent training budgets, evaluation checkpoints, and multi seed aggregation.
5. To evaluate performance using learning curves, step normalized AUC, thresholded reliability, intrinsic reward dynamics, and wall clock normalized AUC.

### 1.2 Statement of the Problem

Many intrinsic motivation methods improved exploration, but their reward signals were not always aligned with actual learning progress in sparse reward or high variance environments (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Mavor-Parker et al., 2021; Raileanu & Rocktäschel, 2020). Agents could therefore spend substantial interaction budget on transitions that remained surprising without producing sustained policy gains.

This thesis addressed the problem of constructing an intrinsic reward mechanism that preserves exploratory behavior while reducing unproductive curiosity, and of evaluating that mechanism against established baselines under both sample efficiency and wall clock efficiency criteria.

Specifically, the study examined whether combining feature space impact with region local learning progress, with optional region specific gating, can provide reliable and competitive performance across sparse and dense reward benchmarks under a common PPO backbone.

### 1.3 Significance of the Study

For reinforcement learning research, the study provided an empirical formulation of intrinsic shaping that linked representation change with localized model improvement, extending learning progress oriented exploration to a modern on policy deep RL setting (Oudeyer et al., 2007; Schmidhuber, 1991).

For method developers, the GLPE framework offered a practical design that integrates with PPO based pipelines without requiring privileged environment state, while preserving interpretable components for analysis of exploration behavior.

For evaluation practice, the study demonstrated the importance of combining step based metrics with wall clock analysis and reliability thresholds, which supported a more complete assessment of exploration methods in realistic training workflows.

For undergraduate computer science research, the study presented a reproducible case of translating intrinsic motivation theory into an implemented algorithm, controlled experiments, and critical comparative analysis.

### 1.4 Scope and Limitations of the Study

The study focused on intrinsic reward design for on policy deep reinforcement learning with a shared PPO backbone. The proposed methods were limited to GLPE and GLPE (no gate), which used the same base intrinsic score with and without region specific gating.

The experimental scope was restricted to MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5, with fixed environment rewards and termination settings. Baseline comparisons were limited to Vanilla PPO, ICM, RND, RIDE, and RIAC under aligned training budgets, checkpoint schedules, and deterministic offline evaluation from saved checkpoints.

The intrinsic formulation depended on learned latent representations, forward and inverse dynamics components, online region partitioning, and exponential moving average statistics for progress estimation. Therefore, findings were bounded by the selected model classes, hyperparameter settings, and implementation configuration used in this project.

Computational analysis was conducted in the project execution environment. Wall clock results reflected the recorded runtime components under common time budgets, so absolute timings may vary across hardware or software stacks.

The study did not claim policy invariance for intrinsic shaping terms. Conclusions were interpreted empirically through returns, reliability at selected thresholds, intrinsic reward behavior, and measured computational overhead (Ng et al., 1999).

## 2. Review of Related Literature

This chapter reviews prior literature on intrinsic motivation for reinforcement learning and establishes the conceptual basis of the GLPE family examined in this thesis. The discussion is organized into five themes: intrinsic motivation foundations, novelty and prediction-error methods, learning-progress based exploration, impact-driven exploration, and reward shaping with policy invariance constraints.

Prior studies consistently reported that intrinsic rewards improved exploration when extrinsic feedback was sparse or delayed (Barto, 2012; Oudeyer, 2007; Oudeyer et al., 2007; Singh et al., 2005). At the same time, multiple works identified a recurring limitation, wherein exploratory behavior was attracted to transitions that remained surprising but did not improve task learning (Mavor-Parker et al., 2021; Raileanu & Rocktäschel, 2020). This limitation motivated approaches that evaluate not only surprise, but also whether predictive competence improves over time, which is the core principle of learning progress (Baranes & Oudeyer, 2009; Schmidhuber, 1991).

The reviewed literature therefore indicated a gap between broad exploratory drive and sustained usefulness of collected experience. The GLPE formulation addressed this gap by combining representation-level impact with region-local learning progress, and by introducing an optional region-wise gate to suppress persistently unproductive intrinsic shaping (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020).

### 2.1 Intrinsic Motivation in Reinforcement Learning

Intrinsic motivation in reinforcement learning refers to internally generated reward signals that complement environment rewards during policy optimization (Barto, 2012; Singh et al., 2005). In sparse-reward settings, such auxiliary signals were used to encourage exploration before reliable extrinsic feedback became available (Oudeyer, 2007; Oudeyer et al., 2007).

Early formulations described intrinsic behavior as seeking experiences that improve predictive competence rather than maximizing immediate external payoff (Schmidhuber, 1991; Singh et al., 2005). Later taxonomies grouped intrinsic methods into families such as novelty seeking, prediction-error curiosity, information gain, and competence or progress based objectives (Badia et al., 2020; Oudeyer, 2007; Oudeyer et al., 2007).

In deep reinforcement learning, intrinsic rewards were commonly implemented as additive shaping terms combined with extrinsic reward through a task-dependent coefficient (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020). This formulation was practical and often effective, but it generally did not preserve policy invariance because the shaping term could change trajectory preferences during optimization (Ng et al., 1999). For this reason, intrinsic methods were typically assessed empirically using sample efficiency, final return, and reliability across random seeds (Raileanu & Rocktäschel, 2020; Schulman et al., 2015; Schulman et al., 2017).

The literature established two observations relevant to this thesis. First, intrinsic rewards often improved early exploration and learning speed (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020). Second, intrinsic objectives could remain active in regions where surprise stayed high after useful learning had saturated, creating a mismatch between exploration pressure and task progress (Mavor-Parker et al., 2021). These observations motivated the present focus on progress-sensitive intrinsic shaping.

### 2.2 Novelty and Prediction-Error Methods

A major line of exploration research rewarded novelty in rarely visited or weakly modeled states. Count-based methods formalized this idea through visitation frequencies and pseudo-counts, including density-model extensions for high-dimensional observations (Bellemare et al., 2016; Ostrovski et al., 2017; Tang et al., 2016). Episodic reachability-based curiosity provided a related mechanism by rewarding experiences that expanded short-horizon behavioral coverage (Savinov et al., 2018).

Prediction-error curiosity provided a complementary strategy by rewarding transitions that were difficult for a learned forward model to predict (Pathak et al., 2017; Stadie et al., 2015). Feature-space formulations, including ICM, operationalized novelty through model mismatch in learned representations (Pathak et al., 2017). Random Network Distillation used prediction error against a fixed random target network to produce a scalable novelty signal (Burda, Edwards, Storkey, et al., 2018). Related approaches included ensemble-disagreement and directed exploration variants (Badia et al., 2020; Pathak et al., 2019).

The common strength of novelty and prediction-error methods was broad exploratory pressure with limited environment-specific engineering (Bellemare et al., 2016; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017). The common weakness was sensitivity to stochastic or weakly learnable dynamics, where prediction error could remain high without corresponding task progress (Mavor-Parker et al., 2021; Raileanu & Rocktäschel, 2020). This failure mode is often described as unproductive curiosity, and the noisy-TV effect is a representative example (Mavor-Parker et al., 2021).

These findings were directly relevant to this thesis. They indicated that high surprise alone was not a sufficient criterion for useful exploration, and they motivated augmentation of novelty-oriented signals with explicit estimates of local model improvement over time (Baranes & Oudeyer, 2009; Schmidhuber, 1991).

### 2.3 Learning-Progress Based Exploration

Learning-progress exploration was motivated by the view that intrinsically valuable experience is experience that improves predictive performance, rather than experience that is only difficult (Schmidhuber, 1991). Classical formulations tracked reductions in prediction error over time, often by comparing short-horizon and long-horizon competence statistics within local regions of the state space (Baranes & Oudeyer, 2009; Oudeyer et al., 2007).

R-IAC is a representative method in this family. It partitioned the space adaptively and prioritized regions with active competence improvement, while reducing emphasis on regions that were already mastered or persistently unpredictable (Baranes & Oudeyer, 2009). This mechanism addressed a central limitation of purely novelty-driven exploration by introducing a temporal notion of utility.

The literature also identified practical challenges when scaling progress-based ideas to modern deep reinforcement learning. Progress estimates depend on how locality is represented in high-dimensional observation spaces, and the resulting signals can be unstable without smoothing and normalization. In addition, behavior can still degrade when regions maintain high error but negligible progress over long intervals (Baranes & Oudeyer, 2009).

These limitations informed the GLPE design. The framework estimated region-local progress in latent feature space through online partitioning and exponential moving averages, then combined this signal with feature-space impact to preserve exploratory coverage while prioritizing learnable regions (Baranes & Oudeyer, 2009).

### 2.4 Impact-Driven Exploration

Impact-driven exploration rewarded transitions that produced substantial change in the agent's learned representation, rather than rewarding novelty alone (Raileanu & Rocktäschel, 2020). Under this perspective, useful exploration is associated with controllable interaction that moves behavior into distinct states.

RIDE operationalized this principle through feature-space displacement and visitation-based modulation, reducing repeated reward from revisiting similar states (Raileanu & Rocktäschel, 2020). This approach was relevant in settings where novel observations were not controllable or not informative for policy improvement.

The impact perspective complemented both novelty and learning-progress approaches. Novelty promoted broad coverage, learning progress prioritized regions with improving models, and impact emphasized controllable state change (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020; Schmidhuber, 1991). This complementarity motivated hybrid intrinsic objectives.

The GLPE family adopted impact as one component of its intrinsic score and combined it with region-local learning progress. This combination was intended to preserve movement toward behaviorally meaningful transitions while reducing emphasis on high-error regions that did not exhibit sustained model improvement.

### 2.5 Reward Shaping and Policy Invariance

Reward shaping modifies optimization signals to accelerate learning, but shaping terms can alter policy preferences when theoretical constraints are not satisfied (Ng et al., 1999). The policy-invariance result of Ng, Harada, and Russell showed that only potential-based shaping guarantees preservation of optimal policies under reward transformation (Ng et al., 1999).

Most intrinsic rewards used in deep reinforcement learning are not potential-based in this strict sense, because they depend on nonstationary predictive models, visitation statistics, or representation dynamics (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020). Consequently, these methods are generally treated as heuristic objectives that must be validated empirically.

This theoretical context was central to the present study. The GLPE intrinsic term was applied as additive shaping during PPO training, with clipping and scheduling controls, and no claim of policy invariance was made. Evaluation therefore emphasized empirical outcomes, including step efficiency, wall-clock efficiency, thresholded reliability, and final extrinsic return.

### 2.6 Synthesis and Research Gap

The reviewed literature showed that intrinsic motivation can improve exploration when extrinsic rewards are sparse or delayed (Barto, 2012; Oudeyer, 2007; Oudeyer et al., 2007; Singh et al., 2005). It also showed that novelty and prediction-error bonuses can become misaligned with task progress when persistent stochasticity or model mismatch sustains high surprise (Burda, Edwards, Storkey, et al., 2018; Mavor-Parker et al., 2021; Pathak et al., 2017).

Learning-progress methods addressed part of this issue by prioritizing regions where predictive competence improved over time (Baranes & Oudeyer, 2009; Schmidhuber, 1991). Impact-driven methods added a complementary signal that favored transitions associated with meaningful state change (Raileanu & Rocktäschel, 2020). However, existing approaches did not fully resolve the combined requirement of maintaining broad exploration while suppressing intrinsically attractive but persistently unproductive regions in a lightweight on-policy setting (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020).

Based on this gap, this thesis focused on a combined intrinsic formulation that integrated feature-space impact and region-local learning progress, with an optional region-specific gate for high-error, low-progress regions. This direction remained consistent with the problem statement, scope, and evaluation design by testing the formulation against established baselines under a shared PPO backbone using both sample-based and wall-clock criteria.

## 3. Technical Background

This chapter presents the theoretical and algorithmic background used by the study. The discussion covers Markov decision processes, the reinforcement learning objective, policy optimization with PPO, variance reduction with GAE, intrinsic reward design, latent dynamics learning, online region partitioning, and evaluation metrics. These concepts establish the foundation for the GLPE and GLPE (no gate) formulations described in the methodology chapter and for the comparative analysis against PPO, ICM, RND, RIDE, and RIAC baselines (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Schulman et al., 2015; Schulman et al., 2017).

### 3.1 Markov Decision Processes

The learning problem was formulated as an episodic Markov decision process (MDP), represented by states or observations, actions, transition dynamics, and rewards. At each time step t, an observation \(o_t\) was received, an action \(a_t\) was sampled from a stochastic policy \(\pi_\theta(a\mid o)\), and an extrinsic reward \(r_t^{\mathrm{ext}}\) was returned by the environment. The objective of this formulation was to maximize the expected discounted return over trajectories generated by policy-environment interaction (Schulman et al., 2015; Schulman et al., 2017).

This MDP framing was used across all benchmark tasks in the repository, including discrete control and continuous control domains. A shared formalization allowed direct comparison of exploration methods under the same PPO backbone and the same environment-defined reward functions (Schulman et al., 2017).

### 3.2 Reinforcement Learning Objective

In policy-gradient reinforcement learning, parameters are updated to maximize expected return under the current policy distribution. The study used an augmented per-transition reward,
\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}),
\]
where \(r_t^{\mathrm{int}}\) denotes intrinsic reward, \(\eta_t\) controls intrinsic strength, and \(r_{\max}\) bounds intrinsic magnitude. This formulation is consistent with reward shaping practices that preserve task-directed optimization while improving exploration behavior (Ng et al., 1999).

For GLPE-family methods, intrinsic weight was optionally annealed by a cosine schedule over training progress, so intrinsic guidance was emphasized in earlier phases and reduced later when exploitation became more important. Intrinsic rewards were set to zero on environment-terminal transitions to avoid dependence on termination artifacts (Schulman et al., 2017).

### 3.3 Proximal Policy Optimization

Proximal Policy Optimization (PPO) is an on-policy actor-critic method that stabilizes policy updates through clipped probability-ratio objectives. The clipping mechanism constrains update size, which reduces destructive policy shifts while preserving sample-efficient gradient-based improvement (Schulman et al., 2017).

The repository implementation used PPO as the common reinforcement learning backbone for all compared methods. Transition batches were collected with vectorized environments, advantages were computed from rollout data, and multiple shuffled minibatch epochs were used per update. Shared PPO settings across methods isolated the effect of intrinsic objective design rather than changes in the optimizer itself (Schulman et al., 2017).

### 3.4 Generalized Advantage Estimation

Generalized Advantage Estimation (GAE) provides a bias-variance tradeoff for policy-gradient updates by exponentially weighting temporal-difference residuals. Compared with single-step estimators, GAE generally reduces variance in advantage estimates and improves optimization stability in continuous control settings (Schulman et al., 2015).

In the study pipeline, GAE was applied to rewards after intrinsic augmentation when intrinsic methods were enabled. Bootstrapping behavior for time-limit truncations followed the available final-observation signal in the logged rollouts, which maintained consistent target construction across methods (Schulman et al., 2015; Schulman et al., 2017).

### 3.5 Intrinsic Rewards

Intrinsic rewards were used to complement sparse or delayed extrinsic feedback by assigning additional utility to exploratory transitions. Prior approaches include prediction-error curiosity, random-network disagreement, impact-driven exploration, and region-based competence progress (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020).

The study adopted a composite intrinsic structure built from two components: feature-space impact and region-local learning progress. Impact measured representation change across successive observations, while learning progress captured recent reduction in local forward-model error relative to a slower baseline. Component scales were normalized online with running RMS statistics before weighted combination, which reduced sensitivity to task-dependent magnitude differences. The resulting intrinsic signal was then clipped and scaled before addition to extrinsic reward (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020; Schulman et al., 2017).

Two variants were considered. GLPE (no gate) used the composite score directly. GLPE applied an additional region-specific binary gate that suppressed intrinsically attractive but persistently unproductive regions according to robust global thresholds and hysteretic reactivation conditions (Baranes & Oudeyer, 2009; Schulman et al., 2017).

### 3.6 Latent Dynamics Models

A latent dynamics module was used to produce intrinsic quantities from learned features rather than from privileged state variables. An encoder \(\phi_\omega\) mapped observations to latent vectors \(z_t\), a forward model \(f_\psi\) predicted \(z_{t+1}\) from \((z_t,a_t)\), and an inverse model \(g_\xi\) predicted action information from \((z_t,z_{t+1})\). Training minimized a weighted sum of forward and inverse losses (Pathak et al., 2017; Schulman et al., 2017).

Per-transition forward prediction error,
\[
e_t = \frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2,
\]
was treated as the core signal for learning-progress tracking. This design aligned with established curiosity frameworks, where representation learning and predictive modeling jointly shape exploratory behavior (Pathak et al., 2017; Raileanu & Rocktäschel, 2020).

### 3.7 Online Region Partitioning

Learning progress was localized through an online partition of latent space. The partition was represented by a binary tree whose leaves defined adaptive regions. As embeddings accumulated in a leaf, splitting was triggered by capacity and depth criteria, and split rules were selected from coordinate variance with median thresholding to avoid degenerate partitions (Baranes & Oudeyer, 2009; Schulman et al., 2017).

Each region maintained short-horizon and long-horizon exponential moving averages of prediction error. Region-local progress was defined as the positive part of the long-minus-short difference,
\[
\mathrm{LP}(r)=\max(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}),
\]
which became large when local predictive performance was improving. This mechanism adapted exploration pressure to nonstationary learning dynamics in different parts of feature space (Baranes & Oudeyer, 2009; Schulman et al., 2017).

### 3.8 Evaluation Metrics

Evaluation focused on extrinsic task performance and computational efficiency. Primary performance curves used undiscounted episodic return evaluated from offline checkpoints under deterministic action selection. Aggregation across multiple seeds provided mean trends and dispersion summaries per method and environment (Schulman et al., 2017).

Two scalar curve summaries were used. Step-AUC integrated return against environment steps and normalized by step budget, which reflected sample efficiency. Wall-clock AUC integrated return against cumulative training time under a common time budget, defined as the minimum final runtime among compared methods in the same environment. This common-budget rule avoided extrapolation beyond measured runtime and enabled fair efficiency comparison (Schulman et al., 2017).

## 4. Design and Methodology

This chapter presents the methodological design used to transform the proposed intrinsic motivation approach into an implementable and testable reinforcement learning framework. The chapter formalizes the GLPE family, including GLPE and GLPE (no gate), then details the training pipeline, experimental configuration, and statistical analysis procedures used for comparative evaluation. The methodological decisions followed the same technical scope as the source paper, with adaptation to thesis structure and documentation style (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Schulman et al., 2015; Schulman et al., 2017).

The overall design used controlled, multi-seed benchmarking with a shared PPO backbone, fixed per-environment training budgets, and common evaluation checkpoints across methods. Intrinsic-reward methods differed only in intrinsic signal construction and associated module updates, while policy optimization, observation handling, and reporting protocol were standardized to isolate the effect of intrinsic objective design (Schulman et al., 2015; Schulman et al., 2017).

### 4.1 Research Design

The study used an experimental comparative design in which two proposed methods, GLPE and GLPE (no gate), were evaluated against five baseline methods: Vanilla PPO, ICM, RND, RIDE, and RIAC (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Schulman et al., 2015; Schulman et al., 2017). The core objective was to determine whether combining feature-space impact and region-local learning progress, with or without region-specific gating, improved exploration behavior and downstream control performance under fixed training conditions.

A within-environment control strategy was applied. For each environment, all methods used the same PPO architecture, optimizer family, discounting setup, and total interaction budget. Training and evaluation seeds were aligned across methods, and deterministic evaluation actions were used at each saved checkpoint. This design reduced confounding effects from policy backbone differences and focused comparison on intrinsic reward formulation (Schulman et al., 2015; Schulman et al., 2017).

Performance was analyzed from both sample-efficiency and computational-efficiency perspectives. Sample efficiency was examined through learning curves versus environment steps, final-checkpoint return, and step-normalized area under curve. Computational efficiency was examined through wall-clock AUC and per-component runtime decomposition (Schulman et al., 2015). Reliability was further examined using threshold-based reach rates and steps-to-threshold summaries across seeds.

### 4.2 Proposed GLPE Framework

The proposed framework augmented extrinsic reward with a clipped intrinsic term,
\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}),
\]
where \(\eta_t\) controlled intrinsic strength over training and \(r_{\max}\) bounded intrinsic magnitude (Schulman et al., 2017). Intrinsic reward was set to zero on environment-terminal transitions so that shaping did not depend on episode termination.

A shared base score was computed from two components: feature-space impact and region-local learning progress. Let \(z_t=\phi_\omega(o_t)\) be the learned latent representation. The base intrinsic score was defined as
\[
u_t = \alpha_{\mathrm{impact}}\widetilde{I}_t + \alpha_{\mathrm{LP}}\widetilde{\mathrm{LP}}_t,
\]
where \(\widetilde{I}_t\) and \(\widetilde{\mathrm{LP}}_t\) were RMS-normalized components and \(\alpha_{\mathrm{impact}},\alpha_{\mathrm{LP}}\ge 0\) were mixing weights (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020).

Two variants were implemented within this shared structure. GLPE (no gate) used \(r_t^{\mathrm{int}}=u_t\). GLPE applied a binary, region-specific gate and used \(r_t^{\mathrm{int}}=g_{\rho_t}u_t\), where \(\rho_t\) denoted the assigned latent-space region for transition \(t\) (Baranes & Oudeyer, 2009). This separation preserved a common signal foundation while isolating the effect of gating behavior in comparative analysis.

### 4.3 Latent Representation and Dynamics Model

Intrinsic computation relied on a learned latent dynamics model. Observations were encoded as \(z_t=\phi_\omega(o_t)\), then used by a forward predictor \(f_\psi(z_t,a_t)\) to estimate \(z_{t+1}\), and by an inverse predictor \(g_\xi(z_t,z_{t+1})\) to infer action information (Pathak et al., 2017). The inverse model was treated as a classifier in discrete-action tasks and as a Gaussian-likelihood model in continuous-action tasks.

Training used the composite objective
\[
\mathcal{L}_{\mathrm{dyn}}(t)=\beta_{\mathrm{fwd}}\mathcal{L}_{\mathrm{fwd}}(t)+\beta_{\mathrm{inv}}\mathcal{L}_{\mathrm{inv}}(t),
\]
with positive coefficients for forward and inverse losses. The forward loss used mean squared error in latent space,
\[
\mathcal{L}_{\mathrm{fwd}}(t)=\frac{1}{d}\lVert f_\psi(z_t,a_t)-z_{t+1}\rVert_2^2,
\]
and per-transition prediction error was defined as \(e_t=\mathcal{L}_{\mathrm{fwd}}(t)\) (Pathak et al., 2017).

For vector-observation tasks in the experiment suite, the encoder used a two-layer multilayer perceptron with 256 hidden units per layer and produced a 128-dimensional latent feature. Dynamics modules were optimized with Adam at learning rate \(3\times10^{-4}\), with intrinsic-model gradient clipping at 5.0.

### 4.4 Region-Local Learning Progress

Learning progress was localized through an online binary partition tree over latent space. Each embedding \(z_t\) was routed to a leaf region \(\rho_t\). A leaf was split when it reached capacity \(C\), had depth below \(D_{\max}\), and allowed a non-degenerate partition. Split dimension selection followed highest coordinate variance, and thresholding used the coordinate median (Baranes & Oudeyer, 2009).

For each region \(r\), long-horizon and short-horizon exponential moving averages of forward prediction error were maintained,
\[
\mu_r^{\mathrm{long}}\leftarrow\beta_{\mathrm{long}}\mu_r^{\mathrm{long}}+(1-\beta_{\mathrm{long}})e_t,
\]
\[
\mu_r^{\mathrm{short}}\leftarrow\beta_{\mathrm{short}}\mu_r^{\mathrm{short}}+(1-\beta_{\mathrm{short}})e_t,
\]
for transitions assigned to region \(r\). Newly created region identifiers were initialized with \(\mu_r^{\mathrm{long}}=\mu_r^{\mathrm{short}}=e_t\) at first visit.

Region-local learning progress was defined as
\[
\mathrm{LP}(r)=\max(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}).
\]
The transition-level value used in intrinsic computation was \(\mathrm{LP}_t=\mathrm{LP}(\rho_t)\). This definition emphasized areas where recent prediction error dropped below longer-horizon baseline, which indicated active local model improvement (Baranes & Oudeyer, 2009).

### 4.5 Feature-Space Impact

The second intrinsic component measured latent-state displacement between consecutive observations,
\[
I_t=\lVert z_{t+1}-z_t\rVert_2.
\]
This term rewarded transitions that changed the learned representation, and therefore emphasized state changes that were significant in latent feature geometry rather than raw observation space (Raileanu & Rocktäschel, 2020).

To stabilize scale across environments and across training phases, component-wise RMS normalization was applied. For a scalar signal \(x_t\), a running accumulator was updated as
\[
v\leftarrow\beta_{\mathrm{rms}}v+(1-\beta_{\mathrm{rms}})x_t^2,
\]
then normalized using \(\mathrm{RMS}(x_t)=\sqrt{v+\varepsilon}\). This produced
\[
\widetilde{I}_t=\frac{I_t}{\mathrm{RMS}(I_t)}, \qquad \widetilde{\mathrm{LP}}_t=\frac{\mathrm{LP}_t}{\mathrm{RMS}(\mathrm{LP}_t)}.
\]
The normalized values reduced method sensitivity to absolute signal magnitude and supported a shared mixing rule for GLPE and GLPE (no gate).

### 4.6 Gating Mechanism

The GLPE gating mechanism was designed to suppress intrinsic shaping in regions that remained difficult to predict yet showed limited evidence of ongoing learning progress. Let \(\mathcal{R}\) denote visited regions. Robust global references were computed using medians,
\[
\mathrm{LP}_{\mathrm{med}}=\mathrm{median}_{r\in\mathcal{R}}\,\mathrm{LP}(r), \qquad e_{\mathrm{med}}=\mathrm{median}_{r\in\mathcal{R}}\,\mu_r^{\mathrm{short}}.
\]
A learning-progress threshold was defined as \(\tau_{\mathrm{LP}}=\kappa\,\mathrm{LP}_{\mathrm{med}}\), and normalized short-horizon error as
\[
s_r=\frac{\mu_r^{\mathrm{short}}}{e_{\mathrm{med}}+\varepsilon}.
\]
Region \(r\) was marked unproductive on a visit when both \(\mathrm{LP}(r)<\tau_{\mathrm{LP}}\) and \(s_r>\tau_s\) held (Mavor-Parker et al., 2021).

Each region maintained binary gate state \(g_r\in\{0,1\}\) and persistence counters. Gating was activated only after at least \(R_{\min}\) regions had been visited, so that median references were sufficiently informative. With gating active, persistence and hysteresis were enforced: an active gate was turned off after \(K\) consecutive unproductive visits, while a disabled gate was re-enabled only after two consecutive visits satisfying \(\mathrm{LP}(r)>h\tau_{\mathrm{LP}}\), with \(h>1\). If gating was inactive, gates remained enabled and counters were reset.

The final intrinsic reward for GLPE used
\[
r_t^{\mathrm{int}}=g_{\rho_t}u_t.
\]
This operation retained the same base score used by GLPE (no gate), while introducing selective suppression as a guardrail against persistent curiosity traps (Mavor-Parker et al., 2021).

### 4.7 Intrinsic Reward Scheduling

Intrinsic shaping strength was scheduled over training using a cosine taper in the GLPE family. Let \(p\in(Badia et al., 2020)\) denote training progress as fraction of total environment steps, and let \(p_{\mathrm{start}}<p_{\mathrm{end}}\) define taper interval (Barto, 2012). The schedule was
\[
w(p)=
\begin{cases}
1, & p\le p_{\mathrm{start}},\\
\tfrac{1}{2}\left(1+\cos\left(\pi\tfrac{p-p_{\mathrm{start}}}{p_{\mathrm{end}}-p_{\mathrm{start}}}\right)\right), & p_{\mathrm{start}}<p<p_{\mathrm{end}},\\
0, & p\ge p_{\mathrm{end}}.
\end{cases}
\]
The effective intrinsic coefficient became \(\eta_t=\eta\,w(p_t)\), and remained constant at \(\eta_t=\eta\) when schedule bounds were not specified.

This schedule treated intrinsic reward as a transient exploration aid, with stronger influence early in learning and reduced influence later when policy refinement depended more on extrinsic objective optimization. The same scheduling rule was used in GLPE and GLPE (no gate), preserving comparability between the two proposed variants (Schulman et al., 2017).

### 4.8 Algorithmic Workflow

The intrinsic reward workflow followed the same sequence described in the source paper: latent encoding, forward-error computation, online region assignment, region-level EMA updates, impact and learning-progress normalization, weighted intrinsic-score construction, optional gating, and PPO optimization with augmented reward.

Figure 4.1. High-level pseudocode for computing GLPE-family intrinsic rewards within one PPO update.

```text
Input: on-policy transitions {(o_t, a_t, o_{t+1})}_{t=1}^N;
       encoder phi_omega; forward model f_psi; inverse model g_xi;
       region assignment rho; region EMAs; RMS accumulators; optional gate states
Output: intrinsic rewards {r_t^int}_{t=1}^N; updated region statistics; updated intrinsic model parameters

for t = 1 to N:
    z_t <- phi_omega(o_t), z_{t+1} <- phi_omega(o_{t+1})
    e_t <- (1/d) ||f_psi(z_t, a_t) - z_{t+1}||^2
    r <- rho(z_t), including insertion and split when needed
    update short and long EMAs for region r with e_t
    LP_t <- max(0, mu_long(r) - mu_short(r))
    I_t <- ||z_{t+1} - z_t||
    normalize I_t and LP_t with running RMS
    u_t <- alpha_impact * I_t_tilde + alpha_LP * LP_t_tilde
    if gating enabled:
        compute global medians across visited regions
        update gate state with persistence and hysteresis
        r_t^int <- g_r * u_t
    else:
        r_t^int <- u_t

update intrinsic model parameters using supervised forward and inverse losses
```

### 4.9 Experimental Environment

Experiments were conducted on five Gymnasium benchmark tasks spanning sparse-reward and dense-reward control settings: MountainCar-v0, BipedalWalker-v3, Ant-v5, HalfCheetah-v5, and Humanoid-v5. The protocol used default environment rewards and termination conditions, with no domain randomization and no additional frame skipping.

Training used vectorized environments with \(B\) parallel instances and rollout length \(T\), configured so that nominal batch size per PPO update was
\[
N=B\times T=16{,}384
\]
transitions. The final update could be smaller when remaining budget was below \(N\). Environment-specific step budgets and seed counts were fixed according to the source experimental table, and all compared methods used identical per-environment seed sets.

Execution was performed under deterministic settings when supported, and timing measurements were gathered in the same execution mode used for training so that wall-clock statistics reflected end-to-end optimization overhead.


Table 4.1. Benchmark suite and training budgets.

| Environment | B | T | N | Total steps | Seeds |
|---|---:|---:|---:|---:|---:|
| MountainCar-v0 | 16 | 1,024 | 16,384 | 3,000,000 | 10 |
| BipedalWalker-v3 | 8 | 2,048 | 16,384 | 7,000,000 | 8 |
| Ant-v5 | 8 | 2,048 | 16,384 | 15,000,000 | 8 |
| HalfCheetah-v5 | 8 | 2,048 | 16,384 | 15,000,000 | 8 |
| Humanoid-v5 | 4 | 4,096 | 16,384 | 30,000,000 | 5 |

The symbol B denotes the number of parallel environment instances, T denotes rollout horizon per instance, and N = B x T denotes transitions per PPO update.

### 4.10 Baseline Methods

The proposed methods were compared against five baselines that represent established intrinsic-reward or control references: Vanilla PPO, ICM, RND, RIDE, and RIAC (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Schulman et al., 2017). Vanilla PPO optimized only extrinsic reward and served as the non-intrinsic control baseline.

ICM used forward-model prediction error in learned feature space as intrinsic reward. RND used predictor error against a fixed random target network. RIDE used feature-space impact modulated by episodic visitation counts from discretized features. RIAC used region-local learning progress from adaptive partitioning of feature space (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020).

All methods shared the same PPO backbone and policy-value architecture within each environment. Intrinsic-reward methods used a common augmented-reward form with scaling and clipping, and per-environment intrinsic scale parameters were held constant across methods to reduce reward-scale confounding in cross-method comparison (Schulman et al., 2017).

### 4.11 Training Protocol

All agents were trained with PPO and GAE using separate policy and value multilayer perceptrons with two hidden layers of width 256 and ReLU activations (Schulman et al., 2015; Schulman et al., 2017). Continuous-control policies used diagonal Gaussian outputs with action squashing to finite environment bounds when required.

Each training iteration collected up to \(N=16{,}384\) on-policy transitions, computed intrinsic rewards when applicable, set intrinsic rewards to zero on terminal transitions and specific truncation cases without final observation, then computed advantages and value targets. PPO updates were applied across shuffled minibatches for multiple epochs. Adam optimization, per-batch advantage normalization, and gradient-norm clipping at 1.0 were used for policy and value updates (Schulman et al., 2015; Schulman et al., 2017).

Vector observations were normalized online using running mean and variance, and the same normalization was applied across policy, value, and intrinsic modules. Trainable intrinsic modules were updated once per PPO iteration using the same collected on-policy batch. For methods without internal intrinsic normalization, running RMS normalization was applied to raw intrinsic output before scaling and clipping. For methods with intrinsically normalized outputs, scaling and clipping were applied directly.


Table 4.2. PPO hyperparameters by environment.

| Environment | LR | Epochs | Minibatches | Clip | Lambda | Entropy | V-clip | KL stop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MountainCar-v0 | 3.0e-4 | 10 | 16 | 0.20 | 0.95 | 0.00 | 0.00 | 0.06 |
| BipedalWalker-v3 | 5.0e-4 | 5 | 16 | 0.25 | 0.95 | 0.00 | 0.00 | 0.06 |
| Ant-v5 | 1.5e-4 | 15 | 64 | 0.20 | 0.95 | 0.00 | 0.20 | 0.04 |
| HalfCheetah-v5 | 3.0e-4 | 10 | 32 | 0.20 | 0.95 | 0.01 | 0.20 | 0.03 |
| Humanoid-v5 | 2.0e-4 | 5 | 32 | 0.20 | 0.97 | 0.01 | 0.20 | 0.03 |

Table 4.3. GLPE hyperparameters by environment.

| Environment | eta | r_max | alpha_LP | p_start | p_end | C | D_max | beta_long | beta_short | kappa | tau_s | K | R_min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MountainCar-v0 | 0.05 | 4.0 | 0.5 | 0.05 | 0.80 | 128 | 10 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 8 |
| BipedalWalker-v3 | 0.08 | 4.0 | 0.5 | 0.12 | 0.75 | 200 | 12 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 16 |
| Ant-v5 | 0.06 | 4.0 | 0.6 | 0.10 | 0.70 | 256 | 12 | 0.997 | 0.92 | 0.012 | 2.5 | 8 | 64 |
| HalfCheetah-v5 | 0.04 | 5.0 | 0.5 | 0.05 | 0.75 | 256 | 12 | 0.995 | 0.90 | 0.010 | 2.0 | 5 | 32 |
| Humanoid-v5 | 0.06 | 5.0 | 0.5 | 0.05 | 0.80 | 256 | 12 | 0.998 | 0.92 | 0.010 | 2.0 | 5 | 32 |

### 4.12 Evaluation Protocol

Evaluation used undiscounted episodic extrinsic return. Online evaluation during training was not performed. Instead, saved checkpoints were evaluated offline in separate environment instances using deterministic action selection based on distribution mode.

Each evaluated checkpoint was run for 20 episodes. Episode seeds were fixed per training seed to support consistent between-method comparison. Aggregation was performed across multiple independent training seeds per environment.

Checkpointing included step zero, additional warmup checkpoints within the initial interval, regular checkpoints at fixed fractions of total budget, and a final checkpoint at training completion. Scalar metrics were logged at fixed step intervals. This structure supported curve-level, threshold-level, and efficiency-level analyses from a common checkpoint record.

### 4.13 Statistical Analysis

Performance curves were aggregated across seeds using mean return trajectories, with uncertainty bands derived by bootstrap resampling across seeds. Scalar summaries included final-checkpoint return, step-normalized AUC, and wall-clock AUC under a common per-environment time horizon defined by the minimum final runtime among compared methods.

Thresholded reliability analysis used task-specific solved thresholds and additional reduced thresholds at 25 percent and 50 percent of solved level. For each threshold, summaries included reach rate and steps-to-threshold distribution across seeds. This analysis separated delayed success from non-attainment and was used to complement curve-level comparisons.

Runtime analysis decomposed per-iteration wall-clock into environment interaction, policy inference, intrinsic computation, intrinsic-module update, advantage computation, and PPO optimization. The decomposition was used to attribute efficiency differences and to contextualize wall-clock AUC outcomes. Additional diagnostic measurements, such as gating-median recomputation throughput, were treated as supporting implementation analysis rather than primary benchmark criteria.

### 4.14.1 Budget and Cost Management

Budget utilization was concentrated on compute infrastructure required for iterative reinforcement learning training, repeated evaluation across seeds, and generation of publication-ready outputs. Cost control emphasized workload consolidation, fixed environment budgets, and reuse of common training utilities so that experiments remained within a bounded resource envelope.

The recorded direct compute expenditure is summarized below.

| Cost Category | Amount (PHP) | Cost Management Note |
|---|---:|---|
| Cloud-based accelerated compute services for training and evaluation workloads | 41,266.87 | Usage was allocated to prioritized experiment batches aligned with the final benchmark protocol and reporting requirements. |

The cost profile was consistent with the experimental design, where multiple methods were trained under matched budgets and repeated seeds for reliable comparison.

### 4.14.2 Software Development Tools

Software development and experimentation were implemented through a Python-based research stack with explicit separation of training, evaluation, benchmarking, visualization, and testing modules in the codebase. The selected tools supported the PPO-centered pipeline, intrinsic reward modules, and benchmark environments described in prior sections (Schulman et al., 2017).

| Tool or Library | Role in the Study | Evidence in Repository |
|---|---|---|
| Python 3.10 to 3.11 runtime | Core execution environment for all scripts and modules | Project runtime constraint in code configuration  |
| PyTorch | Neural network modeling and optimization for policy, value, and intrinsic modules | Declared project dependency  |
| Gymnasium | Standardized environment interface and benchmark task execution | Declared dependency and benchmark usage alignment  |
| MuJoCo and Gymnasium MuJoCo integration | Continuous-control physics simulation for Ant, HalfCheetah, and Humanoid tasks | Optional dependency and task-level alignment  |
| NumPy | Array operations and numerical preprocessing | Declared dependency  |
| Pandas | Structured result aggregation and CSV-based summaries | Declared dependency and results artifacts  |
| Matplotlib | Figure generation for evaluation curves, timing, and ablation visualizations | Declared dependency and plot artifacts  |
| Typer | Command-line interface for experiment and utility entry points | Declared dependency  |
| PyYAML | Configuration parsing for experiment setup | Declared dependency  |
| ImageIO and imageio-ffmpeg | Video and frame export support for experiment outputs | Declared dependency and video utility modules  |
| Pillow | Image processing support for generated visual outputs | Declared dependency  |
| Pytest | Automated verification of configuration, training, evaluation, and algorithm utilities | Optional development dependency and test suite presence  |

The toolchain was selected to preserve reproducibility and maintain compatibility between research code, generated metrics, and thesis reporting artifacts.

### 4.14.3 Schedule and Timeline

Schedule management followed milestone-based progression across proposal preparation, framework implementation, controlled experimentation, result analysis, and manuscript consolidation. Timeline control prioritized completion of dependency-critical activities first, particularly implementation validation before full benchmark execution and final figure production.

| Project Phase | Timeline Description |
|---|---|
| Proposal and planning | Initial scope definition, methodological framing, and evaluation criteria alignment were completed before full implementation cycles. |
| Implementation and internal validation | Core modules for training, intrinsic reward computation, and evaluation were completed with iterative verification against configured protocols. |
| Full experimentation | Multi-seed benchmark runs were executed under fixed per-environment budgets, followed by consolidation of intermediate artifacts. |
| Analysis and manuscript integration | Quantitative outputs, plots, and interpretive discussion were synchronized with thesis chapter structure and citation requirements. |
| Final packaging and defense preparation | Document refinement, formatting checks, and presentation-aligned material preparation were completed for final submission stages. |

This structure reflected the dependency order of technical work products already represented in the repository, including source modules, benchmark outputs, and thesis-ready visual artifacts.

### 4.14.4 Responsibilities

Responsibilities were assigned according to academic requirements for project execution, supervisory coordination, and formal presentation activities. Functional ownership emphasized continuity between implementation, evaluation, documentation, and dissemination outputs.

| Role | Responsibility Profile |
|---|---|
| Mikael Vincent Tumampos | Served as primary lead for end-to-end technical execution, including framework development, experiment orchestration, result synthesis, manuscript drafting, and preparation of presentation materials used across project milestones and formal dissemination activities. |
| Ervin Joshua Guirnela | Provided secondary project support in selected communication and presentation activities, including participation in proposal-stage reporting and conference delivery, with contributions coordinated to align with finalized technical and presentation materials. |
| Christine Peña (Thesis Adviser) | Provided advisory oversight focused on institutional thesis workflow compliance, chapter organization standards, submission documentation requirements, and formatting alignment with university processes. |

This allocation supported consistent progression from implementation to reporting while maintaining conformance with academic process requirements.

### 4.14 Project Management

Project management was implemented to maintain methodological consistency across model design, experimental execution, result consolidation, and thesis integration. The management approach followed a reproducible research workflow centered on version-controlled code, fixed training and evaluation protocols, and explicit artifact generation for plots and summary tables.

Operational planning covered four areas: budget and cost management, software development tools, schedule and timeline control, and role responsibilities. These areas supported the same technical scope used in the experimental sections, particularly PPO-based training, intrinsic reward computation, and multi-environment evaluation under fixed budgets (Schulman et al., 2017).

#### 4.14.1 Budget and Cost Management

#### 4.14.2 Software Development Tools

#### 4.14.3 Schedule and Timeline

#### 4.14.4 Responsibilities

## 5. Results and Analysis

This chapter reports comparative results for GLPE, GLPE without gating, Vanilla PPO, ICM, RND, RIDE, and RIAC on the five-task benchmark suite defined in Chapter 4 (Baranes & Oudeyer, 2009; Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020; Schulman et al., 2017). Consistent with the evaluation protocol, reported task performance uses deterministic offline evaluation and extrinsic return unless explicitly stated otherwise.

The analysis is organized into curve-level behavior, integrated performance summaries, thresholded reliability, component ablation, intrinsic shaping diagnostics, gating behavior, and wall-clock efficiency. This organization follows the same experimental logic used in the source paper, while aligning with thesis chapter structure.

### 5.1 Learning Curve Performance

Learning curves versus environment steps showed that GLPE without gating tracked the strongest baseline closely across most tasks, with stable behavior across random seeds. The gated variant differed most clearly in exploration-sensitive settings. On MountainCar-v0, gating remained beneficial and supported strong upward progression. On Humanoid-v5, between-seed variance was large for all methods, and gating tended to be conservative in some runs.

On MuJoCo locomotion tasks, where extrinsic reward was denser, both GLPE variants behaved similarly and stayed within a modest gap of the strongest intrinsic baseline in the curve-level view (Burda, Edwards, Storkey, et al., 2018; Raileanu & Rocktäschel, 2020). This pattern indicated that GLPE retained competitiveness even when dense task reward reduced the relative advantage of additional exploration shaping.

The curve-level perspective also clarified that ranking differences were task-dependent rather than uniform. MountainCar-v0 favored GLPE strongly, whereas BipedalWalker-v3 and MuJoCo tasks showed closer competition among several methods.


Figure 5.1. Evaluation learning curves for GLPE and baseline intrinsic-reward methods.

![Figure 5.1: Evaluation learning curves for GLPE and baseline intrinsic-reward methods.](../resources/eval-curves-baselines-curves.png)

### 5.2 Final Performance and Step-AUC

Final-checkpoint comparisons and step-normalized AUC summarized both asymptotic quality and learning speed over fixed interaction budgets. Step-AUC values showed that GLPE achieved the highest mean value on MountainCar-v0, with GLPE equal to or near the best baseline on several other tasks but not dominant in all environments.

For BipedalWalker-v3, GLPE without gating reached a competitive step-AUC of 255.2, close to the best baseline value of 257.3 from ICM (Pathak et al., 2017). For Ant-v5 and HalfCheetah-v5, GLPE values remained below the strongest baseline means, although confidence intervals overlapped in several cases (Burda, Edwards, Storkey, et al., 2018; Raileanu & Rocktäschel, 2020). On Humanoid-v5, all methods exhibited wide uncertainty bands, and step-AUC ranking was therefore unstable under bootstrap uncertainty.

These results indicated that GLPE provided strong sample-efficiency behavior in sparse-reward settings, while remaining broadly competitive in dense-reward settings where baseline intrinsic objectives were already effective.


Table 5.1. Step-AUC of deterministic evaluation return versus cumulative environment steps.

| Environment | GLPE | GLPE (no gate) | Best baseline |
|---|---|---|---|
| MountainCar-v0 | -107.0 [-114.8,-101.8] | -111.3 [-128.7,-101.4] | RIDE: -113.7 [-134.2,-101.9] |
| BipedalWalker-v3 | 249.0 [223.9,270.7] | 255.2 [230.0,275.6] | ICM: 257.3 [229.4,278.3] |
| Ant-v5 | 3,402 (11, 67, 708) | 3,402 (11, 67, 707) | RND: 3,565 (11, 202, 876) |
| HalfCheetah-v5 | 5,005 (12, 17, 316, 708) | 4,998 (12, 17, 296, 700) | RIDE: 5,208 (17, 410) |
| Humanoid-v5 | 1,583 (11, 360, 551) | 1,665 (20, 769, 921) | ICM: 1,781 (20, 797, 829) |

### 5.3 Thresholded Reliability and Steps-to-Threshold

Thresholded analysis was used to separate delayed attainment from complete non-attainment. Solved-threshold statistics showed that both GLPE variants solved MountainCar-v0 in all seeds, each at a median of 0.35M steps, while the most reliable baseline solved 9 of 10 seeds at 0.44M steps (Raileanu & Rocktäschel, 2020).

At solved level, reliability differed more on tasks near the performance cutoff. On BipedalWalker-v3, GLPE solved 4 of 8 seeds and GLPE without gating solved 2 of 8, while RIAC solved 8 of 8 but at a slower median of 4.09M steps (Baranes & Oudeyer, 2009). On Humanoid-v5, solved-threshold reach counts were low across methods, which was consistent with the high-variance behavior seen in learning curves.

At 50 percent threshold, GLPE without gating reached the target in all seeds on four tasks and in 4 of 5 seeds on Humanoid-v5, matching the strongest baseline reach count on each environment. The gap between 50 percent and 100 percent success therefore concentrated on high-variance or near-cutoff regimes rather than on early competence acquisition.


Figure 5.2. Sample efficiency and reliability at fixed return thresholds.

![Figure 5.2: Sample efficiency and reliability at fixed return thresholds.](../resources/steps-to-beat-baselines.png)

Table 5.2. Reliability and speed at solved threshold.

| Environment | GLPE | GLPE (no gate) | Most reliable baseline |
|---|---|---|---|
| MountainCar-v0 | 10/10; 0.35M | 10/10; 0.35M | RIDE: 9/10; 0.44M |
| BipedalWalker-v3 | 4/8; 3.10M | 2/8; 3.04M | RIAC: 8/8; 4.09M |
| Ant-v5 | 7/8; 10.39M | 7/8; 10.39M | RIAC: 8/8; 10.22M |
| HalfCheetah-v5 | 8/8; 9.68M | 8/8; 9.42M | RIDE: 8/8; 9.03M |
| Humanoid-v5 | 1/5; 6.73M | 2/5; 18.23M | ICM: 2/5; 13.93M |

Table 5.3. Reliability and speed at 50 percent solved threshold.

| Environment | GLPE | GLPE (no gate) | Most reliable baseline |
|---|---|---|---|
| MountainCar-v0 | 10/10; 0.12M | 10/10; 0.11M | RIDE: 9/10; 0.13M |
| BipedalWalker-v3 | 8/8; 0.44M | 8/8; 0.41M | ICM: 8/8; 0.41M |
| Ant-v5 | 8/8; 4.61M | 8/8; 4.61M | RND: 8/8; 4.18M |
| HalfCheetah-v5 | 8/8; 2.01M | 8/8; 2.01M | Vanilla PPO: 8/8; 1.28M |
| Humanoid-v5 | 2/5; 14.51M | 4/5; 11.47M | ICM: 4/5; 10.32M |

### 5.4 Component Ablation Analysis

Component ablations evaluated whether impact and learning-progress terms contributed differently across environments. On MountainCar-v0, full GLPE obtained a final mean return of -96.2, while impact-only and LP-only variants fell to -111.8 and -106.6, respectively. This gap indicated that combining both signals was important in sparse-reward exploration.

On Ant-v5, the impact-only variant reached 5233, exceeding full GLPE at 4961, while LP-only was lower at 4599. On BipedalWalker-v3, LP-only reached 298.8, closest to the solved cutoff of 300, and exceeded both full GLPE and impact-only in final-checkpoint mean return.

Taken together, the ablation results showed that no single intrinsic component was uniformly optimal across tasks. The combined GLPE score remained a robust default because task-specific dominance between impact and learning progress could not be assumed in advance.


Table 5.4. Final-checkpoint mean extrinsic return for GLPE and component ablations.

| Environment | GLPE | Impact-only | LP-only |
|---|---|---|---|
| MountainCar-v0 | -96.2 [-96.5,-95.9] | -111.8 [-137.0,-96.2] | -106.6 [-127.4,-96.0] |
| BipedalWalker-v3 | 266.5 [214.0,301.3] | 277.5 [256.0,296.5] | 298.8 [285.5,308.1] |
| Ant-v5 | 4,961 (12, 17, 359, 421) | 5,233 (12, 17, 544, 663) | 4,599 (11, 17, 401, 617) |

### 5.5 Intrinsic Reward Dynamics

The intrinsic term in GLPE was designed as a temporary exploration aid rather than a persistent optimization target. Training therefore applied a cosine taper to the intrinsic coefficient so that intrinsic shaping weight decreased over time.

Reward decomposition diagnostics showed that GLPE and GLPE without gating reduced applied intrinsic contribution later in training, whereas several baselines retained nonzero intrinsic contribution throughout a larger fraction of training (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020). This behavior was consistent with the objective of reducing long-horizon dependence on intrinsic shaping once useful behavior had emerged.

Because evaluation used extrinsic return only, these diagnostics were interpreted as training-signal analysis rather than direct outcome metrics. Even so, the dynamics supported the intended mechanism of early exploration support followed by gradual emphasis on task reward.


Figure 5.3. Decomposition of rollout reward during training.

![Figure 5.3: Decomposition of rollout reward during training.](../resources/train-reward-decomp-baselines.png)

### 5.6 Gating Behavior Analysis

State-space gate maps from final checkpoints indicated that gate-off events occupied a small and typically localized subset of visited states. For MountainCar-v0, visualization used raw position and velocity. For higher-dimensional tasks, observations were z-scored and projected onto the first two principal components before plotting.

This pattern supported the interpretation that gating acted as a targeted guardrail against potentially unhelpful intrinsic shaping in persistently high-error and low-progress regions, rather than suppressing intrinsic motivation globally. The mechanism was therefore selective in application and preserved intrinsic shaping over most of the visited distribution.

Task-level outcomes remained mixed. Gating was beneficial in MountainCar-v0, while GLPE without gating was often similar or slightly stronger on dense-reward locomotion tasks. This result was consistent with a tradeoff between selective robustness and additional computational overhead.


Figure 5.4. State-space view of GLPE gating decisions from final-checkpoint trajectories.

![Figure 5.4: State-space view of GLPE gating decisions from final-checkpoint trajectories.](../resources/glpe-gate-map.png)

### 5.7 Wall-Clock Efficiency and Computational Overhead

Wall-clock AUC was computed under a common per-task time horizon equal to the minimum final runtime among compared methods, with curves truncated to that horizon and without extrapolation. This definition prevented slower methods from receiving extra area by running longer.

Under this wall-clock view, GLPE without gating stayed close to the strongest baseline on BipedalWalker-v3, HalfCheetah-v5, Ant-v5, and Humanoid-v5. The gated variant usually produced lower wall-clock AUC, which was consistent with additional robust-statistics and gating computations.

Per-update timing decomposition showed that environment stepping and PPO optimization dominated runtime on expensive MuJoCo tasks, while intrinsic overhead became proportionally more important on MountainCar-v0 where environment interaction was cheap (Schulman et al., 2017). A microbenchmark of gating-median recomputation showed 20,877 transitions per second for recomputation every update and 100,173 transitions per second with cache refresh every 64 updates, corresponding to a 4.83x throughput increase. Since cached medians can alter gating decisions when stale, this optimization was treated as an implementation option rather than a core benchmark condition.


Figure 5.5. Wall-clock AUC of evaluation performance under a common time horizon.

![Figure 5.5: Wall-clock AUC of evaluation performance under a common time horizon.](../resources/eval-auc-time-all-methods.png)

Figure 5.6. Timing breakdown per PPO update.

![Figure 5.6: Timing breakdown per PPO update.](../resources/timing-breakdown.png)

### 5.8 Summary of Findings

Results across curve-level, threshold-level, and efficiency-level analyses support four main findings. First, GLPE was strongest in sparse-reward exploration, with clear gains on MountainCar-v0 in both step-AUC and solved-threshold reliability. Second, on dense-reward locomotion tasks, GLPE variants remained competitive but did not consistently exceed the best intrinsic baseline on all metrics (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017; Raileanu & Rocktäschel, 2020).

Third, thresholded analysis showed that many apparent gaps at solved level were concentrated in high-variance or near-cutoff settings, especially BipedalWalker-v3 and Humanoid-v5, while intermediate-threshold competence was often comparable to top baselines (Baranes & Oudeyer, 2009). Fourth, ablation and diagnostic results indicated that combining impact and learning progress was generally robust across mixed task regimes, and that gating behaved selectively rather than globally.

Overall, the evidence indicates that GLPE is a practical intrinsic-shaping framework for balancing exploration guidance and policy optimization stability, with strongest benefits in sparse or exploration-sensitive environments and acceptable competitiveness elsewhere.

## 6. Conclusion and Recommendations

This chapter presents the final synthesis of the study outcomes and their implications for intrinsic-reward shaping in reinforcement learning. Conclusions are drawn from the reported curve-level, threshold-level, ablation, diagnostic, and efficiency analyses under a unified PPO training protocol across five control benchmarks (Schulman et al., 2017). Recommendations are then provided for practical use, methodological refinement, and subsequent research directions that remain aligned with the established scope and limitations of the study (Ng et al., 1999).

### 6.1 Conclusions

The study showed that intrinsic-reward shaping based on combined feature-space impact and region-local learning progress can improve exploration quality while preserving practical training stability across mixed task regimes (Baranes & Oudeyer, 2009; Raileanu & Rocktäschel, 2020). Under the benchmark conditions used in this work, GLPE without gating behaved as the most consistent default variant, remaining competitive with strong intrinsic baselines on both step-normalized and wall-clock views in most tested environments (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017).

The strongest gains were observed in sparse-reward exploration, particularly on MountainCar-v0, where GLPE produced favorable threshold reliability and step-efficiency behavior relative to compared methods. On dense-reward locomotion tasks, outcomes indicated competitive but non-uniform superiority, which is consistent with the higher variance and task-dependent exploration demands of those settings.

The gated GLPE variant provided targeted suppression of intrinsic shaping in regions where prediction error stayed high while local learning progress was weak, reducing exposure to potentially unproductive curiosity signals (Mavor-Parker et al., 2021). This behavior supported robustness in sparse settings but could be conservative in high-variance domains, especially when aggressive filtering delayed beneficial exploration.

The cosine taper schedule for intrinsic-reward scaling supported the intended transition from exploration assistance to task-return optimization later in training. This schedule design helped maintain compatibility with PPO optimization dynamics while limiting late-stage dependence on intrinsic bonuses (Schulman et al., 2017).

The study remained bounded to vector-observation control benchmarks and an on-policy PPO backbone, and the applied intrinsic shaping was not policy-invariant in the formal reward-transformation sense (Ng et al., 1999; Schulman et al., 2017). Therefore, conclusions should be interpreted as evidence of practical effectiveness within the evaluated setup rather than universal guarantees across architectures, observation modalities, or training paradigms.

### 6.2 Recommendations

For comparable low-dimensional continuous-control tasks trained with PPO, GLPE without gating should be considered the primary default configuration because it provided the best overall balance between consistency and performance across environments (Schulman et al., 2017).

The gated variant should be prioritized when the task exhibits sparse or delayed extrinsic feedback and when instability from persistent high prediction error is expected. In such cases, region-wise suppression can improve reliability by reducing time spent in low-progress exploratory regimes (Baranes & Oudeyer, 2009; Mavor-Parker et al., 2021).

Evaluation practice should retain multiple complementary views, including learning curves, step-normalized AUC, wall-clock AUC, and thresholded reliability at solved and reduced levels. This combined protocol avoids over-reliance on a single metric and better captures delayed attainment and variance-sensitive behavior.

Reporting of computational results should continue to separate algorithmic quality from implementation overhead. Runtime decomposition and explicit disclosure of optional optimizations, such as cached gating statistics, should be preserved so that comparisons remain interpretable and reproducible.

Future implementations should maintain consistency between shaping design and policy optimization settings by preserving explicit schedules for intrinsic scaling and by documenting hyperparameter choices in a task-aware manner (Schulman et al., 2017).

### 6.3 Future Work

Future work may extend GLPE to richer observation modalities, including image-based inputs, where latent representation quality and dynamics-model calibration can affect both impact and progress estimates (Burda, Edwards, Storkey, et al., 2018; Pathak et al., 2017).

Additional investigation is warranted for off-policy or hybrid training regimes to determine whether the same intrinsic formulation preserves its practical advantages when replay dynamics, target networks, and update frequencies differ from PPO (Schulman et al., 2017).

Adaptive gating mechanisms should be examined to reduce conservatism in high-variance environments while retaining protection against persistent noisy-error regions. Candidate directions include robust online threshold adaptation and confidence-aware region statistics grounded in existing uncertainty-aware exploration literature (Mavor-Parker et al., 2021).

Computational refinement remains important for broader deployment. Follow-up work should evaluate efficient approximations for region statistics and update scheduling that reduce overhead without materially altering gating decisions or benchmark conclusions.

Broader benchmark coverage is also recommended, including more diverse sparse-reward tasks and additional continuous-control settings, so that generalization claims can be assessed under wider dynamics and reward structures.

## Bibliography

(Badia et al., 2020)
Badia, A. P., Sprechmann, P., Vitvitskyi, A., Guo, D., Piot, B., Kapturowski, S., Tieleman, O., Arjovsky, M., Pritzel, A., Bolt, A., & Blundell, C. (2020). Never Give Up: Learning Directed Exploration Strategies. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2002.06038
(Badia et al., 2020)

(Baranes & Oudeyer, 2009)
Baranes, A., & Oudeyer, P. (2009). R-IAC: robust intrinsically motivated exploration and active learning. *IEEE Transactions on Autonomous Mental Development*, *1*(3), 155--169. https://doi.org/10.1109/tamd.2009.2037513
(Baranes & Oudeyer, 2009)

(Barto, 2012)
Barto, A. G. (2012). Intrinsic Motivation and Reinforcement Learning. In *Intrinsically Motivated Learning in Natural and Artificial Systems* (pp. 17--47). https://doi.org/10.1007/978-3-642-32375-1_2
(Barto, 2012)

(Bellemare et al., 2016)
Bellemare, M. G., Srinivasan, S., Ostrovski, G., Schaul, T., Saxton, D., & Munos, R. (2016). Unifying Count-Based exploration and intrinsic motivation. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1606.01868
(Bellemare et al., 2016)

(Burda, Edwards, Pathak, et al., 2018)
Burda, Y., Edwards, H., Pathak, D., Storkey, A., Darrell, T., & Efros, A. A. (2018). Large-Scale study of Curiosity-Driven Learning. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1808.04355
(Burda, Edwards, Pathak, et al., 2018)

(Burda, Edwards, Storkey, et al., 2018)
Burda, Y., Edwards, H., Storkey, A., & Klimov, O. (2018). Exploration by random network distillation. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1810.12894
(Burda, Edwards, Storkey, et al., 2018)

(Houthooft et al., 2016)
Houthooft, R., Chen, X., Duan, Y., Schulman, J., Filip, D. T., & Abbeel, P. (2016). VIME: Variational Information Maximizing Exploration. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1605.09674
(Houthooft et al., 2016)

(Mavor-Parker et al., 2021)
Mavor-Parker, A. N., Young, K. A., Barry, C., & Griffin, L. D. (2021). How to Stay Curious while Avoiding Noisy TVs using Aleatoric Uncertainty Estimation. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2102.04399
(Mavor-Parker et al., 2021)

(Ng et al., 1999)
Ng, A. Y., Harada, D., & Russell, S. (1999). Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping. In *Proceedings of the Sixteenth International Conference on Machine Learning* (pp. 278--287). Morgan Kaufmann Publishers Inc. https://doi.org/10.5555/645528.657613
(Ng et al., 1999)

(Ostrovski et al., 2017)
Ostrovski, G., Bellemare, M. G., Van Den Oord, A., & Munos, R. (2017). Count-Based Exploration with Neural Density Models. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1703.01310
(Ostrovski et al., 2017)

(Oudeyer, 2007)
Oudeyer, P. (2007). What is intrinsic motivation? A typology of computational approaches. *Frontiers in Neurorobotics*, *1*, 6. https://doi.org/10.3389/neuro.12.006.2007
(Oudeyer, 2007)

(Oudeyer et al., 2007)
Oudeyer, P., Kaplan, F., & Hafner, V. V. (2007). Intrinsic motivation systems for autonomous mental development. *IEEE Transactions on Evolutionary Computation*, *11*(2), 265--286. https://doi.org/10.1109/tevc.2006.890271
(Oudeyer et al., 2007)

(Pathak et al., 2017)
Pathak, D., Agrawal, P., Efros, A., & Darrell, T. (2017). Curiosity-driven Exploration by Self-supervised Prediction. In *arXiv*(arXiv:1705.05363). arXiv. https://arxiv.org/abs/1705.05363
(Pathak et al., 2017)

(Pathak et al., 2019)
Pathak, D., Gandhi, D., & Gupta, A. (2019). Self-Supervised Exploration via disagreement. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1906.04161
(Pathak et al., 2019)

(Raileanu & Rocktäschel, 2020)
Raileanu, R., & Rocktäschel, T. (2020). RIDE: Rewarding Impact-Driven Exploration for Procedurally-Generated Environments. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2002.12292
(Raileanu & Rocktäschel, 2020)

(Savinov et al., 2018)
Savinov, N., Raichuk, A., Marinier, R., Vincent, D., Pollefeys, M., Lillicrap, T., & Gelly, S. (2018). Episodic Curiosity through Reachability. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1810.02274
(Savinov et al., 2018)

(Schmidhuber, 1991)
Schmidhuber, J. (1991). A possibility for implementing curiosity and boredom in Model-Building neural controllers. In *The MIT Press eBooks* (pp. 222--228). https://doi.org/10.7551/mitpress/3115.003.0030
(Schmidhuber, 1991)

(Schulman et al., 2015)
Schulman, J., Moritz, P., Levine, S., Jordan, M., & Abbeel, P. (2015). High-Dimensional Continuous Control Using Generalized Advantage Estimation. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1506.02438
(Schulman et al., 2015)

(Schulman et al., 2017)
Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). Proximal Policy Optimization Algorithms. In *arXiv*(arXiv:1707.06347). arXiv. https://arxiv.org/abs/1707.06347
(Schulman et al., 2017)

(Singh et al., 2005)
Singh, S., Barto, A. G., & Chentanez, N. (2005). *Intrinsically motivated reinforcement learning*. https://doi.org/10.21236/ada440280
(Singh et al., 2005)

(Stadie et al., 2015)
Stadie, B. C., Levine, S., & Abbeel, P. (2015). Incentivizing exploration in reinforcement learning with deep predictive models. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.1507.00814
(Stadie et al., 2015)

(Tang et al., 2016)
Tang, H., Houthooft, R., Foote, D., Stooke, A., Chen, X., Duan, Y., Schulman, J., Filip, D. T., & Abbeel, P. (2016). #Exploration: A study of Count-Based exploration for deep reinforcement learning. *arXiv (Cornell University)*, *30*, 2750--2759. https://doi.org/10.48550/arxiv.1611.04717
(Tang et al., 2016)
