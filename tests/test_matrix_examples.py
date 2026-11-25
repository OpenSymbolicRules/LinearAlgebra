"""Check the portable pilot examples through an independent matrix consumer."""

import json
import random
import unittest
from pathlib import Path

from numerical import add, det, eye, matmul, scale, transpose
from type_guard import ContextError, infer, validate_equality


EXAMPLES = Path(__file__).resolve().parents[1] / 'examples' / 'matrix-identities.json'


def product(a, b):
    if isinstance(a, list):
        return matmul(a, b) if isinstance(b, list) else scale(b, a)
    if isinstance(b, list):
        return scale(a, b)
    return a * b


SYMBOLS = {('arith1', 'times'): ('mul', product),
           ('arith1', 'power'): ('pow', pow),
           ('linalg1', 'determinant'): ('det', det),
           ('linalg5', 'identity'): ('I', eye),
           ('arith1', 'plus'): ('add', add),
           ('linalg1', 'transpose'): ('T', transpose)}

# Catalogue orientation, including the order in every matrix product.
CASES = {
    'transpose_scalar': ({'k': (), 'A': ('m', 'n')}, 'T(mul(k,A))', 'mul(k,T(A))', ('n', 'm')),
    'determinant_product': ({'A': ('n', 'n'), 'B': ('n', 'n')}, 'det(mul(A,B))', 'mul(det(A),det(B))', ()),
    'determinant_transpose': ({'A': ('n', 'n')}, 'det(T(A))', 'det(A)', ()),
    'determinant_scalar': ({'k': (), 'A': ('n', 'n')}, 'det(mul(k,A))', 'mul(pow(k,n),det(A))', ()),
    'determinant_identity': ({}, 'det(I(n))', '1', ()),
    'transpose_product': ({'A': ('m', 'n'), 'B': ('n', 'p')}, 'T(mul(A,B))', 'mul(T(B),T(A))', ('p', 'm')),
    'transpose_sum': ({'A': ('m', 'n'), 'B': ('m', 'n')}, 'T(add(A,B))', 'add(T(A),T(B))', ('n', 'm')),
    'transpose_twice': ({'A': ('m', 'n')}, 'T(T(A))', 'A', ('m', 'n')),
    'multiply_associative': ({'A': ('m', 'n'), 'B': ('n', 'p'), 'C': ('p', 'q')},
                             'mul(mul(A,B),C)', 'mul(A,mul(B,C))', ('m', 'q')),
    'distribute_left': ({'A': ('m', 'n'), 'B': ('n', 'p'), 'C': ('n', 'p')},
                        'mul(A,add(B,C))', 'add(mul(A,B),mul(A,C))', ('m', 'p')),
    'distribute_right': ({'A': ('m', 'n'), 'B': ('m', 'n'), 'C': ('n', 'p')},
                         'mul(add(A,B),C)', 'add(mul(A,C),mul(B,C))', ('m', 'p')),
}


def read_term(term, values):
    if term['kind'] == 'OMI':
        return str(term['integer']), term['integer']
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
        self.assertEqual(payload['profile'], 'linear_algebra.matrix_examples/0.2.0')
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
                key = rule['id'].removeprefix('linear_algebra.')
                inputs, left, right, result_shape = CASES[key]
                shapes = {}
                for name, decl in ctx['variables'].items():
                    if decl == {'kind': 'scalar'}:
                        shapes[name] = ('scalar',)
                    else:
                        self.assertEqual(set(decl), {'kind', 'rows', 'columns'})
                        shapes[name] = (decl['kind'], decl['rows'], decl['columns'])
                expected_inputs = {name: ('matrix', *axes) if axes else ('scalar',)
                                   for name, axes in inputs.items()}
                self.assertEqual(shapes, expected_inputs)
                dims = {dim for axes in inputs.values() for dim in axes}
                if key == 'determinant_identity':
                    dims.add('n')
                self.assertEqual(ctx['dimensions'], {d: {'min': 1} for d in dims})
                lhs, rhs = rule['pattern'], rule['replacement']
                self.assertTrue(validate_equality(lhs, rhs, shapes, dims))
                expected = ('matrix', *result_shape) if result_shape else ('scalar',)
                self.assertEqual(infer(lhs, shapes, dims), expected)
                for n, k in ((1, 2), (2, -2), (3, 1+2j), (4, 0), (4, 2)):
                    sizes = dict(m=2, n=n, p=4, q=5)
                    def entry():
                        real = rng.randint(-3, 3)
                        return complex(real, rng.randint(-3, 3)) if isinstance(k, complex) else real
                    values = {d: sizes[d] for d in dims}
                    for name, shape in shapes.items():
                        if shape == ('scalar',):
                            values[name] = k
                        else:
                            values[name] = [[entry() for _ in range(sizes[shape[2]])]
                                            for _ in range(sizes[shape[1]])]
                    if n == 4 and k == 2 and 'A' in values:
                        # Include a singular witness for each square-matrix formula.
                        values['A'][0] = [0] * len(values['A'][0])
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
