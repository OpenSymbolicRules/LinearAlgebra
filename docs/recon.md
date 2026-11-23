# Reconnaissance: abstract linear algebra in OSR

Status: research and design only; examined 23 November 2026. This directory is
not a Git repository. No existing OSR repository or specification has been
changed by this investigation. All version claims below refer to the checked
out commits, not to an unpinned future version.

## Executive finding and phase-0 decision

Proceed with **design**, not a conforming implementation. The existing Lean
and Verification infrastructure is available, so the generator-availability
stop condition is not triggered. However, the current v1 contract does not
provide heterogeneous typed variables, matrix or vector carriers, or the
necessary registry interpretations. A portable JSON object may be written,
but neither schema validity nor numerical agreement makes it a conforming,
certified OSR v1 rule. Approval of a representation and of any changes to
other repositories is needed before implementation. The proposed pilot can
host research artifacts independently, but cannot deliver its full v1 and
independent-recheck acceptance criteria without integration work in existing
repositories, or a maintainers-approved extension mechanism.

## Repository snapshot

The [public OSR organization](https://github.com/OpenSymbolicRules) exposes
Specification, Lean, Verification, Conformance, OpenMath, Trigonometry,
Algebra, Logic, Calculus, Integration and the independent client
OpenSymbolicRules.jl, among others. The public organization API did not list
LinearAlgebra, TensorAlgebra or DifferentialGeometry at inspection time.
Three *local*, empty Git worktrees with those names already exist and point to
`s-celles`, not to the OSR organization. They have no commits; their remote
existence or ownership cannot be inferred from the local configuration. They
were not modified and no repository was created.

| Component | Inspected evidence | Purpose |
|---|---|---|
| Specification | [`eb12fb1`](https://github.com/OpenSymbolicRules/Specification/tree/eb12fb1), v1 and v0.1 specs and schemas | Normative interchange and legacy syntax; v1 is a draft |
| Lean | [`68f25be`](https://github.com/OpenSymbolicRules/Lean/tree/68f25be), `OSR/Expr.lean`, `OSR/Registry.lean`, `scripts/Export.lean` | Lean-native statement, kernel proofs, registry, audits and JSON export |
| Verification | [`658d3cb`](https://github.com/OpenSymbolicRules/Verification/tree/658d3cb), `scripts/recheck.sh` | Published digest-addressed reports and independent source rebuild/recheck |
| Trigonometry | [`18bf9c6`](https://github.com/OpenSymbolicRules/Trigonometry/tree/18bf9c6), `rules/`, `v1/`, `scripts/check-v1.sh` | v0.1 rules, v1 generated bundle, validation and optional byte comparison with a report |
| Julia client | [OpenSymbolicRules.jl](https://github.com/OpenSymbolicRules/OpenSymbolicRules.jl), `src/OpenSymbolicRules.jl`, `src/osr_v1.jl` | Independent consumer; not the mathematical authority |
| OpenMath | [OpenMath CDs](https://openmath.org/cd/) and OSR OpenMath snapshots | Symbol definitions and pinned CD versions |

## Rule and expression model

[OSR v1](https://github.com/OpenSymbolicRules/Specification/blob/eb12fb1/docs/osr-v1.md)
is `1.0.0-alpha.1`. `OMS`, `OMV`, `OMI`, applications of an `OMS`, and
symbol-binder `OMBIND` form its fragment; a special applied integral is the
only permitted non-symbol applicant. Rules declare `variables`, `pattern`,
`replacement`, `conditions`, `orientation: forward`, `applicability:
defined_pattern`, `profiles`, `priority`, `symbols`, `provenance`, `findings`
and per-domain verification. `id` is dotted and unique, while `legacy_id`
is optional migration provenance. Profiles order rules by priority. The
reference rewrite is syntactic and must not apply undecided conditions.

Variables are OpenMath names, with no variable-level type field. Domains in
the v1 schema are `real`, `complex`, and `boolean`; `set1#in` is restricted
by the specification to integer membership in this condition fragment.
Allowed conditions are equality, inequality, greater-than, greater-or-equal,
integer membership and binary disjunction. `independent` is a syntactic
free-variable matching constraint, not a type or mathematical precondition.
The `defined_pattern` contract requires a defined result equal in value to a
defined matching pattern; it must be preserved for partial inverse operations.

Schema acceptance, specification conformance, symbol interpretation and
proof certification are four different checks. The schema checks JSON shape,
not shape equality or the truth of a rule. `OMS` is syntactically open, but
V1-E-003, V1-P-001 and the semantic registry require declared, real CD
symbols and domain interpretations. Existing consumers reject undeclared
symbols or unsupported expression kinds; a declared symbol is not thereby a
verified semantic mapping. A supported mapping must be reviewed or formally
related before a proved record can be certified.

The v0.1 [specification](https://github.com/OpenSymbolicRules/Specification/blob/eb12fb1/docs/spec.md)
uses JSON S-expressions, wildcard strings and constraint strings. Its
`meta.json` has `extensions` for operator declarations and
`custom_predicates` for extensions; these are **not** a general v1 rule-level
type extension, nor do they certify new symbol semantics. v0.1 and v1 are not
wire-compatible. A Trigonometry file such as `1.3-double-angle.json` records
semantics, pattern, constraints, result and provenance; its v1 counterpart is
generated, with formal records and CD digests.

## Existing domain and noncommutative support

Lean's `OSR.Expr` uses a fixed scalar operator enumeration and `OSR.Interp`
interprets variables in a single field-valued environment. `OSR.Cond` has a
fixed enumeration. Real, complex and Boolean interpretations exist, but a
rectangular matrix, vector and scalar do not inhabit one existing field
carrier. The registry's present `arith1#times` interpretation and CMP audit
are scalar-field specific. Merely declaring a new `OMS` in JSON cannot create
a type-preserving matrix interpretation or verify it.

The v0.1 Julia client explicitly marks `arith1#times` associative but does
**not** put it in its commutative-symbol set, precisely because the operands
might be matrices; `arith1#plus` is commutative. The separate v1 client uses
ordered syntactic matching, not general AC matching. Neither fact proves that
the clients understand matrix shapes or execute this pilot: adapters, typed
condition evaluation and tests remain future work.

## OpenMath survey

| CD and status | Actual symbols | Relevance / cautions |
|---|---|---|
| [linalg1](https://openmath.org/cd/linalg1.html), official | `determinant`, `matrix_selector`, `outerproduct`, `scalarproduct`, `transpose`, `vector_selector`, `vectorproduct` | Transpose/determinant are representation-independent; `vectorproduct` is specifically three-dimensional and `scalarproduct` is Euclidean. It does not define matrix multiplication or trace. |
| [linalg2](https://openmath.org/cd/linalg2.html), official | `matrix`, `matrixrow`, `vector` | Row-oriented constructors, not an abstract matrix type. |
| [linalg3](https://openmath.org/cd/linalg3.html), experimental | `matrix`, `matrixcolumn`, `vector` | Column-oriented constructors; not aliases for linalg2. |
| [linalg4](https://openmath.org/cd/linalg4.html), experimental | `characteristic_eqn`, `columncount`, `eigenvalue`, `eigenvector`, `rank`, `rowcount`, `size` | `size` is vector length, not a general pair-valued shape. |
| [linalg5](https://openmath.org/cd/linalg5.html), experimental | `Hermitian`, `anti-Hermitian`, `banded`, `constant`, `diagonal_matrix`, `identity`, `lower-Hessenberg`, `lower-triangular`, `scalar`, `skew-symmetric`, `symmetric`, `tridiagonal`, `upper-Hessenberg`, `upper-triangular`, `zero` | Mostly constructors. `symmetric` constructs from a vector of vectors, not a unary predicate; `identity(n)` specifies positive integral dimension. |
| [sts2](https://openmath.org/cd/sts2.html), experimental | `interval`, `list`, `matrix`, `square_matrix`, `vector`, `vector_n` | Type constructors worth evaluating; no assumption that a general symbolic m-by-n dependent type or OSR v1 typing already exists. |
| [tensor1](https://openmath.org/cd/tensor1.html), experimental | `Cartesian`, `Kronecker_tensor`, `Levi-Civita`, `basis_selector`, `contra_index`, `covar_index`, `metric_tensor`, `tensor_selector`, `tuple`, `tuple_selector`, `unit_Cartesian` | Existing index and basis vocabulary for future investigation; it does not by itself establish an intrinsic tensor or manifold type system. |
| [linalg6](https://openmath.org/cd/linalg6.html), experimental | `matrix_tensor`, `vector_tensor` | Tensor-product constructions of matrices and vectors; their component conventions need review before use for abstract tensor spaces. |
| [calculus1](https://openmath.org/cd/calculus1.html), official | `defint`, `diff`, `int`, `nthdiff`, `partialdiff`, `partialdiffdegree` | Ordinary and partial calculus vocabulary; `diff` is ordinary differentiation, not automatically the exterior derivative. Further geometry vocabulary needs a separate survey. |

[`arith1#times`](https://openmath.org/cd/arith1.html) is used in OpenMath's
own matrix examples, while the present OSR interpretation is field-valued.
Any overloaded matrix interpretation needs an independently reviewed typed
fragment and ordered product semantics, not a blanket AC rule. `linalg5#scalar`
constructs a scalar matrix, not scalar multiplication; its published prose
contains an arity wording discrepancy with its two-argument FMP. See
[`upstream-bugs.md`](../upstream-bugs.md). We found no trace, inverse,
commutation, typed shape or matrix-exponential symbol in **these five CDs**;
this is not a claim that no other CD exists. Survey and approve each candidate
before assigning a symbol.
The inspected OSR OpenMath snapshot contains `arith1.ocd` and other scalar
CDs but no `linalg1`–`linalg5` files. V1-S-003 requires pinned CD snapshots
and SHA-256 values, so adopting these CDs also needs a reviewed snapshot and
registry integration; the public web pages alone do not satisfy that audit.

## Verification and version pins

The current architecture is **Lean source → audited OpenMath JSON**, not a
general-purpose JSON → Lean `osr2lean` generator. `scripts/Export.lean`
checks the exact expected theorem type, source rule declaration and permitted
axioms before recording proof metadata. Verification's `recheck.sh` checks
the source digest, builds Lean, invokes `just check`/`leanchecker`, reruns the
export and compares published report files byte for byte. This is valuable
infrastructure to reuse, but it does not currently accept arbitrary typed
matrix JSON as input. The pinned environment is `leanprover/lean4:v4.35.0`
and Mathlib [`56a005855ea17e0b0958f73ec801ae140b0a1679`](https://github.com/leanprover-community/mathlib4/tree/56a005855ea17e0b0958f73ec801ae140b0a1679).
No theorem for this research inventory has been generated or proved here.

The prose specification V1-V-001 lists `proved`, `unproved`,
`counterexample`, `unsupported`; the JSON schema additionally permits
`generation_error`. This discrepancy is documented, not silently resolved.
An external report can map UI `refuted` to v1 `counterexample`, retaining a
separate generation-error field; it must not fabricate a theorem.

## Compatibility and future domains

The existing v1 schema closes top-level, rule, OMV and other objects with
`additionalProperties: false`. An existing trigonometry ruleset validated
against the checked-out schema; adding `x-osr-types` to its first rule was
rejected by `check-jsonschema 0.38.0`. A separate sidecar is possible as a
research artifact, but not a normative part of v1 and never safe to ignore
when applying a rule. See [schema proposal](schema-proposal.md).

Reusable foundations are symbol/provenance identities, typed contexts,
side-condition logic, domain-aware interpretation, proof/status auditing and
ordered rewriting. Tensors need type-indexed products, duals and explicit
associators; geometry needs base manifolds, bundles, smoothness, pullbacks,
degree and local/global scope. Component arrays alone cannot encode those
distinctions. No tensor or geometry implementation is authorized here.

## Phase-0 report

- Completed: repository inventory, v0.1/v1, client, OpenMath CDs, Lean pin and
  verification flow; checked actual v1 schema behavior.
- Tests: existing scalar JSON accepted and modified rule rejected, using
  `check-jsonschema 0.38.0`; no external OSR state was modified.
- Blockers for implementation: agreed type/domain extension, reviewed
  vocabulary and CD snapshot strategy, typed proof-to-export bridge, shape
  and condition semantics, independent recheck plan, explicit approvals.
- Open: whether the maintainers prefer an in-schema versioned extension, an
  approved sidecar, or a successor format; whether new OpenMath CDs are
  necessary; formal support for several geometry statements at the pin.
- Recommendation: review phases 1 and 2 before writing the pilot, and do not
  change the official Specification or any existing repository autonomously.
