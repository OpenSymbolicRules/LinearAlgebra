# Mathlib mapping at the existing pin

This started as a source inspection. Subsequently, 28 hand-written
corresponding mathematical statements were compiled; see the
[status report](../reports/status.md) for their precise limits. They are not
generated theorems or an assertion that OSR can ingest these objects. Checked
on geekr9 in the existing
Mathlib checkout at commit
[`56a005855ea17e0b0958f73ec801ae140b0a1679`](https://github.com/leanprover-community/mathlib4/tree/56a005855ea17e0b0958f73ec801ae140b0a1679),
with `leanprover/lean4:v4.35.0`. The pin was not changed. Names below were
looked up in that checkout; intended application, imports, assumptions and
statement equivalence still need compilation and semantic review.

| OSR concept | Inspected Mathlib type or declaration | Existing candidate / classification | Notes |
|---|---|---|---|
| Finite `m×n` matrix | `Matrix (Fin m) (Fin n) R` | Existing matrix type | A function on two finite index types, not an abstract linear map; users need not expand components. |
| Linear operator | `LinearMap R V W` | Existing type | Domain/codomain and basis transformations are explicit; a matrix is basis-dependent. |
| Matrix product and matrix-vector application | `Matrix.mul_assoc`, `Matrix.mul_add`, `Matrix.add_mul`, `Matrix.mulVec`, `Matrix.mulVec_add` | Existing declarations in [`Data/Matrix/Mul.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Data/Matrix/Mul.lean) | Rectangular shapes and finite intermediate index; never rewrite by commutativity. |
| Transpose | `Matrix.transpose_transpose`, `Matrix.transpose_add`, `Matrix.transpose_smul`, `Matrix.transpose_mul` | Existing declarations | The inspected `transpose_mul` requires commutative entry multiplication. `Aᵀ` is not conjugate transpose. |
| Trace | `Matrix.trace_add`, `Matrix.trace_smul`, `Matrix.trace_transpose`, `Matrix.trace_mul_comm` | Existing declarations in [`Trace.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/LinearAlgebra/Matrix/Trace.lean) | `trace_mul_comm` explicitly accepts `A : Matrix m n R`, `B : Matrix n m R`; it is not limited to same-size square inputs. |
| Determinant | `Matrix.det`, `Matrix.det_mul`, `Matrix.det_transpose`, `Matrix.det_smul`, `Matrix.det_one` | Existing declarations in [`Determinant/Basic.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean) | Finite square matrices over the file's commutative coefficient structure; scalar exponent is `Fintype.card n`. |
| Inverse / invertibility | `Matrix.nonsing_inv_apply_not_isUnit`, `Matrix.nonsing_inv_mul`, `Matrix.nonsing_inv_nonsing_inv`, `Matrix.transpose_nonsing_inv`, `Matrix.mul_inv_rev`, `Matrix.det_nonsing_inv`; `IsUnit A.det`, `Invertible A` | Existing declarations in [`NonsingularInverse.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean) | Matrix `A⁻¹` is **totalized to zero** when `det A` is not a unit. Some lemmas, including `mul_inv_rev`, are stated without the intended OSR inverse-domain premises. Keep explicit invertibility/definedness even when a totalized identity compiles. |
| Identity | `(1 : Matrix n n R)`, `Matrix.det_one` | Existing instance/declaration | Match finite index type and the OpenMath identity constructor's positive-dimension restriction. |
| Exponential | `Matrix.exp_add_of_commute`, `NormedSpace.exp_zero` | Existing candidates in [`MatrixExponential.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Analysis/Normed/Algebra/MatrixExponential.lean) and [`Exponential.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/Analysis/Normed/Algebra/Exponential.lean) | `Matrix.exp_add_of_commute` explicitly requires `Commute A B`, finite indices, normed ring/algebra and completeness assumptions. Both specializations compile for real and complex matrices. |
| Cross product | `crossProduct`, `cross_anticomm`, `cross_self`, `cross_cross_eq_smul_sub_smul` | Existing declarations in [`CrossProduct.lean`](https://github.com/leanprover-community/mathlib4/blob/56a005855ea17e0b0958f73ec801ae140b0a1679/Mathlib/LinearAlgebra/CrossProduct.lean) | Defined on `Fin 3 → R` with a chosen coordinate orientation. Transferring to an abstract oriented Euclidean space needs an explicit orientation-compatible isometry, not an arbitrary basis. |
| Dot product / norm identities | `Matrix.dotProduct`, inner product structures | Existing notions; exact identity-to-OpenMath mapping needs verification | Dot product and complex Hermitian inner product are not interchangeable. The checked proofs use `jacobi_cross`, `cross_dot_cross`, `real_inner_self_eq_norm_sq` and `EuclideanSpace.inner_eq_star_dotProduct`. |
| Tensor product / multilinearity | `Mathlib/LinearAlgebra/TensorProduct`, `Mathlib/LinearAlgebra/Multilinear/TensorProduct` | Existing source directories | Associators are equivalences, not definitional equality in an arbitrary model. Full mappings are postponed. |
| Tangent and covariant derivative | `Mathlib/Geometry/Manifold/VectorBundle/Tangent.lean`, `.../CovariantDerivative/{Basic,LeviCivita,Torsion,Metric}.lean` | Existing source files | Existence of files is not a claim that all exterior-calculus or curvature identities in the research table are available at this pin. Exact declarations, hypotheses and convention compatibility need separate audit. |

## Proof and verification contract to review

The current producer is the existing [Lean-native exporter](https://github.com/OpenSymbolicRules/Lean/blob/68f25be/scripts/Export.lean),
not a generic `osr2lean` compiler. A compatible extension must state the
typed rule and the semantic interpretation as Lean data, generate the exact
corresponding theorem from the same data, check the theorem statement and
axioms, and export via an approved path. Alternatively, a new JSON-to-Lean
translator would itself need a reviewed correspondence proof, hard errors for
unknown symbols and an independent audit; it does not currently exist in the
inspected repositories. Do not implement either path without authorization to
modify the relevant repository or approve an integration boundary.

For a square matrix over ℝ/ℂ, `IsUnit A.det` is a candidate invertibility
condition; `[Invertible A]` is another Mathlib interface. Verify equivalence
under the chosen finite-dimensional hypotheses, and represent scalar `k ≠ 0`
explicitly. `Commute A B` is a candidate for E2. Rectangular multiplication
types enforce matching index types once translated, but symbolic dimension
unification must be checked **before** constructing the Lean term.

An accepted certificate must cover the conditional OSR statement and the
correct CD interpretation, not a theorem that happens to hold because of
totalization. Preserve OSR's axiom allowlist and per-domain mapping assurance;
`sorry`, omitted premises, unknown symbols or arbitrary fallback mappings are
not proofs. `counterexample` is the v1 status corresponding to a UI label
`refuted`; `generation_error` exists in the schema but not V1-V-001 prose.

## Candidate coverage and status

Six of the 28 entries use typed Lean operands and the pinned OSR OpenMath
encoder in the [matrix examples](matrix-examples.md). Official v1 certification
requires a reviewed typed registry and independent recheck. Hand-written mathematical
counterparts compile, including the explicit inverse premises and commutation
hypothesis; this does not complete the semantic bridge. The column determinant and Euclidean squared norm formulations compile in
the standard oriented real coordinate space. Coordinate-free transport remains
open. All six proposed false rules have compiled concrete Lean witnesses.
For the exponential witness, `NormedSpace.exp_eq_tsum` reduces the exponential
of a square-zero matrix to `1 + A`, and `Commute.exp_right` forces the sum to
commute with its exponential. No eligibility percentage is asserted before reviewing
all typed translations. See the current [status report](../reports/status.md).
