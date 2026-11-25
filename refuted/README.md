# False rule proposals

These are counterexamples to proposed universal identities, not executable OSR
rules. The full calculations and corrected statements are in the
[rule design](../docs/rule-design.md#six-false-candidates-and-exact-witnesses).

| False proposal | Witness | Lean status |
|---|---|---|
| `(A+B)^2 = A^2 + 2AB + B^2` | `A=[[0,1],[0,0]]`, `B=[[0,0],[1,0]]` | Compiled concrete counterexample |
| `exp(A+B) = exp(A)exp(B)` without commutation | Same noncommuting `A,B` | Compiled real-matrix counterexample |
| `det(A+B) = det(A)+det(B)` | `A=B=I₂` | Compiled concrete counterexample |
| `det(kA) = k det(A)` | `k=2`, `A=I₂` | Compiled concrete counterexample |
| `(AB)⁻¹ = A⁻¹B⁻¹` | `A=[[1,1],[0,1]]`, `B=[[1,0],[1,1]]` | Compiled counterexample; both determinants proved units |
| `tr(AB) = tr(A)tr(B)` | `A=B=I₂` | Compiled concrete counterexample |

Five witnesses are in the [pinned OSR Lean source](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSRTest/LinearAlgebraCounterexamples.lean).
The [sixth proof](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/main/verification/MatrixExponential.lean)
uses the same two nilpotent matrices as the numerical test. The [status
report](../reports/status.md) gives the replay commands and OSR export status.
