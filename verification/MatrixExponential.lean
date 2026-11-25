import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

namespace OSR.LinearAlgebraPilot

open Matrix

private theorem exp_of_square_zero (X : Matrix (Fin 2) (Fin 2) ℝ) (h : X ^ 2 = 0) :
    NormedSpace.exp X = 1 + X := by
  simp only [NormedSpace.exp_eq_tsum ℝ]
  rw [tsum_eq_sum (s := Finset.range 2) (f := fun n : ℕ => (n.factorial : ℝ)⁻¹ • X ^ n)]
  · simp [Finset.sum_range_succ]
  · intro n hn
    rw [pow_eq_zero_of_le (Nat.le_of_not_gt (mt Finset.mem_range.mpr hn)) h, smul_zero]

/-- The unguarded exponential sum rule fails on two real matrix units. -/
theorem exponential_sum_false :
    let A : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 0, 0]
    let B : Matrix (Fin 2) (Fin 2) ℝ := !![0, 0; 1, 0]
    NormedSpace.exp (A + B) ≠ NormedSpace.exp A * NormedSpace.exp B := by
  let A : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 0, 0]
  let B : Matrix (Fin 2) (Fin 2) ℝ := !![0, 0; 1, 0]
  change NormedSpace.exp (A + B) ≠ NormedSpace.exp A * NormedSpace.exp B
  have hA : A ^ 2 = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [A, pow_two, Matrix.mul_apply, Fin.sum_univ_two]
  have hB : B ^ 2 = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [B, pow_two, Matrix.mul_apply, Fin.sum_univ_two]
  intro heq
  have comm := ((Commute.refl (A + B)).exp_right).eq
  rw [heq, exp_of_square_zero A hA, exp_of_square_zero B hB] at comm
  have entry := congrFun (congrFun comm 0) 1
  norm_num [A, B, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] at entry

end OSR.LinearAlgebraPilot

/-- info: 'OSR.LinearAlgebraPilot.exponential_sum_false' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OSR.LinearAlgebraPilot.exponential_sum_false
