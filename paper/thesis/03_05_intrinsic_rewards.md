### 3.5 Intrinsic Rewards

Intrinsic rewards were introduced to supplement delayed or sparse extrinsic feedback by providing additional training signal for exploration. The implemented design combined feature-space impact and region-local learning progress, which were normalized with running root-mean-square statistics before weighted aggregation.

Let \(I_t=\lVert z_{t+1}-z_t\rVert_2\) denote impact in latent space and let \(\mathrm{LP}_t\) denote local learning progress from region-level prediction-error dynamics. With normalized components \(\widetilde{I}_t\) and \(\widetilde{\mathrm{LP}}_t\), the shared base intrinsic score was
\[
u_t = \alpha_{\mathrm{impact}}\widetilde{I}_t + \alpha_{\mathrm{LP}}\widetilde{\mathrm{LP}}_t,
\]
where \(\alpha_{\mathrm{impact}},\alpha_{\mathrm{LP}}\ge 0\). GLPE (no gate) set \(r_t^{\mathrm{int}}=u_t\). GLPE applied a region-specific binary gate so that \(r_t^{\mathrm{int}}=g_{\rho_t}u_t\), suppressing regions with persistently high local error and low learning progress {{CIT:2,15}}.
