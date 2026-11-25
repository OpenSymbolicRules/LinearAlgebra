import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.LinearAlgebra.CrossProduct

namespace OSR.LinearAlgebraPilot

open Matrix
open scoped Matrix InnerProductSpace

/-- V3 in the standard right-handed coordinates, with the three vectors as columns. -/
theorem scalar_triple_columns (u v w : Fin 3 → ℝ) :
    u ⬝ᵥ (v ⨯₃ w) = Matrix.det (![u, v, w]ᵀ) := by
  exact (triple_product_eq_det u v w).trans
    (Matrix.det_transpose (![u, v, w] : Matrix (Fin 3) (Fin 3) ℝ)).symm

/-- V6 for the Euclidean norm and real inner product in the same coordinates. -/
theorem lagrange_norm (u v : EuclideanSpace ℝ (Fin 3)) :
    ‖WithLp.toLp 2 (WithLp.ofLp u ⨯₃ WithLp.ofLp v)‖ ^ 2 =
      ‖u‖ ^ 2 * ‖v‖ ^ 2 - ⟪u, v⟫_ℝ ^ 2 := by
  simp only [← real_inner_self_eq_norm_sq, EuclideanSpace.inner_eq_star_dotProduct]
  simpa [dotProduct_comm, pow_two] using
    cross_dot_cross (WithLp.ofLp u) (WithLp.ofLp v) (WithLp.ofLp u) (WithLp.ofLp v)

/-- E1 over the complex numbers. -/
theorem complex_exp_zero {n : ℕ} : NormedSpace.exp (0 : Matrix (Fin n) (Fin n) ℂ) = 1 :=
  NormedSpace.exp_zero

/-- E2 over the complex numbers, under the catalogue's commutation hypothesis. -/
theorem complex_exp_commuting {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℂ) (h : Commute A B) :
    NormedSpace.exp (A + B) = NormedSpace.exp A * NormedSpace.exp B :=
  Matrix.exp_add_of_commute A B h

end OSR.LinearAlgebraPilot

/-- info: 'OSR.LinearAlgebraPilot.scalar_triple_columns' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.scalar_triple_columns

/-- info: 'OSR.LinearAlgebraPilot.lagrange_norm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.lagrange_norm

/-- info: 'OSR.LinearAlgebraPilot.complex_exp_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.complex_exp_zero

/-- info: 'OSR.LinearAlgebraPilot.complex_exp_commuting' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.complex_exp_commuting
