# Proposal: typed abstract objects and conditional rewriting

**Discussion draft, not OSR v1, not an implemented JSON Schema.** This document
does not change Specification. Its examples are design fragments, not exported
rules or certificates. The current v1 draft forbids arbitrary extension fields
on a ruleset, rule and `OMV`; a proposed field is not valid there merely because
it begins with `x-`. See [the v1 schema](https://github.com/OpenSymbolicRules/Specification/blob/eb12fb1/schemas/v1/ruleset.schema.json)
and [the v1 requirements](https://github.com/OpenSymbolicRules/Specification/blob/eb12fb1/docs/osr-v1.md).

The [six matrix examples](matrix-examples.md) exercise symbolic dimensions and
forward rewrites in a single experimental envelope. They supply evidence for
reviewing this proposal. The normative migration choice remains open.

## Proposed minimal contract

1. Keep OSR rules and OpenMath expressions, with one portable `OMS` identity
   per operator; do not introduce a competing expression language.
2. Add a **versioned, mandatory-to-understand** rule context: declarations for
   scalar carriers, dimension variables, object types, and explicit structural
   and mathematical conditions. Each variable in it refers to an existing
   `OMV`, and each dimension is a natural literal or a declared dimension
   variable, not an implicitly quantified scalar metavariable.
3. Type-check both sides and conditions with signature rules before enabling a
   rewrite. A failed or undecided dimension, domain, definedness, assumption,
   registry mapping or proof check must prevent application. Type equality is
   not the same as structural equality of printed dimension expressions.
4. Associate symbol interpretations with **signatures**, carrier structures
   and domains, not only an unqualified operator name and `real`/`complex`
   label. Matrix and scalar multiplication may share a reviewed CD symbol if
   its overload is made unambiguous; do not reuse the existing scalar-field
   Lean interpretation as though it were a matrix interpretation.
5. Preserve operand order in product trees. Associative flattening may preserve
   the list `[A,B,C]`; it must not sort or permute it. A matcher may reorder
   only when a specific rule has a proved/decided commutation premise.

The smallest initial scope is finite matrices over ℝ and ℂ and three-dimensional
real Euclidean vectors. Generic vector spaces, named fields, operators, and
noncommutative scalar rings need explicit later contracts, not hidden defaults.
All dimensions in the first pilot should be positive naturals while
`linalg5#identity` requires a positive dimension; supporting zero-dimensional
identities needs an explicit CD/fragment decision. Index types, basis choices,
transpose versus adjoint, scalar extension and equality of spaces need their
own semantics.

## Proposed type context: illustrative JSON sidecar

The following is ordinary JSON for a **proposed separate sidecar**; it is not
a current OSR ruleset or a validated schema instance. `example.*` names are
local labels in this proposal, **not OpenMath symbols**. A future specification
must fix the sidecar schema, digest linkage, canonicalization and namespace.

```json
{
  "proposal_version": "0.1.0",
  "rule_id": "linear_algebra.transpose_product",
  "dimensions": {"m": {"min": 1}, "n": {"min": 1}, "p": {"min": 1}},
  "scalar_domain": "http://www.openmath.org/cd/setname1#R",
  "variables": {
    "A": {"kind": "matrix", "rows": "m", "columns": "n"},
    "B": {"kind": "matrix", "rows": "n", "columns": "p"},
    "u": {"kind": "vector", "dimension": "n", "space": "R^n"},
    "k": {"kind": "scalar"}
  },
  "required_checks": ["same_scalar_domain", "ordered_product"]
}
```

The string `R^n` is an illustrative local space identifier, not a published
OpenMath symbol; a normative design must bind it to an identified space and
scalar carrier rather than parse its spelling. The sidecar is keyed by rule
ID **and must be bound to the exact canonical ruleset digest** in a future
version. In production it cannot be optional metadata: a consumer that cannot
interpret the context must reject/disable its rules, rather than fall back to
untyped rewriting. Signing/versioning and semantic-closure validation of the
pair must also be specified. This sidecar is a transition *option*, not a
claim that the pair complies with V1-P-002 or the v1 specification.

### OpenMath expression fragment

The following is a valid JSON *fragment*, not a complete schema-validated
ruleset. It uses actual OpenMath `OMS` names, but has no registry
interpretations or proof record. It expresses `(A B)^T`; the type context above
is necessary to determine that `A B` has shape `m × p`.

```json
{
  "kind": "OMA",
  "applicant": {"kind": "OMS", "cd": "linalg1", "name": "transpose"},
  "arguments": [{
    "kind": "OMA",
    "applicant": {"kind": "OMS", "cd": "arith1", "name": "times"},
    "arguments": [{"kind": "OMV", "name": "A"}, {"kind": "OMV", "name": "B"}]
  }]
}
```

The proposed right-hand side is `times(transpose(B), transpose(A))`: its
shape is `p × m`. A vector example is `times(A,u) : R^m` for `A : R^(m×n)`
and `u : R^n`; that overload is a proposed, reviewed interpretation and not a
claim that the present scalar evaluator supports it. A square-matrix example
binds both dimensions to one `n`; an operator example should instead declare
`L : V → W` with identity of its actual domain and codomain. A scalar example
retains the existing trigonometry v1 ruleset byte-for-byte: it needs no matrix
context and continues to validate under its existing schema and specification.

Additional proposed declarations, again a sidecar fragment rather than v1
rule JSON, cover square matrices, fixed dimension, and maps between named
spaces. `V` and `W` are context identifiers whose declarations and equality
must be supplied by a future contract; they are not OpenMath CDs.

```json
{
  "dimensions": {"n": {"min": 1}},
  "variables": {
    "S": {"kind": "matrix", "rows": "n", "columns": "n"},
    "v": {"kind": "vector", "dimension": 3, "space": "R3"},
    "L": {"kind": "linear_map", "domain": "V", "codomain": "W"}
  }
}
```

For an inverse rule over ℝ or ℂ, this **OpenMath JSON fragment** expresses
the condition `det(S) ≠ 0`; it is syntactically JSON but is not a complete
v1 rule and the current Lean scalar registry cannot interpret matrix
determinants. For other scalar rings, nonsingularity must be stated using the
right unit/invertibility notion rather than just a nonzero determinant.

```json
{
  "kind": "OMA",
  "applicant": {"kind": "OMS", "cd": "relation1", "name": "neq"},
  "arguments": [
    {"kind": "OMA", "applicant": {"kind": "OMS", "cd": "linalg1", "name": "determinant"},
     "arguments": [{"kind": "OMV", "name": "S"}]},
    {"kind": "OMI", "integer": 0}
  ]
}
```

## Categories and constraints

| Category | Example | Proposed checking behavior |
|---|---|---|
| Type | `k ∈ ℝ`, `A : Mat(ℝ,m,n)`, `u : Vec(ℝ,n)` | Assignment/matcher checks object and scalar carrier; no implicit coercion. |
| Structural | `columns(A)=rows(B)`, `rows(A)=columns(A)`, `dim(u)=3` | Shape inference/unification using declared natural dimensions; unresolved is not true. |
| Assumption | `invertible(A)`, `commute(A,B)` | Proposition supplied by context or proved by a decision service; never infer from shape. |
| Preconditions | required assumptions for a particular rewrite, e.g. `k≠0` | Matcher checks all before applying; inverse is undefined outside its intended domain. |
| Derived fact | `AB` is `m×p`, `transpose(A)` is `n×m` | Inference result with proof/evidence, not a new user assumption. |

For finite matrices over ℝ/ℂ, invertibility can be represented mathematically
by `det(A) ≠ 0` once typed determinant, inequality and its mathematical
interpretation are in scope; that equivalence should not be generalized
silently to arbitrary rings. Commutation can use `eq(times(A,B),times(B,A))`
for same-size square matrices, and symmetry `eq(transpose(A),A)`. Orthogonal
over ℝ requires square `A` and `A^T A = I`; complex unitary uses `A* A = I`
and is distinct. Diagonality needs a clear basis-specific predicate;
positive-definiteness needs an ordered real or Hermitian setting. These are
**not current v1 condition implementations**. Do not use `linalg5#symmetric`
as a predicate: it is a constructor.

## Type and assumption test cases

All are proposed semantic conformance tests; none has been executed here.

| Situation | Expected result |
|---|---|
| `A:m×n`, `B:n×p` | `AB:m×p`, transpose product has type `p×m`. |
| `A:m×n`, `B:q×p`, context proves `n=q` | Eligible only after the equality is established. |
| `A:2×3`, `B:4×2` | Reject product: `3 ≠ 4`. |
| `A:2×3`, `B:3×2` | `tr(AB)=tr(BA)` is eligible, although square result sizes are 2 and 3. |
| `det(A)` with `A:2×3` | Reject as ill-typed. |
| `transpose(inv(A))` with square `A` but unknown invertibility | Do not apply; unknown is not false and not true. |
| `inv(kA)` with `k=0` | Reject that rule's nonzero premise. |
| `A×B` with two arbitrary matrix variables | Never reorder solely because product is associative. |
| `u×v` for vectors of dimension 4 | Reject; 3D Euclidean cross-product interpretation is unavailable. |
| scalar trigonometry v1 file with no sidecar | Existing scalar validator and semantics remain unchanged. |

## Backward compatibility and deployment choices

* **JSON syntax:** a JSON object can contain an extra key, but syntax alone
  establishes no OSR meaning.
* **Current official v1 schema:** the test in [recon](recon.md) rejects the
  extra rule key. A schema accepting it would be a different, proposed schema.
* **Current normative v1:** V1-P-002 requires generated artifacts; a
  hand-written sidecar neither makes a file generated nor creates Lean
  certification. V1-R-005 does not provide general typing or properties.
* **Option A:** introduce an explicit versioned schema/consumer capability,
  with strict fail-closed semantics and migration rules. A closed old consumer
  rejects rather than misinterprets the new format. Negotiate the version with
  maintainers; do not call it backwards-compatible solely because old files
  still validate against a revised schema.
* **Option B:** a separately versioned sidecar linked by digest, enabled only
  through an explicit typed-profile capability. Existing schema validation of
  the *unchanged* v1 document remains possible, but an old consumer cannot
  safely claim support for, or apply, the sidecar-dependent rules. A schema-
  valid legacy payload alone is not a complete portable rule contract.

The requested claim that arbitrary typed `x-` fields remain valid under the
unchanged current v1 schema is false. v0.1 operator extension points do not
change that conclusion. Preserve existing scalar files, compare conformance
suites and proof digests, and prohibit silently relabeling a document as v1.

## Future domain fit and open decisions

The same context/registry/audit framework can eventually carry spaces,
domains/codomains, dimension equations and properties for multilinear maps.
Tensor products need specified associators and duality; variance is not merely
an array-axis flag. Geometry needs base spaces, bundles, sections, smoothness,
degree, local/global scope, pullback/pushforward and connection/metric choices.
Those are separate mathematical vocabularies and are not defined by this
pilot. Open questions: CD candidate publication and cdbase/versioning; typing
judgments and equality of symbolic dimensions; proof transport across sidecar
revisions; trustworthy third-party condition evidence; rule/strategy
termination; and exact compatibility/version policy. Tensor and geometry
schemas and implementations are explicitly postponed.

## Phase-1 report

Completed: type/shape/property separation, examples and compatibility analysis.
Verification: JSON syntax of the examples is illustrative; only the existing
scalar file and the rejection of the extra v1 field were tested in phase 0.
Limitation: no proposed extension schema or typed checker has been implemented.
Recommended next step: specification-maintainer review before selecting A or B.
