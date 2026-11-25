# Typed vector rewrites

The [six generated rules](../examples/vector-identities.json) use the
experimental profile `linear_algebra.euclidean_vectors/0.1.0`. Each rule
binds symbolic vectors in real three-dimensional Euclidean space with a
standard right-handed orthonormal basis. A reader must recognize all four
space fields, the real carrier and the variable declarations before using a
rule. In this model `e₁ × e₂ = e₃`. Complex and indefinite inner products
require different interpretations.

| ID after `linear_algebra.` | Forward rewrite | Application |
|---|---|---|
| `cross_anticommutative` | u × v → −(v × u) | Sort a pair of variable operands once, under the guard below. |
| `cross_self` | u × u → 0ᵥ | Eliminate a repeated operand. The result is a vector. |
| `scalar_triple_columns` | u · (v × w) → det[u v w] | Opt-in expansion exposing signed volume. The operands are columns in this order. |
| `vector_triple` | u × (v × w) → (u · w)v − (u · v)w | Opt-in expansion removing nested cross products. |
| `cross_jacobi` | u × (v × w) + v × (w × u) + w × (u × v) → 0ᵥ | Simplify the full cyclic sum. |
| `lagrange_norm` | ‖u × v‖² → ‖u‖²‖v‖² − (u · v)² | Express the squared area using scalar quantities. |

The mathematical conditions list is empty because the space supplies all
required structures. The separate `application_guard` controls direction.
For `strict_variable_name_order`, look up the matched objects named by
`less` and `greater`. Both must be bare OpenMath variables with nonempty
names. Compare their unchanged names lexicographically by Unicode code point.
For example, `z × a` can become `−(a × z)`. Equal names, a pair already
in order, compound operands and missing bindings disable the swap. An
unrecognized guard must disable application. Other entries carry a null guard.

## Encoding the determinant of three columns

The OpenMath outer product of vectors a and b has entries aᵢbⱼ. Therefore
the matrix with columns u, v and w is the sum of the outer products of u
with e₁, v with e₂ and w with e₃. Only the three fixed basis vectors are
written out in JSON. All three input vectors remain symbolic. The Lean
proof first checks the matrix equality itself, since a determinant alone
cannot distinguish a matrix from its transpose. [Outer product](https://openmath.org/cd/linalg1.html#outerproduct)
and [column vectors](https://openmath.org/cd/linalg3.html#vector).

The profile uses the three-dimensional vector product and real scalar
product from `linalg1`, the unary Euclidean norm from `norm1`, and the
length-three zero vector from `linalg4vec`. Integer powers in this fragment
are squares of real scalars. The mappings rely on the published operator
descriptions. The [upstream observations](../upstream-bugs.md) record
discrepancies in two associated formal properties. [Vector and scalar products](https://openmath.org/cd/linalg1.html),
[Euclidean norm](https://openmath.org/cd/norm1.html#Euclidean_norm) and
[zero vector](https://openmath.org/cd/linalg4vec.html#zero).

## Reproducing the checks

`just lean OSR-Lean` compiles the proofs with the pinned project and compares
the generated JSON with the tracked file. For every assignment, Lean requires
the exact two OpenMath trees to evaluate to the same **defined** value.
Its interpreter dispatches on content dictionary, symbol, arity and operand
types. Undeclared variables and unsupported signatures yield no value.
`just test` independently reads the JSON, checks the six directed formulas,
exercises the order guard, checks the actual columns with a nonsymmetric
matrix and tests signed volume and squared norm on real inputs.
[Lean source](https://github.com/OpenSymbolicRules/LinearAlgebra/blob/main/verification/VectorExamples.lean)
and [environment and export status](../reports/status.md).
