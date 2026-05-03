### 5.2 Final Performance and Step-AUC

Final-checkpoint comparisons and step-normalized AUC summarized both asymptotic quality and learning speed over fixed interaction budgets [18]. Step-AUC values showed that GLPE achieved the highest mean value on MountainCar-v0, with GLPE equal to or near the best baseline on several other tasks but not dominant in all environments [18].

For BipedalWalker-v3, GLPE without gating reached a competitive step-AUC of 255.2, close to the best baseline value of 257.3 from ICM [9][18]. For Ant-v5 and HalfCheetah-v5, GLPE values remained below the strongest baseline means, although confidence intervals overlapped in several cases [10][11][18]. On Humanoid-v5, all methods exhibited wide uncertainty bands, and step-AUC ranking was therefore unstable under bootstrap uncertainty [18].

These results indicated that GLPE provided strong sample-efficiency behavior in sparse-reward settings, while remaining broadly competitive in dense-reward settings where baseline intrinsic objectives were already effective [18].
