### 3.7 Online Region Partitioning

Learning progress was localized through an online binary partition of latent space. Each embedding \(z_t\) was routed to a leaf region \(\rho_t\). A leaf was split when capacity and depth conditions were satisfied, using the highest-variance coordinate and a median threshold to produce non-degenerate child regions {{CIT:2}}.

For each region \(r\), short-horizon and long-horizon exponential moving averages of forward error were maintained:
\[
\mu_r^{\mathrm{long}}\leftarrow \beta_{\mathrm{long}}\mu_r^{\mathrm{long}}+(1-\beta_{\mathrm{long}})e_t,
\]
\[
\mu_r^{\mathrm{short}}\leftarrow \beta_{\mathrm{short}}\mu_r^{\mathrm{short}}+(1-\beta_{\mathrm{short}})e_t.
\]
Region-local learning progress was defined as
\[
\mathrm{LP}(r)=\max\left(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}\right).
\]
This quantity increased when recent local prediction error decreased relative to the slower baseline.
