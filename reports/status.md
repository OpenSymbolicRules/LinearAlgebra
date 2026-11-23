# Pilot status

The inventory contains 28 proposed directed identities and six proposed false
rules. It is not yet an exported OSR ruleset. All OSR certification statuses
are pending: no typed OSR terms, generated theorems or audited mappings exist
for this pilot, so none of the 28 is classified as OSR-proved or OSR-refuted.
The formal-verification eligibility proportion cannot yet be determined.

As a preliminary Mathlib investigation, 28 corresponding hand-written
mathematical statements compile with Lean 4.35.0 and Mathlib revision
`56a005855ea17e0b0958f73ec801ae140b0a1679`. The source is
[`Lean/OSRTest/LinearAlgebraPilot.lean`](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSRTest/LinearAlgebraPilot.lean).
These are not generated
OSR theorems: they establish neither CD semantics nor an OSR translation.
The checked matrix cases include rectangular trace cyclicity and explicit
invertibility assumptions. Mathlib totalizes singular matrix inverse to zero;
the hypotheses are retained even when a Mathlib lemma holds more generally.

The cross-product statements use the standard coordinate model; Lagrange's
identity is written using dot products, and the scalar triple product uses a
matrix of rows. Correspondence to the intended intrinsic, norm and column
formulations requires review. The exponential statements are checked over the
reals; the numerical suite does not cover complex matrices.

Five of the six proposed false formulas have compiled concrete Lean
counterexamples in [`Lean/OSRTest/LinearAlgebraCounterexamples.lean`](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSRTest/LinearAlgebraCounterexamples.lean); the
inverse example separately proves that both witness matrices are invertible.
The noncommuting exponential counterexample has a numerical witness but no
Lean proof yet. These counterexamples are mathematical checks, not exported
OSR refutation records.
The [numerical test report](numerical.json) records four test groups; it is not
a proof and does not test OSR serialization. The next tasks are proof coverage,
typed interpretation and an audited export/recheck path under the existing OSR
verification architecture. A successful hand-written proof must not be
reported as an OSR rule certification.

The prototype CI runs the numerical and limited shape-guard tests and builds
the documentation. It does not yet generate OSR theorems or independently
recheck the Lean statements. Those gates cannot be claimed until the typed
rule format, semantic registry and existing export/recheck pipeline support
the pilot.
