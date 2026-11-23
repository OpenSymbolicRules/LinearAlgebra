# CAS interoperability assessment

This is documentation research, not an implemented adapter or a live CAS
conformance test. OSR's representation, semantic interpretation, proof and
CAS execution are separate. No listed CAS is a required dependency. A future
adapter must preserve ordered multiplication, domain and codomain, symbolic
shapes, assumptions, orientation and exact symbol meaning; it must reject a
rule it cannot translate faithfully. Native simplification is not a proof.

| System | Evidence for native objects | Conditions / order / direction | OSR import and unresolved gaps |
|---|---|---|---|
| Giac/Xcas | [Xcas reference](https://www-fourier.univ-grenoble-alpes.fr/~parisse/giac/doc/xcasen.html) documents matrices as vectors of vectors and matrix operations; [Giac API](https://xcas.univ-grenoble-alpes.fr/backup/giac_us.html) documents the library. | Ordered products of explicit matrices are available; fully abstract symbolic-shape matching and durable invertibility/commutation assumptions were **not verified**. | No OSR importer was found or tested in this investigation. A wrapper for abstract matrix objects and condition negotiation needs investigation; do not equate ordinary scalar symbols with matrix variables. |
| SymPy | [Matrix expressions](https://docs.sympy.org/latest/modules/matrices/expressions.html) describe `MatrixSymbol`, `MatMul`, `Transpose`, `Inverse`, shape and `Trace`. | `MatMul` retains matrix factors; scalar/matrix distinction and shape checks exist. Assumption inference and an exact one-step orientation still need adapter tests; automatic evaluation may transform a requested result. | No OSR importer or typed-conditions adapter was established. [diffgeom](https://docs.sympy.org/latest/modules/diffgeom.html) has manifolds, differential forms and tensor products, with coordinate-related limitations; it is not proof of complete intrinsic geometry interoperability. |
| Symbolics.jl | [Symbolic arrays](https://docs.sciml.ai/Symbolics/stable/manual/arrays/) document non-expanded array expressions and shape metadata. | Array operations can retain shape, but coverage and representation vary by operation. Verify explicit assumptions, noncommutative order and one-step rewriting before asserting support. | Independent Julia consumer, not OSR's semantic authority. Existing OSRv1 loader is a syntactic OpenMath consumer and has no demonstrated typed matrix-rule support; no adapter was built. |
| Wolfram Language | [`MatrixSymbol`](https://reference.wolfram.com/language/ref/MatrixSymbol.html) supports symbolic dimensions/domains; [noncommutative algebra](https://reference.wolfram.com/language/tutorial/NonCommutativeAlgebras.html) has explicit noncommuting products. | A phrasebook must map matrix multiplication and assumptions to the right constructs and control evaluation and orientation; `Times`, `Dot` and `NonCommutativeMultiply` must not be conflated. | No OSR import or execution was tested. Native tensor capabilities do not imply a verified OSR rule mapping. |
| Maple | [Physics](https://www.maplesoft.com/support/help/AddOns/view.aspx?path=Physics) and [Vectors](https://www.maplesoft.com/support/help/maple/view.aspx?path=Physics%2FVectors) document noncommutative algebra, abstract vectors and tensor capabilities. [Dot](https://www.maplesoft.com/support/help/view.aspx?L=E&path=dot) is noncommutative but has operation-specific behavior. | Translate types and assumptions explicitly; do not assume that similarly printed `.` and scalar multiplication have identical meaning or shape behavior. | No OSR importer, conditions round trip or proof correspondence was tested. DifferentialGeometry/Physics support is not a guarantee of intrinsic-rule compatibility. |

## Representative translation to validate later

For `A:2×3`, `B:3×4`, represent the OpenMath product as an ordered node;
check the target has a native `2×4` result and that `B*A` is rejected or
different. Translate `(AB)^T → B^TA^T` only with compatible dimensions, then
verify the target has not pre-evaluated the proposed left side. For
`tr(AB) → tr(BA)`, test `A:2×3`, `B:3×2` to avoid accidentally enforcing
identical sizes. For `exp(A+B) → exp(A)exp(B)`, test unknown commutation as
**blocked**, not as permission to rewrite. Translate inverse only under the
same partiality convention and preserve an explicit condition.

Future conformance suites should verify parse/serialize round trips, source
identity, semantic assumptions, negative shape checks, ordered rewriting,
and behavior when a condition is unknown. Adapters must not silently discard
a sidecar, rewrite in reverse, or convert `proved` into a claim that the CAS
matcher is formally verified. Record software versions and test actual
implementations before publishing a compatibility matrix with stronger claims.
