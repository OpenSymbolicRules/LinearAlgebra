"""Tests for the experimental guard on a small OpenMath expression fragment."""

import unittest

from type_guard import ContextError, infer, validate_equality


def var(name):
    return {'kind': 'OMV', 'name': name}


def call(cd, name, *args):
    return {'kind': 'OMA', 'applicant': {'kind': 'OMS', 'cd': cd, 'name': name},
            'arguments': list(args)}


class ShapeGuardTests(unittest.TestCase):
    def setUp(self):
        self.context = {'A': ('matrix', 'm', 'n'), 'B': ('matrix', 'n', 'p'),
                        'C': ('matrix', 'q', 'p'), 'u': ('vector', 'n'),
                        'k': ('scalar',)}

    def test_rectangular_transpose_product(self):
        lhs = call('linalg1', 'transpose', call('arith1', 'times', var('A'), var('B')))
        rhs = call('arith1', 'times', call('linalg1', 'transpose', var('B')),
                   call('linalg1', 'transpose', var('A')))
        self.assertEqual(infer(lhs, self.context), ('matrix', 'p', 'm'))
        self.assertTrue(validate_equality(lhs, rhs, self.context))

    def test_invalid_inner_dimension_is_rejected(self):
        with self.assertRaises(ContextError):
            infer(call('arith1', 'times', var('A'), var('C')), self.context)

    def test_matrix_vector_and_scalar(self):
        self.assertEqual(infer(call('arith1', 'times', var('A'), var('u')), self.context),
                         ('vector', 'm'))
        self.assertEqual(infer(call('arith1', 'times', var('k'), var('A')), self.context),
                         ('matrix', 'm', 'n'))

    def test_addition_requires_equal_shapes(self):
        with self.assertRaises(ContextError):
            infer(call('arith1', 'plus', var('A'), var('B')), self.context)

    def test_determinant_requires_square_matrix(self):
        expr = call('linalg1', 'determinant', var('A'))
        self.assertEqual(infer(expr, {'A': ('matrix', 'n', 'n')}), ('scalar',))
        for declaration in [('matrix', 2, 3), ('matrix', 'm', 'n'), ('scalar',), ('vector', 3)]:
            with self.subTest(declaration=declaration), self.assertRaises(ContextError):
                infer(expr, {'A': declaration})

    def test_dimension_arguments(self):
        ident = lambda size: call('linalg5', 'identity', size)
        power = lambda size: call('arith1', 'power', var('k'), size)
        self.assertEqual(infer(ident(var('n')), {}, {'n'}), ('matrix', 'n', 'n'))
        self.assertEqual(infer(ident({'kind': 'OMI', 'integer': 3}), {}), ('matrix', 3, 3))
        self.assertEqual(infer(power(var('n')), self.context, {'n'}), ('scalar',))
        for constructor in (ident, power):
            for arg in (var('undeclared'), var('k'), {'kind': 'OMI', 'integer': 0},
                        {'kind': 'OMI', 'integer': -2}, {'kind': 'OMI', 'integer': True}):
                with self.subTest(arg=arg), self.assertRaises(ContextError):
                    infer(constructor(arg), self.context, {'n'})
        with self.assertRaises(ContextError):
            infer(ident(var('n')), {'n': ('scalar',)}, {'n'})
        with self.assertRaises(ContextError):
            infer(call('arith1', 'power', var('A'), var('n')), self.context, {'m', 'n'})
        with self.assertRaises(ContextError):
            infer(call('linalg1', 'determinant', var('A')), {'A': ('matrix', 'n', 'n')}, {'m'})

    def test_order_is_significant(self):
        self.assertEqual(infer(call('arith1', 'times', var('A'), var('B')), self.context),
                         ('matrix', 'm', 'p'))
        with self.assertRaises(ContextError):
            infer(call('arith1', 'times', var('B'), var('A')), self.context)

    def test_unknown_and_malformed_are_rejected(self):
        for expression in (call('unknown', 'transpose', var('A')),
                           call('linalg1', 'transpose', var('A'), var('B')),
                           var('unbound'), {'kind': 'OMS', 'cd': 'arith1', 'name': 'times'}):
            with self.subTest(expression=expression), self.assertRaises(ContextError):
                infer(expression, self.context)

    def test_equations_with_distinct_result_shapes_are_rejected(self):
        with self.assertRaises(ContextError):
            validate_equality(var('A'), var('B'), self.context)


if __name__ == '__main__':
    unittest.main()
