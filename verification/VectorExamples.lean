import OSR.OMObject

/-! Checked OpenMath rewrites in the standard oriented real Euclidean three-space. -/

namespace OSR.LinearAlgebraPilot.VectorExamples

open Matrix
open scoped Matrix
open Lean (Json)

private abbrev Vec := Fin 3 → ℝ
private abbrev Env := String → Vec
private inductive Value where
  | vector (v : Vec)
  | scalar (s : ℝ)
  | matrix (m : Matrix (Fin 3) (Fin 3) ℝ)
  | integer (n : Int)

private def cross (u v : OMObj) := OMObj.oma ⟨"linalg1", "vectorproduct"⟩ [u, v]
private def dot (u v : OMObj) := OMObj.oma ⟨"linalg1", "scalarproduct"⟩ [u, v]
private def zeroVec := OMObj.oma ⟨"linalg4vec", "zero"⟩ [.omi 3]
private def neg (v : OMObj) := OMObj.oma ⟨"arith1", "unary_minus"⟩ [v]
private def add (x y : OMObj) := OMObj.oma Op2.add.symbol [x, y]
private def sub (x y : OMObj) := OMObj.oma Op2.sub.symbol [x, y]
private def mul (x y : OMObj) := OMObj.oma Op2.mul.symbol [x, y]
private def norm (v : OMObj) := OMObj.oma ⟨"norm1", "Euclidean_norm"⟩ [v]
private def square (x : OMObj) := OMObj.oma powerSymbol [x, .omi 2]

private def outer (u v : OMObj) := OMObj.oma ⟨"linalg1", "outerproduct"⟩ [u, v]
private def vector (a b c : Int) := OMObj.oma ⟨"linalg3", "vector"⟩ [.omi a, .omi b, .omi c]
private def det (a : OMObj) := OMObj.oma ⟨"linalg1", "determinant"⟩ [a]

/-- The argument types distinguish the scalar, vector and matrix overloads. -/
private noncomputable def applySymbol (h : OMSymbol) (args : List Value) : Option Value :=
  match h.cd, h.name, args with
  | "linalg1", "vectorproduct", [.vector u, .vector v] => some (.vector (u ⨯₃ v))
  | "linalg1", "scalarproduct", [.vector u, .vector v] => some (.scalar (u ⬝ᵥ v))
  | "linalg1", "outerproduct", [.vector u, .vector v] => some (.matrix (vecMulVec u v))
  | "linalg1", "determinant", [.matrix m] => some (.scalar m.det)
  | "linalg3", "vector", [.integer a, .integer b, .integer c] => some (.vector ![(a : ℝ), b, c])
  | "linalg4vec", "zero", [.integer 3] => some (.vector 0)
  | "arith1", "unary_minus", [.vector v] => some (.vector (-v))
  | "arith1", "plus", [.vector u, .vector v] => some (.vector (u + v))
  | "arith1", "plus", [.matrix a, .matrix b] => some (.matrix (a + b))
  | "arith1", "minus", [.vector u, .vector v] => some (.vector (u - v))
  | "arith1", "minus", [.scalar x, .scalar y] => some (.scalar (x - y))
  | "arith1", "times", [.scalar k, .vector v] => some (.vector (k • v))
  | "arith1", "times", [.scalar x, .scalar y] => some (.scalar (x * y))
  | "norm1", "Euclidean_norm", [.vector v] => some (.scalar ‖WithLp.toLp 2 v‖)
  | "arith1", "power", [.scalar x, .integer 2] => some (.scalar (x ^ 2))
  | _, _, _ => none

/-- Structural size bounds the depth of every finite input tree. -/
private noncomputable def evalAt (names : List String) (ρ : Env) : Nat → OMObj → Option Value
  | 0, _ => none
  | _ + 1, .omv n => if n ∈ names then some (.vector (ρ n)) else none
  | _ + 1, .omi n => some (.integer n)
  | fuel + 1, .oma h args => do
    let vs ← args.mapM (evalAt names ρ fuel)
    applySymbol h vs
  | _ + 1, _ => none

private noncomputable def eval (names : List String) (ρ : Env) (e : OMObj) : Option Value :=
  evalAt names ρ (sizeOf e + 1) e

-- Undefined terms cannot satisfy the shared-value obligation for a rewrite.
example (ρ : Env) : eval ["u"] ρ (.oma ⟨"unknown", "vectorproduct"⟩ [.omv "u", .omv "u"]) = none := rfl
example (ρ : Env) : eval ["u"] ρ (cross (.omv "u") (.omi 2)) = none := rfl
example (ρ : Env) : eval ["u"] ρ (.omv "v") = none := rfl

private abbrev U := OMObj.omv "u"
private abbrev V := OMObj.omv "v"
private abbrev W := OMObj.omv "w"

private structure Example where
  id : String
  names : List String
  pattern : OMObj
  replacement : OMObj
  sound : ∀ ρ : Env, ∃ v, eval names ρ pattern = some v ∧ eval names ρ replacement = some v
  orderedSwap : Option (Fin names.length × Fin names.length) := none

private def antisymmetry : Example where
  id := "cross_anticommutative"
  names := ["u", "v"]
  pattern := cross U V
  replacement := neg (cross V U)
  orderedSwap := some (1, 0)
  sound ρ := by
    refine ⟨_, rfl, ?_⟩
    exact congrArg (fun x => some (Value.vector x)) (cross_anticomm (ρ "v") (ρ "u"))

private def selfCross : Example where
  id := "cross_self"
  names := ["u"]
  pattern := cross U U
  replacement := zeroVec
  sound ρ := by
    refine ⟨_, ?_, rfl⟩
    exact congrArg (fun x => some (Value.vector x)) (cross_self (ρ "u"))

private def triple : Example where
  id := "vector_triple"
  names := ["u", "v", "w"]
  pattern := cross U (cross V W)
  replacement := sub (mul (dot U W) V) (mul (dot U V) W)
  sound ρ := by
    refine ⟨_, ?_, rfl⟩
    apply congrArg (fun x => some (Value.vector x))
    simpa only [dotProduct_comm (ρ "v") (ρ "u")] using
      (cross_cross_eq_smul_sub_smul' (ρ "u") (ρ "v") (ρ "w"))

private def jacobi : Example where
  id := "cross_jacobi"
  names := ["u", "v", "w"]
  pattern := add (add (cross U (cross V W)) (cross V (cross W U))) (cross W (cross U V))
  replacement := zeroVec
  sound ρ := by
    refine ⟨_, ?_, rfl⟩
    exact congrArg (fun x => some (Value.vector x)) (jacobi_cross (ρ "u") (ρ "v") (ρ "w"))

private def lagrange : Example where
  id := "lagrange_norm"
  names := ["u", "v"]
  pattern := square (norm (cross U V))
  replacement := sub (mul (square (norm U)) (square (norm V))) (square (dot U V))
  sound ρ := by
    refine ⟨_, ?_, rfl⟩
    apply congrArg (fun x => some (Value.scalar x))
    change ‖WithLp.toLp 2 (ρ "u" ⨯₃ ρ "v")‖ ^ 2 =
      ‖WithLp.toLp 2 (ρ "u")‖ ^ 2 * ‖WithLp.toLp 2 (ρ "v")‖ ^ 2 - (ρ "u" ⬝ᵥ ρ "v") ^ 2
    simp only [← real_inner_self_eq_norm_sq, EuclideanSpace.inner_eq_star_dotProduct]
    simpa [dotProduct_comm, pow_two] using cross_dot_cross (ρ "u") (ρ "v") (ρ "u") (ρ "v")

private theorem outer_columns (u v w : Vec) :
    vecMulVec u ![1, 0, 0] + vecMulVec v ![0, 1, 0] + vecMulVec w ![0, 0, 1] =
      (![u, v, w] : Matrix (Fin 3) (Fin 3) ℝ)ᵀ := by
  ext i j
  fin_cases j <;> simp <;> rfl

private def scalarTriple : Example where
  id := "scalar_triple_columns"
  names := ["u", "v", "w"]
  pattern := dot U (cross V W)
  replacement := det (add (add (outer U (vector 1 0 0)) (outer V (vector 0 1 0)))
    (outer W (vector 0 0 1)))
  sound ρ := by
    refine ⟨_, ?_, rfl⟩
    apply congrArg (fun x => some (Value.scalar x))
    change ρ "u" ⬝ᵥ (ρ "v" ⨯₃ ρ "w") = Matrix.det
      (vecMulVec (ρ "u") ![(1 : Int), (0 : Int), (0 : Int)] + vecMulVec (ρ "v") ![(0 : Int), (1 : Int), (0 : Int)] + vecMulVec (ρ "w") ![(0 : Int), (0 : Int), (1 : Int)])
    simp only [Int.cast_zero, Int.cast_one]
    rw [outer_columns]
    exact (triple_product_eq_det (ρ "u") (ρ "v") (ρ "w")).trans
      (Matrix.det_transpose (![ρ "u", ρ "v", ρ "w"] : Matrix (Fin 3) (Fin 3) ℝ)).symm

private def Example.toJson (e : Example) : Json :=
  let space := Json.mkObj [("dimension", 3), ("metric", "euclidean"),
    ("orientation", "right_handed"), ("coordinates", "standard_orthonormal_basis")]
  let vars := e.names.map fun n => (n, Json.mkObj [("kind", "vector"), ("dimension", 3)])
  let ctx := Json.mkObj [("scalar_domains", Lean.toJson ["setname1#R"]),
    ("space", space), ("variables", Json.mkObj vars)]
  let guardJson := match e.orderedSwap with
    | none => Json.null
    | some (i, j) => Json.mkObj [("kind", "strict_variable_name_order"),
        ("less", e.names[i]), ("greater", e.names[j])]
  Json.mkObj [("id", "linear_algebra." ++ e.id), ("orientation", "forward"),
    ("context", ctx), ("conditions", Json.arr #[]), ("application_guard", guardJson),
    ("pattern", e.pattern.toJson), ("replacement", e.replacement.toJson)]

def payload : Json := Json.mkObj [("profile", "linear_algebra.euclidean_vectors/0.1.0"),
  ("rules", Json.arr ([antisymmetry, selfCross, scalarTriple, triple, jacobi, lagrange].map Example.toJson).toArray)]

end OSR.LinearAlgebraPilot.VectorExamples

/-- info: 'OSR.LinearAlgebraPilot.VectorExamples.payload' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.VectorExamples.payload

def main : IO Unit := IO.println OSR.LinearAlgebraPilot.VectorExamples.payload.pretty
