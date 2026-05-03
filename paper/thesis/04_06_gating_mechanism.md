### 4.6 Gating Mechanism

The GLPE gating mechanism was designed to suppress intrinsic shaping in regions that remained difficult to predict yet showed limited evidence of ongoing learning progress. Let \(\mathcal{R}\) denote visited regions. Robust global references were computed using medians,
\[
\mathrm{LP}_{\mathrm{med}}=\mathrm{median}_{r\in\mathcal{R}}\,\mathrm{LP}(r), \qquad e_{\mathrm{med}}=\mathrm{median}_{r\in\mathcal{R}}\,\mu_r^{\mathrm{short}}.
\]
A learning-progress threshold was defined as \(\tau_{\mathrm{LP}}=\kappa\,\mathrm{LP}_{\mathrm{med}}\), and normalized short-horizon error as
\[
s_r=\frac{\mu_r^{\mathrm{short}}}{e_{\mathrm{med}}+\varepsilon}.
\]
Region \(r\) was marked unproductive on a visit when both \(\mathrm{LP}(r)<\tau_{\mathrm{LP}}\) and \(s_r>\tau_s\) held [8].

Each region maintained binary gate state \(g_r\in\{0,1\}\) and persistence counters. Gating was activated only after at least \(R_{\min}\) regions had been visited, so that median references were sufficiently informative. With gating active, persistence and hysteresis were enforced: an active gate was turned off after \(K\) consecutive unproductive visits, while a disabled gate was re-enabled only after two consecutive visits satisfying \(\mathrm{LP}(r)>h\tau_{\mathrm{LP}}\), with \(h>1\). If gating was inactive, gates remained enabled and counters were reset .

The final intrinsic reward for GLPE used
\[
r_t^{\mathrm{int}}=g_{\rho_t}u_t.
\]
This operation retained the same base score used by GLPE (no gate), while introducing selective suppression as a guardrail against persistent curiosity traps [8].
