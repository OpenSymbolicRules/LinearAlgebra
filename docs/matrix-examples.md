# Typed matrix rewrites

The [generated JSON examples](../examples/matrix-identities.json) contain eleven
forward rewrites on abstract scalar and matrix operands. A consumer needs only the
JSON to inspect their operands, dimensions, carrier and direction. Their
experimental profile is `linear_algebra.matrix_examples/0.2.0`. Only a consumer
that understands this profile and checks its context should enable these examples.

| Inventory | JSON ID after `linear_algebra.` | Forward rewrite | Shapes in operand order |
|---|---|---|---|
| T1 | `transpose_product` | (AB)ᵀ → BᵀAᵀ | m×n, n×p |
| T2 | `transpose_sum` | (A+B)ᵀ → Aᵀ+Bᵀ | m×n, m×n |
| T4 | `transpose_twice` | (Aᵀ)ᵀ → A | m×n |
| M1 | `multiply_associative` | (AB)C → A(BC) | m×n, n×p, p×q |
| M2 | `distribute_left` | A(B+C) → AB+AC | m×n, n×p, n×p |
| M3 | `distribute_right` | (A+B)C → AC+BC | m×n, m×n, n×p |
| T3 | `transpose_scalar` | (kA)ᵀ → kAᵀ | scalar k, m×n |
| D1 | `determinant_product` | det(AB) → det(A)det(B) | n×n, n×n |
| D2 | `determinant_transpose` | det(Aᵀ) → det(A) | n×n |
| D3 | `determinant_scalar` | det(kA) → kⁿ det(A) | scalar k, n×n |
| D5 | `determinant_identity` | det(Iₙ) → 1 | positive integer n |

Dimension names are local to a rule. Assign each a positive integer and use
one carrier, ℝ or ℂ, for all operands. For T1, setting m=2, n=3 and p=4
gives a 4×2 result on both sides. Binding B to a 4×2 matrix would make AB
undefined. No entry has a further algebraic premise. T4 removes two operators.
T1 and T2 push transposes toward variables. M1 chooses right association. M2
and M3 expand sums and belong in an opt-in expansion strategy.

The determinant returns a scalar. D2 and D5 remove an operation. D1 exposes
the two scalar determinants and D3 extracts the scalar factor. D3 applies to
singular matrices and to k=0. For example, k=2 and A=I₃ give 8 on both
sides. The exponent comes from the declared matrix size. In D5 the dimension
is bound directly by the identity constructor. T3 moves the transpose to A.

Profile 0.2.0 adds scalar variables, scalar results, integer literals and
positive dimension arguments to the six records from profile 0.1.0. Each
OpenMath variable name refers either to a matrix or scalar in
`context.variables`, or to a positive size in `context.dimensions`. Names
must be disjoint. A consumer must recognize the profile before applying its
rules. The [earlier JSON](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/668e228/examples/matrix-identities.json)
remains available at its published commit.

## Symbols and verification

Each pattern and replacement uses the existing OpenMath object encoding.
The profile interprets binary addition on matrices of equal shape, binary
multiplication on matrices with a shared inner dimension, and unary transpose.
Multiplication preserves operand order. Complex transpose leaves entries
unconjugated. The OpenMath multiplication dictionary includes a matrix product
example. [Addition and multiplication](https://openmath.org/cd/arith1.html#times)
and [transpose](https://openmath.org/cd/linalg1.html#transpose).

For D1–D5 in the table, `linalg1#determinant` takes one square matrix.
The experimental `linalg5#identity` takes one positive integral dimension.
The D3 signature of `arith1#power` takes a scalar base and a dimension
exponent. `arith1#times` resolves to scalar multiplication, scalar action on
a matrix or ordered matrix multiplication according to its operand types.
[Determinant](https://openmath.org/cd/linalg1.html#determinant),
[identity](https://openmath.org/cd/linalg5.html#identity) and
[power](https://openmath.org/cd/arith1.html#power).

In Lean, a variable selects both its name and its scalar or matrix type from one
declaration. Each operation constructs an OSR OpenMath object and its Mathlib
interpretation together. The row and column indices constrain how the objects
can be composed. Each example supplies a proof that its two interpretations
agree for every assignment. The proofs work over a commutative ring of
**entries** and hence apply to both advertised carriers. The same objects are
serialized by the pinned OSR encoder. [Example declarations](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/main/verification/MatrixExamples.lean)
and [OSR OpenMath encoder](https://github.com/OpenSymbolicRules/Lean/blob/22cf025/OSR/OMObject.lean).

Run `just test` to read the JSON independently, check operand order and
symbolic shapes, and exercise rectangular real and complex samples. Run
`just lean OSR-Lean` in the environment described in the [status
report](../reports/status.md) to rebuild the examples and compare every byte.
To regenerate the file after editing the Lean source, first build
`OSR.OMObject` in that checkout, then run the following from the pilot root.

```sh
(cd OSR-Lean && lake env lean -DwarningAsError=true --run ../verification/MatrixExamples.lean) > matrix-examples.new.json &&
  mv matrix-examples.new.json examples/matrix-identities.json
```

The experimental envelope keeps the context and expressions together. The
comparison checks reproducibility, and the independent consumer tests the
exported symbol signatures. A normative typed context, a reviewed registry
interpretation and an independent OSR Verification record are still required
for v1 certification. The mappings in this pilot cover only these signatures.
See the [schema proposal](schema-proposal.md).
