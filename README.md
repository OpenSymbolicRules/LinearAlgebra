# OpenSymbolicRules — LinearAlgebra

This pilot investigates portable, oriented rewrite rules for abstract matrices
and vectors. OpenSymbolicRules is language-independent: a consumer need not
use a particular computer algebra system or proof assistant.

The pilot contains [eleven typed matrix rewrites](docs/matrix-examples.md)
and [six typed vector rewrites](docs/vector-examples.md).
Lean checks their directed equalities and generates the portable JSON from
the same terms. The wider catalogue contains 28 identities with mathematical
proofs and six false proposals with compiled counterexamples. Typed OSR v1
certification requires an approved context and registry interpretation.
See the [status report](reports/status.md) and [schema proposal](docs/schema-proposal.md).

The [rule design](docs/rule-design.md) specifies dimensions, assumptions,
orientation and six false proposals. [Reconnaissance](docs/recon.md) records
the existing ecosystem and [Mathlib mapping](docs/mathlib-mapping.md) records
candidate declarations. The [numerical prototype](docs/numerical-prototype.md)
explains how to run the checks and their limitations. Future tensor and
differential geometry domains are discussed in [architecture research](docs/architecture-research.md);
they are outside this pilot's implementation scope.

Run `just test` to execute the deterministic Python standard-library tests,
or `just report` for a machine-readable test report. No third-party Python
dependency is needed. The tests include an experimental guard for a small
OpenMath fragment; it is not a complete OSR rule validator or matcher. Build
the documentation with `julia --project=docs -e 'using Pkg; Pkg.instantiate()'`
followed by `just docs`. To reproduce the Lean checks, see the checkout and
`just lean` commands in the [status report](reports/status.md).
