"""Deterministic sanity checks for the proposed identities, not formal proofs."""

import math
import random
import unittest

from numerical import (add, cross, det, dot, expm, eye, inv, matmul, scale,
                       trace, transpose, vecadd, vecscale)


class NumericalIdentities(unittest.TestCase):
    def assertClose(self, a, b):
        if isinstance(a, list):
            self.assertEqual(len(a), len(b))
            for x, y in zip(a, b):
                self.assertClose(x, y)
        else:
            self.assertTrue(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9),
                            f"{a!r} != {b!r}")

    def test_square_matrix_rules(self):
        rng = random.Random(20261123)
        for n in (1, 2, 3):
            for _ in range(4):
                # Strictly upper triangular perturbations of identity are invertible.
                a = [[(1 if i == j else rng.randint(-2, 2) if i < j else 0)
                      for j in range(n)] for i in range(n)]
                b = [[(1 if i == j else rng.randint(-2, 2) if i > j else 0)
                      for j in range(n)] for i in range(n)]
                c = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
                k = 2
                ai, bi = inv(a), inv(b)
                with self.subTest(n=n, a=a, b=b):
                    self.assertClose(transpose(matmul(a, b)), matmul(transpose(b), transpose(a)))
                    self.assertClose(transpose(add(a, b)), add(transpose(a), transpose(b)))
                    self.assertClose(transpose(scale(k, a)), scale(k, transpose(a)))
                    self.assertClose(transpose(transpose(a)), a)
                    self.assertClose(transpose(ai), inv(transpose(a)))
                    self.assertClose(trace(add(a, b)), trace(a) + trace(b))
                    self.assertClose(trace(scale(k, a)), k * trace(a))
                    self.assertClose(trace(transpose(a)), trace(a))
                    self.assertClose(det(matmul(a, b)), det(a) * det(b))
                    self.assertClose(det(transpose(a)), det(a))
                    self.assertClose(det(scale(k, a)), k ** n * det(a))
                    self.assertClose(det(ai), 1 / det(a))
                    self.assertClose(det(eye(n)), 1)
                    self.assertClose(inv(matmul(a, b)), matmul(bi, ai))
                    self.assertClose(inv(ai), a)
                    self.assertClose(inv(scale(k, a)), scale(1 / k, ai))
                    self.assertClose(matmul(matmul(a, b), c), matmul(a, matmul(b, c)))
                    self.assertClose(matmul(a, add(b, c)), add(matmul(a, b), matmul(a, c)))
                    self.assertClose(matmul(add(a, b), c), add(matmul(a, c), matmul(b, c)))
                    self.assertClose(expm(scale(0, a)), eye(n))
                    # B is a scalar multiple of A, ensuring AB = BA.
                    commuting = scale(0.2, a)
                    self.assertClose(expm(add(scale(0.1, a), commuting)),
                                     matmul(expm(scale(0.1, a)), expm(commuting)))

    def test_rectangular_trace_and_transpose(self):
        rng = random.Random(47)
        for m, n in ((1, 3), (2, 3), (3, 2)):
            a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
            b = [[rng.randint(-3, 3) for _ in range(m)] for _ in range(n)]
            self.assertClose(trace(matmul(a, b)), trace(matmul(b, a)))
            self.assertClose(transpose(matmul(a, b)), matmul(transpose(b), transpose(a)))

    def test_vector_rules(self):
        rng = random.Random(81)
        for _ in range(12):
            u, v, w = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
            self.assertClose(cross(u, v), vecscale(-1, cross(v, u)))
            self.assertClose(cross(u, u), [0, 0, 0])
            self.assertClose(dot(u, cross(v, w)), det(transpose([u, v, w])))
            self.assertClose(cross(u, cross(v, w)),
                             vecadd(vecscale(dot(u, w), v), vecscale(-dot(u, v), w)))
            self.assertClose(vecadd(vecadd(cross(u, cross(v, w)), cross(v, cross(w, u))),
                                    cross(w, cross(u, v))), [0, 0, 0])
            self.assertClose(dot(cross(u, v), cross(u, v)),
                             dot(u, u) * dot(v, v) - dot(u, v) ** 2)

    def test_invalid_shapes_and_false_rules(self):
        with self.assertRaises(ValueError):
            matmul([[1, 2]], [[1, 2]])
        with self.assertRaises(ValueError):
            inv([[1, 2], [2, 4]])
        a, b = [[0, 1], [0, 0]], [[0, 0], [1, 0]]
        self.assertNotEqual(matmul(add(a, b), add(a, b)),
                            add(add(matmul(a, a), scale(2, matmul(a, b))), matmul(b, b)))
        self.assertGreater(abs(expm(add(a, b))[0][0] - matmul(expm(a), expm(b))[0][0]), 0.1)
        i = eye(2)
        self.assertNotEqual(det(add(i, i)), det(i) + det(i))
        self.assertNotEqual(det(scale(2, i)), 2 * det(i))
        a, b = [[1, 1], [0, 1]], [[1, 0], [1, 1]]
        self.assertNotEqual(inv(matmul(a, b)), matmul(inv(a), inv(b)))
        self.assertNotEqual(trace(matmul(i, i)), trace(i) * trace(i))


if __name__ == '__main__':
    unittest.main(verbosity=2)
