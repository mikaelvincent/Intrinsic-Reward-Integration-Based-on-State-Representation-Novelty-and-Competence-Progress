### 4.4 Region-Local Learning Progress

Learning progress was localized through an online binary partition tree over latent space. Each embedding \(z_t\) was routed to a leaf region \(\rho_t\). A leaf was split when it reached capacity \(C\), had depth below \(D_{\max}\), and allowed a non-degenerate partition. Split dimension selection followed highest coordinate variance, and thresholding used the coordinate median [13], [18].

For each region \(r\), long-horizon and short-horizon exponential moving averages of forward prediction error were maintained,
\[
\mu_r^{\mathrm{long}}\leftarrow\beta_{\mathrm{long}}\mu_r^{\mathrm{long}}+(1-\beta_{\mathrm{long}})e_t,
\]
\[
\mu_r^{\mathrm{short}}\leftarrow\beta_{\mathrm{short}}\mu_r^{\mathrm{short}}+(1-\beta_{\mathrm{short}})e_t,
\]
for transitions assigned to region \(r\). Newly created region identifiers were initialized with \(\mu_r^{\mathrm{long}}=\mu_r^{\mathrm{short}}=e_t\) at first visit [18].

Region-local learning progress was defined as
\[
\mathrm{LP}(r)=\max(0,\mu_r^{\mathrm{long}}-\mu_r^{\mathrm{short}}).
\]
The transition-level value used in intrinsic computation was \(\mathrm{LP}_t=\mathrm{LP}(\rho_t)\). This definition emphasized areas where recent prediction error dropped below longer-horizon baseline, which indicated active local model improvement [13], [18].
