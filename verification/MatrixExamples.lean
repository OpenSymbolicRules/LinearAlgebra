import OSR.OMObject

/-! Matrix-shaped interpretations for six catalogue examples. The portable trees
are OSR.OMObj values. The symbolic indices on each operation constrain both
the resulting object and the Mathlib value whose equality we prove. -/

namespace OSR.LinearAlgebraPilot.MatrixExamples

open Lean (Json)

private structure Variable where
  name : String
  rows : String
  cols : String

private abbrev Mat (K : Type) (d : String → Nat) (r c : String) :=
  Matrix (Fin (d r)) (Fin (d c)) K

private abbrev Assignment (ctx : List Variable) (K : Type) (d : String → Nat) :=
  (i : Fin ctx.length) → Mat K d ctx[i].rows ctx[i].cols

private structure Term (ctx : List Variable) (r c : String) where
  object : OMObj
  eval : (K : Type) → [CommSemiring K] → (d : String → Nat) → Assignment ctx K d → Mat K d r c

private def var (ctx : List Variable) (i : Fin ctx.length) : Term ctx ctx[i].rows ctx[i].cols :=
  ⟨.omv ctx[i].name, fun _ _ _ env => env i⟩

private def trans {ctx r c} (a : Term ctx r c) : Term ctx c r :=
  ⟨.oma ⟨"linalg1", "transpose"⟩ [a.object], fun K _ d env => (a.eval K d env).transpose⟩

private def add {ctx r c} (a b : Term ctx r c) : Term ctx r c :=
  ⟨.oma Op2.add.symbol [a.object, b.object], fun K _ d env => a.eval K d env + b.eval K d env⟩

private def mul {ctx r n c} (a : Term ctx r n) (b : Term ctx n c) : Term ctx r c :=
  ⟨.oma Op2.mul.symbol [a.object, b.object], fun K _ d env => a.eval K d env * b.eval K d env⟩

private structure Example where
  id : String
  ctx : List Variable
  {rows : String}
  {cols : String}
  pattern : Term ctx rows cols
  replacement : Term ctx rows cols
  sound : ∀ (K : Type) [CommSemiring K] (d : String → Nat) (env : Assignment ctx K d),
    pattern.eval K d env = replacement.eval K d env

private def transposeProduct : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩, ⟨"B", "n", "p"⟩]
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  ⟨"transpose_product", ctx, trans (mul a b), mul (trans b) (trans a),
    fun _ _ _ _ => Matrix.transpose_mul ..⟩

private def transposeSum : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩, ⟨"B", "m", "n"⟩]
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  ⟨"transpose_sum", ctx, trans (add a b), add (trans a) (trans b),
    fun _ _ _ _ => Matrix.transpose_add ..⟩

private def transposeTwice : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩]
  let a := var ctx ⟨0, by decide⟩
  ⟨"transpose_twice", ctx, trans (trans a), a, fun _ _ _ _ => Matrix.transpose_transpose ..⟩

private def multiplyAssociative : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩, ⟨"B", "n", "p"⟩, ⟨"C", "p", "q"⟩]
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"multiply_associative", ctx, mul (mul a b) c, mul a (mul b c),
    fun _ _ _ _ => Matrix.mul_assoc ..⟩

private def distributeLeft : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩, ⟨"B", "n", "p"⟩, ⟨"C", "n", "p"⟩]
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"distribute_left", ctx, mul a (add b c), add (mul a b) (mul a c),
    fun _ _ _ _ => Matrix.mul_add ..⟩

private def distributeRight : Example :=
  let ctx : List Variable := [⟨"A", "m", "n"⟩, ⟨"B", "m", "n"⟩, ⟨"C", "n", "p"⟩]
  let a := var ctx ⟨0, by decide⟩
  let b := var ctx ⟨1, by decide⟩
  let c := var ctx ⟨2, by decide⟩
  ⟨"distribute_right", ctx, mul (add a b) c, add (mul a c) (mul b c),
    fun _ _ _ _ => Matrix.add_mul ..⟩

private def catalogue : List Example :=
  [transposeProduct, transposeSum, transposeTwice, multiplyAssociative, distributeLeft, distributeRight]

private def Example.toJson (e : Example) : Json :=
  let dims := (e.ctx.flatMap fun v => [v.rows, v.cols]).eraseDups
  let ctx := Json.mkObj [
    ("dimensions", Json.mkObj (dims.map fun d => (d, Json.mkObj [("min", 1)]))),
    ("scalar_domains", Lean.toJson ["setname1#R", "setname1#C"]),
    ("variables", Json.mkObj (e.ctx.map fun v => (v.name, Json.mkObj [
      ("kind", "matrix"), ("rows", v.rows), ("columns", v.cols)])))]
  Json.mkObj [("id", "linear_algebra." ++ e.id), ("orientation", "forward"),
    ("context", ctx), ("conditions", Json.arr #[]),
    ("pattern", e.pattern.object.toJson), ("replacement", e.replacement.object.toJson)]

def payload : Json := Json.mkObj [
  ("profile", "linear_algebra.matrix_examples/0.1.0"),
  ("rules", Json.arr (catalogue.map Example.toJson).toArray)]

end OSR.LinearAlgebraPilot.MatrixExamples

/-- info: 'OSR.LinearAlgebraPilot.MatrixExamples.payload' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.MatrixExamples.payload

def main : IO Unit := IO.println OSR.LinearAlgebraPilot.MatrixExamples.payload.pretty
