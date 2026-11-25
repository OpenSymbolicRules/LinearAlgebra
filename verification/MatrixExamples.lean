import OSR.OMObject

/-! Matrix-shaped interpretations for the catalogue examples. The portable trees
are OSR.OMObj values. The symbolic indices on each operation constrain both
the resulting object and the Mathlib value whose equality we prove. -/

namespace OSR.LinearAlgebraPilot.MatrixExamples

open Lean (Json)

private inductive Shape where
  | scalar
  | matrix (rows cols : String)

private structure Variable where
  name : String
  shape : Shape

private structure Context where
  vars : List Variable
  /-- Dimensions introduced independently of a matrix variable, as in det(I_n). -/
  parameters : List String := []

private def Context.dimensions (ctx : Context) : List String :=
  (ctx.parameters ++ ctx.vars.flatMap fun v => match v.shape with
    | .matrix r c => [r, c]
    | .scalar => []).eraseDups

private abbrev Shape.Value (K : Type) (d : String → Nat) : Shape → Type
  | .scalar => K
  | .matrix r c => Matrix (Fin (d r)) (Fin (d c)) K

private abbrev Assignment (ctx : Context) (K : Type) (d : String → Nat) :=
  (i : Fin ctx.vars.length) → ctx.vars[i].shape.Value K d

private structure Term (ctx : Context) (shape : Shape) where
  object : OMObj
  eval : (K : Type) → [CommRing K] → (d : String → Nat) → Assignment ctx K d → shape.Value K d

private def var (ctx : Context) (i : Fin ctx.vars.length) : Term ctx ctx.vars[i].shape :=
  ⟨.omv ctx.vars[i].name, fun _ _ _ env => env i⟩

private def trans {ctx r c} (a : Term ctx (.matrix r c)) : Term ctx (.matrix c r) :=
  ⟨.oma ⟨"linalg1", "transpose"⟩ [a.object], fun K _ d env => (a.eval K d env).transpose⟩

private def add {ctx r c} (a b : Term ctx (.matrix r c)) : Term ctx (.matrix r c) :=
  ⟨.oma Op2.add.symbol [a.object, b.object], fun K _ d env => a.eval K d env + b.eval K d env⟩

private def mul {ctx r n c} (a : Term ctx (.matrix r n)) (b : Term ctx (.matrix n c)) : Term ctx (.matrix r c) :=
  ⟨.oma Op2.mul.symbol [a.object, b.object], fun K _ d env => a.eval K d env * b.eval K d env⟩

private def scale {ctx r c} (k : Term ctx .scalar) (a : Term ctx (.matrix r c)) :
    Term ctx (.matrix r c) :=
  ⟨.oma Op2.mul.symbol [k.object, a.object], fun K _ d env => k.eval K d env • a.eval K d env⟩

private def times {ctx} (a b : Term ctx .scalar) : Term ctx .scalar :=
  ⟨.oma Op2.mul.symbol [a.object, b.object], fun K _ d env => a.eval K d env * b.eval K d env⟩

private def det {ctx n} (a : Term ctx (.matrix n n)) : Term ctx .scalar :=
  ⟨.oma ⟨"linalg1", "determinant"⟩ [a.object], fun K _ d env => Matrix.det (a.eval K d env)⟩

private def powDim {ctx} (a : Term ctx .scalar) (n : String) (_h : n ∈ ctx.dimensions) :
    Term ctx .scalar :=
  ⟨.oma powerSymbol [a.object, .omv n], fun K _ d env => a.eval K d env ^ d n⟩

private def identity (ctx : Context) (n : String) (_h : n ∈ ctx.dimensions) :
    Term ctx (.matrix n n) :=
  ⟨.oma ⟨"linalg5", "identity"⟩ [.omv n], fun _ _ _ _ => 1⟩

private def one (ctx : Context) : Term ctx .scalar := ⟨.omi 1, fun _ _ _ _ => 1⟩

private structure Example where
  id : String
  ctx : Context
  {shape : Shape}
  pattern : Term ctx shape
  replacement : Term ctx shape
  sound : ∀ (K : Type) [CommRing K] (d : String → Nat) (env : Assignment ctx K d),
    pattern.eval K d env = replacement.eval K d env

private def transposeProduct : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩, ⟨"B", .matrix "n" "p"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  ⟨"transpose_product", ctx, trans (mul a b), mul (trans b) (trans a),
    fun _ _ _ _ => Matrix.transpose_mul ..⟩

private def transposeSum : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩, ⟨"B", .matrix "m" "n"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  ⟨"transpose_sum", ctx, trans (add a b), add (trans a) (trans b),
    fun _ _ _ _ => Matrix.transpose_add ..⟩

private def transposeTwice : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩] }
  let a := var ctx ⟨0, by decide⟩
  ⟨"transpose_twice", ctx, trans (trans a), a, fun _ _ _ _ => Matrix.transpose_transpose ..⟩

private def multiplyAssociative : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩, ⟨"B", .matrix "n" "p"⟩, ⟨"C", .matrix "p" "q"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"multiply_associative", ctx, mul (mul a b) c, mul a (mul b c),
    fun _ _ _ _ => Matrix.mul_assoc ..⟩

private def distributeLeft : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩, ⟨"B", .matrix "n" "p"⟩, ⟨"C", .matrix "n" "p"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"distribute_left", ctx, mul a (add b c), add (mul a b) (mul a c),
    fun _ _ _ _ => Matrix.mul_add ..⟩

private def distributeRight : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "m" "n"⟩, ⟨"B", .matrix "m" "n"⟩, ⟨"C", .matrix "n" "p"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"distribute_right", ctx, mul (add a b) c, add (mul a c) (mul b c),
    fun _ _ _ _ => Matrix.add_mul ..⟩

private def transposeScalar : Example :=
  let ctx : Context := { vars := [⟨"k", .scalar⟩, ⟨"A", .matrix "m" "n"⟩] }
  let k := var ctx ⟨0, by decide⟩
  let a := var ctx ⟨1, by decide⟩
  ⟨"transpose_scalar", ctx, trans (scale k a), scale k (trans a),
    fun _ _ _ _ => Matrix.transpose_smul ..⟩

private def determinantProduct : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "n" "n"⟩, ⟨"B", .matrix "n" "n"⟩] }
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  ⟨"determinant_product", ctx, det (mul a b), times (det a) (det b),
    fun _ _ _ _ => Matrix.det_mul ..⟩

private def determinantTranspose : Example :=
  let ctx : Context := { vars := [⟨"A", .matrix "n" "n"⟩] }
  let a := var ctx ⟨0, by decide⟩
  ⟨"determinant_transpose", ctx, det (trans a), det a, fun _ _ _ _ => Matrix.det_transpose ..⟩

private def determinantScalar : Example :=
  let ctx : Context := { vars := [⟨"k", .scalar⟩, ⟨"A", .matrix "n" "n"⟩] }
  let k : Term ctx .scalar := var ctx ⟨0, by decide⟩
  let a : Term ctx (.matrix "n" "n") := var ctx ⟨1, by decide⟩
  ⟨"determinant_scalar", ctx, det (scale k a), times (powDim k "n" (by decide)) (det a),
    fun K _ d env => by
      change Matrix.det (k.eval K d env • a.eval K d env) =
        k.eval K d env ^ d "n" * Matrix.det (a.eval K d env)
      simpa only [Fintype.card_fin] using
        (Matrix.det_smul (a.eval K d env) (k.eval K d env))⟩

private def determinantIdentity : Example :=
  let ctx : Context := { vars := [], parameters := ["n"] }
  ⟨"determinant_identity", ctx, det (identity ctx "n" (by decide)), one ctx,
    fun _ _ _ _ => Matrix.det_one⟩

private def catalogue : List Example :=
  [transposeProduct, transposeSum, transposeTwice, multiplyAssociative, distributeLeft, distributeRight,
   transposeScalar, determinantProduct, determinantTranspose, determinantScalar, determinantIdentity]

private def Example.toJson (e : Example) : Json :=
  let declarations := e.ctx.vars.map fun v => (v.name, match v.shape with
    | .scalar => Json.mkObj [("kind", "scalar")]
    | .matrix r c => Json.mkObj [("kind", "matrix"), ("rows", r), ("columns", c)])
  let ctx := Json.mkObj [
    ("dimensions", Json.mkObj (e.ctx.dimensions.map fun d => (d, Json.mkObj [("min", 1)]))),
    ("scalar_domains", Lean.toJson ["setname1#R", "setname1#C"]),
    ("variables", Json.mkObj declarations)]
  Json.mkObj [("id", "linear_algebra." ++ e.id), ("orientation", "forward"),
    ("context", ctx), ("conditions", Json.arr #[]),
    ("pattern", e.pattern.object.toJson), ("replacement", e.replacement.object.toJson)]

def payload : Json := Json.mkObj [
  ("profile", "linear_algebra.matrix_examples/0.2.0"),
  ("rules", Json.arr (catalogue.map Example.toJson).toArray)]

end OSR.LinearAlgebraPilot.MatrixExamples

/-- info: 'OSR.LinearAlgebraPilot.MatrixExamples.payload' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.MatrixExamples.payload

def main : IO Unit := IO.println OSR.LinearAlgebraPilot.MatrixExamples.payload.pretty
