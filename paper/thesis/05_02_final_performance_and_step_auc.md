### 5.2 Final Performance and Step-AUC

Final-checkpoint comparisons and step-normalized AUC summarized both asymptotic quality and learning speed over fixed interaction budgets [18]. Step-AUC values showed that GLPE achieved the highest mean value on MountainCar-v0, with GLPE equal to or near the best baseline on several other tasks but not dominant in all environments [18].

For BipedalWalker-v3, GLPE without gating reached a competitive step-AUC of 255.2, close to the best baseline value of 257.3 from ICM [9][18]. For Ant-v5 and HalfCheetah-v5, GLPE values remained below the strongest baseline means, although confidence intervals overlapped in several cases [10][11][18]. On Humanoid-v5, all methods exhibited wide uncertainty bands, and step-AUC ranking was therefore unstable under bootstrap uncertainty [18].

These results indicated that GLPE provided strong sample-efficiency behavior in sparse-reward settings, while remaining broadly competitive in dense-reward settings where baseline intrinsic objectives were already effective [18].


Table 5.1. Step-AUC of deterministic evaluation return versus cumulative environment steps [18].

| Environment | GLPE | GLPE (no gate) | Best baseline |
|---|---|---|---|
| MountainCar-v0 | -107.0 [-114.8,-101.8] | -111.3 [-128.7,-101.4] | RIDE: -113.7 [-134.2,-101.9] |
| BipedalWalker-v3 | 249.0 [223.9,270.7] | 255.2 [230.0,275.6] | ICM: 257.3 [229.4,278.3] |
| Ant-v5 | 3,402 [3,067,3,708] | 3,402 [3,067,3,707] | RND: 3,565 [3,202,3,876] |
| HalfCheetah-v5 | 5,005 [4,708,5,316] | 4,998 [4,700,5,296] | RIDE: 5,208 [5,019,5,410] |
| Humanoid-v5 | 1,583 [551,3,360] | 1,665 [769,2,921] | ICM: 1,781 [829,2,797] |
