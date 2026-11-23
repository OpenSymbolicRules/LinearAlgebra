# Phase 2: proposed LinearAlgebra rule inventory

**Design for review only. No rule below is an implemented OSR rule, a generated
Lean theorem, a numerical test result or a certification.** Every item is a
forward rewrite proposal with a mathematical statement, domain and
preconditions. The existing v1 fragment cannot express all of these rules or
their types and assumptions: see [schema proposal](schema-proposal.md).

## Shared conventions

`F` is ℝ or ℂ unless restricted below. Matrices are finite and symbolic;
`A:m×n`, `B:n×p`, `C:p×q` have entries in the same field. Square matrices are
`n×n`, with `n ≥ 1` in this proposed OpenMath fragment. `I_n` is the identity
on the specified space. `T` is transpose, **not** Hermitian adjoint. Inverse
means a partial mathematical inverse, defined only for an invertible square
matrix; `k⁻¹` requires `k ≠ 0`. `A^2` means `AA` and requires square `A`.
For 3D vectors use an oriented real 3D Euclidean inner product space, with
cross product defined by that orientation and metric. `det[u v w]` means
the determinant with columns in a positively oriented orthonormal basis;
it equals the orientation-compatible volume form, independent of that choice.
For matrix exponential, use finite square matrices over ℝ or ℂ with the
usual analytic exponential. No complex Euclidean norm claim is made.

`plus` and `times` in the inventory are notation, not an invented OpenMath
symbol. Candidate existing symbols are `arith1#plus`, `arith1#times`,
`arith1#power`, `linalg1#transpose`, `linalg1#determinant`,
`linalg1#vectorproduct`, `linalg1#scalarproduct`, and experimental
`linalg5#identity`. Trace, inverse, matrix exponential, type and assumption
vocabulary require a CD survey and reviewed interpretation; they are not
silently assigned fabricated CD names. The current `arith1#power` evaluator
is scalar-only, so matrix powers require a separate reviewed typed mapping.

## Proposed directional entries

Exactly **28 independent mathematical identities / 28 proposed directed
entries** follow: transpose 5, trace 4, determinant 5, inverse 3, vectors 6,
matrix exponential 2, associativity/distribution 3. All are **not generated,
unproved in this pilot**, including those with an existing Mathlib candidate.
The alternate orientation `(A^T)⁻¹ → (A⁻¹)^T` is the reverse of T5 and is
not a 29th identity; enabling both would create a loop. Existing proofs in
Mathlib would not by themselves prove a faithful OSR-to-Lean mapping.

| ID | Forward rule and explicit assumptions | Orientation and proposed check |
|---|---|---|
| T1 | `(AB)^T → B^T A^T`; `A:m×n`, `B:n×p` | Push transpose to leaves; order reverses; reject mismatched inner dimensions. |
| T2 | `(A+B)^T → A^T+B^T`; same shape | Push to leaves; expansion; opt-in normalization profile. |
| T3 | `(kA)^T → k A^T`; `k∈F` | Push to leaves; preserves shape. |
| T4 | `(A^T)^T → A`; `A:m×n` | Removes two operations. |
| T5 | `(A⁻¹)^T → (A^T)⁻¹`; `A:n×n`, invertible | One canonical orientation only; reject unknown invertibility. |
| R1 | `tr(A+B) → tr(A)+tr(B)`; square same size | Exposes linearity; expands; optional profile. |
| R2 | `tr(kA) → k tr(A)`; `A:n×n` | Extract scalar. |
| R3 | `tr(AB) → tr(BA)`; `A:m×n`, `B:n×m` | Equality is valid for unequal `m,n`; enable only under a **strict** canonical order to avoid a loop, otherwise manual one-shot. |
| R4 | `tr(A^T) → tr(A)`; square `A` | Removes transpose. |
| D1 | `det(AB) → det(A)det(B)`; same-size square `A,B` | Exposes multiplicativity; can increase size. |
| D2 | `det(A^T) → det(A)`; square `A` | Removes transpose. |
| D3 | `det(kA) → k^n det(A)`; `A:n×n` | Exposes dimension-dependent scalar factor. |
| D4 | `det(A⁻¹) → (det A)⁻¹`; square invertible `A` | Invertibility is essential to intended partial semantics. |
| D5 | `det(I_n) → 1`; `n≥1` | Removes determinant; identity constructor's CD dimension convention applies. |
| I1 | `(AB)⁻¹ → B⁻¹A⁻¹`; same-size square, `A,B` invertible | Reverses order, expands; optional profile. |
| I2 | `(A⁻¹)⁻¹ → A`; square invertible `A` | Removes inverse pair; no reliance on totalized inverse at singular matrices. |
| I3 | `(kA)⁻¹ → k⁻¹A⁻¹`; square invertible `A`, `k≠0` | Extract factor; conditions must be decided. |
| V1 | `u×v → −(v×u)` only when `v` precedes `u` in a fixed order; real oriented Euclidean 3-space | Canonicalizes operand order; plain unconditional anticommutativity is a loop. |
| V2 | `u×u → 0_V`; same 3D setting | Removes product; typed vector zero. |
| V3 | `u·(v×w) → det[u v w]`; same setting, determinant convention above | Exposes oriented scalar volume; requires a reviewed determinant-of-vectors representation. |
| V4 | `u×(v×w) → v(u·w)−w(u·v)`; same setting | Expands a nested cross product; opt-in profile, not a universal size reduction. |
| V5 | `u×(v×w)+v×(w×u)+w×(u×v) → 0_V`; same setting | Whole-pattern Jacobi simplification; matching must preserve structure. |
| V6 | `‖u×v‖² → ‖u‖²‖v‖²−(u·v)²`; same real setting | Removes cross/norm nesting; not the same formula for an arbitrary complex inner product. |
| E1 | `exp(0_(n×n)) → I_n`; real/complex square matrix, `n≥1` | Removes exponential; typed zero and identity. |
| E2 | `exp(A+B) → exp(A)exp(B)`; same-size square `A,B`, `AB=BA` | Expansion; opt-in/one-shot, never unconditional. |
| M1 | `(AB)C → A(BC)`; `A:m×n`, `B:n×p`, `C:p×q` | Chosen right association; inverse direction disabled. |
| M2 | `A(B+C) → AB+AC`; `B,C:n×p`, `A:m×n` | Expansion; separate profile with bounded strategy. |
| M3 | `(A+B)C → AC+BC`; `A,B:m×n`, `C:n×p` | Expansion; separate profile with bounded strategy. |

Use profiles and a documented well-founded strategy; neither the identity nor
these orientations establishes termination of a combined rewrite system. In
particular, do not include both expansion and factoring in the same unguarded
normalizer, or both transpose/inverse orientations. Explicit, proposed
positive and negative applicability checks for the type/condition system are
listed in [schema-proposal.md](schema-proposal.md). The wider set of 15
cross-domain conceptual examples has its own positive and negative tests in
[architecture-research.md](architecture-research.md).

## Six false candidates and exact witnesses

The following are design witnesses, **not a numerical test suite or Lean
counterexamples**. A one-off deterministic Python standard-library arithmetic
probe reproduced the five exact matrix inequalities and the displayed
floating-point exponential values; it is not a proof or a general numerical
validation of the proposed rules. They must be translated into `refuted/`
only after approval.
Each universal proposal is falsified by exhibiting its one valid instance.

1. **Square expansion:** take `A=[[0,1],[0,0]]`, `B=[[0,0],[1,0]]`.
   Then `(A+B)^2=I`, but `A²+2AB+B²=diag(2,0)`. The missing term is `BA`.
2. **Unconditional exponential:** use the same `A,B`. Since `A²=B²=0`,
   `exp(A)exp(B)=[[2,1],[1,1]]`, whereas `exp(A+B)` has diagonal
   `cosh(1)` and off-diagonal `sinh(1)` (approximately 1.543081 and
   1.175201). The matrices do not commute; this is not a formal check.
3. **Determinant of a sum:** for `A=B=I₂`, `det(A+B)=4` and
   `det(A)+det(B)=2`.
4. **Incorrect scalar determinant:** for `A=I₂`, `k=2`, `det(kA)=4` but
   `k det(A)=2`; the correct factor is `k²`.
5. **Inverse product order:** let `A=[[1,1],[0,1]]` and
   `B=[[1,0],[1,1]]`. Both are invertible; `(AB)⁻¹=[[1,-1],[-1,2]]` but
   `A⁻¹B⁻¹=[[2,-1],[-1,1]]`.
6. **Multiplicative trace:** for `A=B=I₂`, `tr(AB)=2` whereas
   `tr(A)tr(B)=4`.

All witnesses have exact rational entries; a future deterministic numerical
runner should independently reproduce them, use a tolerance and documented
error control for exponentials, and generate exact Lean counterexamples where
feasible. Numerical evaluation never counts as proof. Six is the refutation
inventory count, not six verified counterexamples.

## Phase-2 report

Completed: 28 proposed directed identities, six false proposals with concrete
witnesses, assumptions, dimensions and rewrite orientation. The six witnesses
were checked once by the standard-library arithmetic probe described above.
Formal state: **0 generated, 0 proved, 0 refuted by Lean, no rule test suite**;
all 28 are design-only, and formal eligibility is **not yet assessable**
until types, vocabulary and mapping are accepted. Tests in the tables are
specifications, not claims of execution. Review the choice of algebraic
structures, profile orientation and CD mappings before approving implementation.
