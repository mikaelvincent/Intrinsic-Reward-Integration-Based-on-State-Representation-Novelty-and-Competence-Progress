### 2.4 Impact-Driven Exploration

Impact-driven exploration rewarded transitions that produced substantial change in the agent's learned representation, rather than rewarding novelty alone {{CIT:15}}. Under this perspective, useful exploration is associated with controllable interaction that moves behavior into distinct states.

RIDE operationalized this principle through feature-space displacement and visitation-based modulation, reducing repeated reward from revisiting similar states {{CIT:15}}. This approach was relevant in settings where novel observations were not controllable or not informative for policy improvement.

The impact perspective complemented both novelty and learning-progress approaches. Novelty promoted broad coverage, learning progress prioritized regions with improving models, and impact emphasized controllable state change {{CIT:2,15,17}}. This complementarity motivated hybrid intrinsic objectives.

The GLPE family adopted impact as one component of its intrinsic score and combined it with region-local learning progress. This combination was intended to preserve movement toward behaviorally meaningful transitions while reducing emphasis on high-error regions that did not exhibit sustained model improvement.
