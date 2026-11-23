# OpenSymbolicRules — LinearAlgebra

This pilot investigates portable, oriented rewrite rules for abstract matrices
and vectors. OpenSymbolicRules is language-independent: a consumer need not
use a particular computer algebra system or proof assistant.

**Status: research and numerical prototype.** The 28 designed identities are
not yet distributed as OSR rule files or certified by Lean. Some corresponding
hand-written Mathlib statements have been checked; see [status](reports/status.md).
The current OSR v1
schema cannot faithfully express the pilot's typed matrix contexts; the
[proposal](docs/schema-proposal.md) is not an official specification change.
Numerical checks are sanity checks, never mathematical proofs.

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
followed by `just docs`. The pinned Lean and Mathlib versions are those of the
existing OSR Lean project; no independent proof pipeline is claimed here.
