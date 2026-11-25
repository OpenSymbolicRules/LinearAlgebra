# Six typed matrix rewrites

The [generated JSON examples](../examples/matrix-identities.json) contain six
forward rewrites on abstract rectangular matrices. A consumer needs only the
JSON to inspect their operands, dimensions, carrier and direction. Their
experimental profile is `linear_algebra.matrix_examples/0.1.0`. Only a consumer
that understands this profile and checks its context should enable these examples.

| Inventory | JSON ID after `linear_algebra.` | Forward rewrite | Shapes in operand order |
|---|---|---|---|
| T1 | `transpose_product` | (AB)ᵀ → BᵀAᵀ | m×n, n×p |
| T2 | `transpose_sum` | (A+B)ᵀ → Aᵀ+Bᵀ | m×n, m×n |
| T4 | `transpose_twice` | (Aᵀ)ᵀ → A | m×n |
| M1 | `multiply_associative` | (AB)C → A(BC) | m×n, n×p, p×q |
| M2 | `distribute_left` | A(B+C) → AB+AC | m×n, n×p, n×p |
| M3 | `distribute_right` | (A+B)C → AC+BC | m×n, m×n, n×p |

Dimension names are local to a rule. Assign each a positive integer and use
one carrier, ℝ or ℂ, for all operands. For T1, setting m=2, n=3 and p=4
gives a 4×2 result on both sides. Binding B to a 4×2 matrix would make AB
undefined. No entry has a further algebraic premise. T4 removes two operators.
T1 and T2 push transposes toward variables. M1 chooses right association. M2
and M3 expand sums and belong in an opt-in expansion strategy.

## Symbols and verification

Each pattern and replacement uses the existing OpenMath object encoding.
The profile interprets binary addition on matrices of equal shape, binary
multiplication on matrices with a shared inner dimension, and unary transpose.
Multiplication preserves operand order. Complex transpose leaves entries
unconjugated. The OpenMath multiplication dictionary includes a matrix product
example. [Addition and multiplication](https://openmath.org/cd/arith1.html#times)
and [transpose](https://openmath.org/cd/linalg1.html#transpose).

In Lean, a variable selects both its name and its matrix type from one
declaration. Each operation constructs an OSR OpenMath object and its Mathlib
interpretation together. The row and column indices constrain how the objects
can be composed. Each example supplies a proof that its two interpretations
agree for every assignment. The proofs work over a commutative semiring of
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
three symbol mappings. A normative typed context, a reviewed registry
interpretation and an independent OSR Verification record are still required
for v1 certification. The mappings in this pilot cover only these signatures.
See the [schema proposal](schema-proposal.md).
