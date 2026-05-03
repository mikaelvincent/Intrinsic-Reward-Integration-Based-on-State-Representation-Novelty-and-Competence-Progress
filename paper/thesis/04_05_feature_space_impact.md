### 4.5 Feature-Space Impact The second intrinsic component measured latent-state displacement between consecutive observations,
\[
I_t=\lVert z_{t+1}-z_t\rVert_2.
\]
This term rewarded transitions that changed the learned representation, and therefore emphasized state changes that were significant in latent feature geometry rather than raw observation space [15],. To stabilize scale across environments and across training phases, component-wise RMS normalization was applied. For a scalar signal \(x_t\), a running accumulator was updated as
\[
v\leftarrow\beta_{\mathrm{rms}}v+(1-\beta_{\mathrm{rms}})x_t^2,
\]
then normalized using \(\mathrm{RMS}(x_t)=\sqrt{v+\varepsilon}\). This produced
\[
\widetilde{I}_t=\frac{I_t}{\mathrm{RMS}(I_t)}, \qquad \widetilde{\mathrm{LP}}_t=\frac{\mathrm{LP}_t}{\mathrm{RMS}(\mathrm{LP}_t)}.
\]
The normalized values reduced method sensitivity to absolute signal magnitude and supported a shared mixing rule for GLPE and GLPE (no gate).
