# Changelog

All notable changes to this project will be documented in this file. The
format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Six generated, typed OpenMath matrix examples linked to their Lean proofs,
  with rectangular real and complex consumer tests and a byte comparison in CI.

- A Lean counterexample to the unconditional exponential sum rule using the
  two nilpotent real matrices in the numerical suite.
- Checked column-determinant and Euclidean norm formulations for the 3D
  vector rules and complex versions of both matrix exponential identities.
- A CI check and `just lean` command that compile the mathematical sources
  against the pinned OpenSymbolicRules/Lean project.

- Research and design for abstract matrix and vector rewrite rules, OSR schema
  compatibility, Mathlib mapping and future mathematical domains.
- Deterministic numerical sanity checks for 28 proposed identities and six
  counterexamples; these checks are not proofs or schema-driven validation.
- A status report distinguishing preliminary Mathlib checks from certified
  OSR rule exports.
- An experimental, fail-closed shape guard for a small OpenMath expression
  fragment, with tests for ordering, dimensions and unsupported symbols.
- A Documenter.jl documentation build with landing page and generated
  `llms.txt` and `llms-full.txt` files under the build directory.
- A preliminary CI workflow for the numerical and shape checks and the
  documentation build; OSR generation and proof-audit gates remain pending.
