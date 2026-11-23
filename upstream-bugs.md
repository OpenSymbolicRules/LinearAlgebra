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
