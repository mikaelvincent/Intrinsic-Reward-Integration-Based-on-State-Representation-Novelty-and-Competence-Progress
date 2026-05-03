### 4.2 Proposed GLPE Framework

The proposed framework augmented extrinsic reward with a clipped intrinsic term,
\[
r_t = r_t^{\mathrm{ext}} + \eta_t\,\mathrm{clip}(r_t^{\mathrm{int}},-r_{\max},r_{\max}),
\]
where \(\eta_t\) controlled intrinsic strength over training and \(r_{\max}\) bounded intrinsic magnitude [19]. Intrinsic reward was set to zero on environment-terminal transitions so that shaping did not depend on episode termination .

A shared base score was computed from two components: feature-space impact and region-local learning progress. Let \(z_t=\phi_\omega(o_t)\) be the learned latent representation. The base intrinsic score was defined as
\[
u_t = \alpha_{\mathrm{impact}}\widetilde{I}_t + \alpha_{\mathrm{LP}}\widetilde{\mathrm{LP}}_t,
\]
where \(\widetilde{I}_t\) and \(\widetilde{\mathrm{LP}}_t\) were RMS-normalized components and \(\alpha_{\mathrm{impact}},\alpha_{\mathrm{LP}}\ge 0\) were mixing weights [2,15].

Two variants were implemented within this shared structure. GLPE (no gate) used \(r_t^{\mathrm{int}}=u_t\). GLPE applied a binary, region-specific gate and used \(r_t^{\mathrm{int}}=g_{\rho_t}u_t\), where \(\rho_t\) denoted the assigned latent-space region for transition \(t\) [2]. This separation preserved a common signal foundation while isolating the effect of gating behavior in comparative analysis.
