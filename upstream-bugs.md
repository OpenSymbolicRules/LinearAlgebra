# Upstream observations

These observations have **not** been filed or fixed upstream. They are
recorded for maintainers to verify against the cited releases; none authorizes
editing an external repository.

## OpenMath `linalg5` v3 revision 2: scalar-matrix arity wording

In the [published `linalg5` CD](https://openmath.org/cd/linalg5.html), dated
2004-05-11, version 3 revision 2, the `scalar` description says it takes two
arguments but refers to a “third” scalar argument. Its FMP and example use
two arguments, `scalar(n,s)`. This is a reproducible documentation ambiguity;
the proposal should rely on the FMP and examples only after CD maintainer
confirmation, and must not invent a third argument.

## OpenMath `linalg5` v3 revision 2: apparent unbound symmetry claim

The [published `symmetric` FMP](https://openmath.org/cd/linalg5.html#symmetric)
expresses `symmetric(VV1) + transpose(symmetric(VV1)) = symmetric(VV2)`
without a stated relationship between `VV1` and `VV2`. Read as a universally
valid equation over independent arguments, it is false: take one-dimensional
`VV1=[[1]]` and `VV2=[[0]]`, giving `2 ≠ 0`. The prose appears intended to
say the sum is *a* symmetric matrix. Confirm the interpretation and any
OpenMath binding convention with the upstream maintainers before reporting or
using that FMP as an obligation. `linalg5#symmetric` is a constructor, not a
predicate. Do not classify this note as a formal proof or an upstream fix.

## Vector dictionary observations

- In `norm1` v1 revision 2, the description and the first application in the
  FMP identify a unary Euclidean norm. The remainder of the equality lists
  the `L_norm` symbol, 2 and the vector separately. Comparison with the
  description suggests an omitted application around those last three objects.
  [CD definition](https://openmath.org/cd/norm1.html#Euclidean_norm).
- In `linalg4vec` v2 revision 1, the first two matrix multiplication properties
  of `zero` interchange the row and column dimensions. For a 2×3 matrix
  the matrix-times-column product needs a length-three vector and returns a
  length-two vector. The profile uses only the unary zero-vector constructor.
  [CD definition](https://openmath.org/cd/linalg4vec.html#zero).
- In `linalg3` v3 revision 1 the matrix constructor takes matrix columns. Its
  STS signature instead names `MatrixRow`, and the standalone vector signature
  returns `Vector`. The vector profile constructs columns with outer products.
  [CD definition](https://openmath.org/cd/linalg3.html#matrix) and
  [STS signature](https://openmath.org/sts/linalg3.sts).
