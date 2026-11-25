# Pilot status

| Inventory | Count | Evidence |
|---|---:|---|
| Designed forward identities | 28 | All 28 have a hand-written mathematical counterpart compiled by Lean. |
| False proposals | 6 | Lean checks a concrete witness for every proposal. |
| Exported and certified OSR v1 rules | 0 | Typed OSR terms, audited symbol mappings and generated theorems are pending. |

The four additional formulations below cover existing catalogue entries.
The formal verification eligibility of the eventual v1 rules depends on
their typed translation. Generation has not been attempted for any entry.

The matrix proofs cover rectangular trace cyclicity and preserve explicit
invertibility hypotheses. Mathlib assigns a value to singular inverses, so
those hypotheses matter when translating a rule for a CAS. Five concrete
counterexamples, including the invertible witness for inverse product order,
reside in the same pinned OSR project as the original 28 statements.
[Identities](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSRTest/LinearAlgebraPilot.lean)
and [five counterexamples](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSRTest/LinearAlgebraCounterexamples.lean).

V3 uses the determinant of three **columns**. V6 uses the Euclidean norm
and real inner product on standard oriented ℝ³. Extending the coordinate
proofs to an arbitrary oriented Euclidean space requires transport by an
orientation-preserving isometry. E1 and E2 now have both real and complex
matrix proofs. E2 retains the explicit hypothesis `Commute A B`.
[Additional formulations](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/main/verification/PilotFormulations.lean).

For the sixth false proposal, the proof uses the two real matrices in the
numerical suite. Both square to zero. Their individual exponentials multiply
to a matrix that fails to commute with their sum, whereas the exponential of
the sum commutes with its argument. The contradiction uses exact arithmetic.
[Exponential counterexample](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/main/verification/MatrixExponential.lean).

## Reproduce the checks

From this repository, with elan, Git and Python available, run the following
commands in a shell. The pinned OSR checkout supplies the Lake project,
Lean 4.35.0 and Mathlib revision `56a005855ea17e0b0958f73ec801ae140b0a1679`.

```sh
git clone https://github.com/OpenSymbolicRules/Lean.git OSR-Lean
git -C OSR-Lean checkout --detach "$(cat verification/lean-revision)"
(cd OSR-Lean && lake exe cache get)
just lean OSR-Lean
```

CI compiles the upstream mathematical statements and the pilot sources with
warnings treated as errors. The five new theorem declarations also check
their axiom lists. The [numerical report](numerical.json) records five
deterministic test groups. Checking that a serialized rule and its assumptions
denote the theorem still requires the typed OSR export and independent recheck.
