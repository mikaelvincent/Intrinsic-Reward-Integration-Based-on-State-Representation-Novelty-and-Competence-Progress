### 4.7 Intrinsic Reward Scheduling

Intrinsic shaping strength was scheduled over training using a cosine taper in the GLPE family. Let \(p\in[0,1]\) denote training progress as fraction of total environment steps, and let \(p_{\mathrm{start}}<p_{\mathrm{end}}\) define taper interval. The schedule was
\[
w(p)=
\begin{cases}
1, & p\le p_{\mathrm{start}},\\
\tfrac{1}{2}\left(1+\cos\left(\pi\tfrac{p-p_{\mathrm{start}}}{p_{\mathrm{end}}-p_{\mathrm{start}}}\right)\right), & p_{\mathrm{start}}<p<p_{\mathrm{end}},\\
0, & p\ge p_{\mathrm{end}}.
\end{cases}
\]
The effective intrinsic coefficient became \(\eta_t=\eta\,w(p_t)\), and remained constant at \(\eta_t=\eta\) when schedule bounds were not specified [18].

This schedule treated intrinsic reward as a transient exploration aid, with stronger influence early in learning and reduced influence later when policy refinement depended more on extrinsic objective optimization. The same scheduling rule was used in GLPE and GLPE (no gate), preserving comparability between the two proposed variants [16], [18].
