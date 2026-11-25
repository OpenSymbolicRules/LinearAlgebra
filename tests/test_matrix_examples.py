"""Check the portable pilot examples through an independent matrix consumer."""

import json
import random
import unittest
from pathlib import Path

from numerical import add, matmul, transpose
from type_guard import ContextError, infer, validate_equality


EXAMPLES = Path(__file__).resolve().parents[1] / 'examples' / 'matrix-identities.json'
SYMBOLS = {('arith1', 'times'): ('mul', matmul),
           ('arith1', 'plus'): ('add', add),
           ('linalg1', 'transpose'): ('T', transpose)}
# Catalogue orientation, including the order in every matrix product.
CASES = {
    'transpose_product': ([('m', 'n'), ('n', 'p')], 'T(mul(A,B))', 'mul(T(B),T(A))', ('p', 'm')),
    'transpose_sum': ([('m', 'n'), ('m', 'n')], 'T(add(A,B))', 'add(T(A),T(B))', ('n', 'm')),
    'transpose_twice': ([('m', 'n')], 'T(T(A))', 'A', ('m', 'n')),
    'multiply_associative': ([('m', 'n'), ('n', 'p'), ('p', 'q')],
                             'mul(mul(A,B),C)', 'mul(A,mul(B,C))', ('m', 'q')),
    'distribute_left': ([('m', 'n'), ('n', 'p'), ('n', 'p')],
                        'mul(A,add(B,C))', 'add(mul(A,B),mul(A,C))', ('m', 'p')),
    'distribute_right': ([('m', 'n'), ('m', 'n'), ('n', 'p')],
                         'mul(add(A,B),C)', 'add(mul(A,C),mul(B,C))', ('m', 'p')),
}


def read_term(term, values):
    if term['kind'] == 'OMV':
        name = term['name']
        return name, values[name]
    head = term['applicant']
    label, operation = SYMBOLS[head['cd'], head['name']]
    args = [read_term(arg, values) for arg in term['arguments']]
    return (f"{label}({','.join(name for name, _ in args)})",
            operation(*(value for _, value in args)))


class MatrixExamples(unittest.TestCase):
    def test_portable_terms(self):
        payload = json.loads(EXAMPLES.read_text())
        self.assertEqual(payload['profile'], 'linear_algebra.matrix_examples/0.1.0')
        rules = payload['rules']
        self.assertCountEqual([r['id'] for r in rules],
                              ['linear_algebra.' + name for name in CASES])
        rng = random.Random(4257)
        for rule in rules:
            with self.subTest(rule=rule['id']):
                self.assertEqual(rule['orientation'], 'forward')
                self.assertEqual(rule['conditions'], [])
                ctx = rule['context']
                self.assertEqual(ctx['scalar_domains'], ['setname1#R', 'setname1#C'])
                shapes = {name: (v['kind'], v['rows'], v['columns'])
                          for name, v in ctx['variables'].items()}
                dims = {d for _, rows, cols in shapes.values() for d in (rows, cols)}
                self.assertEqual(ctx['dimensions'], {d: {'min': 1} for d in dims})
                lhs, rhs = rule['pattern'], rule['replacement']
                inputs, left, right, result_shape = CASES[rule['id'].removeprefix('linear_algebra.')]
                self.assertEqual(shapes, {name: ('matrix', *dims)
                                          for name, dims in zip('ABC', inputs)})
                self.assertTrue(validate_equality(lhs, rhs, shapes))
                self.assertEqual(infer(lhs, shapes), ('matrix', *result_shape))
                for complex_entries in (False, True):
                    sizes = dict(m=2, n=3, p=4, q=5)
                    def entry():
                        real = rng.randint(-3, 3)
                        return complex(real, rng.randint(-3, 3)) if complex_entries else real
                    values = {k: [[entry() for _ in range(sizes[c])] for _ in range(sizes[r])]
                              for k, (_, r, c) in shapes.items()}
                    ltext, lval = read_term(lhs, values)
                    rtext, rval = read_term(rhs, values)
                    self.assertEqual((ltext, rtext), (left, right))
                    self.assertEqual(lval, rval)

    def test_invalid_product_context_and_unknown_head(self):
        rules = json.loads(EXAMPLES.read_text())['rules']
        rule = next(r for r in rules if r['id'] == 'linear_algebra.transpose_product')
        with self.assertRaises(ContextError):
            infer(rule['pattern'], {'A': ('matrix', 2, 3), 'B': ('matrix', 4, 2)})
        rule['pattern']['applicant']['cd'] = 'unregistered'
        with self.assertRaises(ContextError):
            infer(rule['pattern'], {'A': ('matrix', 2, 3), 'B': ('matrix', 3, 4)})
