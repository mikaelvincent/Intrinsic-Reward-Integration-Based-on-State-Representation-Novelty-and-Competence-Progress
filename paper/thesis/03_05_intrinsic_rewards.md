### 3.5 Intrinsic Rewards

Intrinsic rewards were used to complement sparse or delayed extrinsic feedback by assigning additional utility to exploratory transitions. Prior approaches include prediction-error curiosity, random-network disagreement, impact-driven exploration, and region-based competence progress {{CIT:2,6,13,15}}.

The study adopted a composite intrinsic structure built from two components: feature-space impact and region-local learning progress. Impact measured representation change across successive observations, while learning progress captured recent reduction in local forward-model error relative to a slower baseline. Component scales were normalized online with running RMS statistics before weighted combination, which reduced sensitivity to task-dependent magnitude differences. The resulting intrinsic signal was then clipped and scaled before addition to extrinsic reward {{CIT:2,15,19}}.

Two variants were considered. GLPE (no gate) used the composite score directly. GLPE applied an additional region-specific binary gate that suppressed intrinsically attractive but persistently unproductive regions according to robust global thresholds and hysteretic reactivation conditions {{CIT:2,19}}.
