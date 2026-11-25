"""Exercise the serialized real Euclidean rules, including their application guard."""

import copy
import json
import math
import random
import unittest
from pathlib import Path

from vector_profile import ModelError, guard_allows, interpret, validate_context


DATA = Path(__file__).resolve().parents[1] / 'examples' / 'vector-identities.json'
VARS = {'cross_anticommutative': 'uv', 'cross_self': 'u', 'vector_triple': 'uvw',
        'scalar_triple_columns': 'uvw', 'cross_jacobi': 'uvw', 'lagrange_norm': 'uv'}
CROSS = {'kind': 'OMS', 'cd': 'linalg1', 'name': 'vectorproduct'}


def var(name):
    return {'kind': 'OMV', 'name': name}


class VectorExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(DATA.read_text())
        assert payload['profile'] == 'linear_algebra.euclidean_vectors/0.1.0'
        cls.rules = {r['id'].removeprefix('linear_algebra.'): r for r in payload['rules']}
        assert len(cls.rules) == len(payload['rules'])

    def test_catalogue(self):
        self.assertEqual(self.rules.keys(), VARS.keys())
        rng = random.Random(281)
        samples = [([1, 0, 0], [0, 1, 0], [0, 0, 1]), ([0, 0, 0], [1, 2, 3], [1, 2, 3])]
        samples.extend([rng.choices(range(-4, 5), k=3) for _ in range(3)] for _ in range(16))
        for key, names in VARS.items():
            r = self.rules[key]
            self.assertEqual(r['orientation'], 'forward')
            self.assertEqual(r['conditions'], [])
            self.assertEqual(set(validate_context(r['context'])), set(names))
            for sample in samples:
                env = dict(zip(names, sample))
                left = interpret(r['pattern'], r['context'], env)
                right = interpret(r['replacement'], r['context'], env)
                with self.subTest(rule=key, sample=sample):
                    if key == 'lagrange_norm':
                        self.assertTrue(math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12))
                    else:
                        self.assertEqual(left, right)
            if key != 'cross_anticommutative':
                self.assertIsNone(r['application_guard'])

    def test_catalogue_forms(self):
        def form(t):
            if t['kind'] == 'OMV':
                return t['name']
            if t['kind'] == 'OMI':
                return str(t['integer'])
            return f"{t['applicant']['name']}({','.join(map(form, t['arguments']))})"

        expected = {
            'cross_self': ('vectorproduct(u,u)', 'zero(3)'),
            'vector_triple': ('vectorproduct(u,vectorproduct(v,w))',
                              'minus(times(scalarproduct(u,w),v),times(scalarproduct(u,v),w))'),
            'cross_jacobi': ('plus(plus(vectorproduct(u,vectorproduct(v,w)),vectorproduct(v,vectorproduct(w,u))),'
                            'vectorproduct(w,vectorproduct(u,v)))', 'zero(3)'),
            'scalar_triple_columns': ('scalarproduct(u,vectorproduct(v,w))',
                                     'determinant(plus(plus(outerproduct(u,vector(1,0,0)),'
                                     'outerproduct(v,vector(0,1,0))),outerproduct(w,vector(0,0,1))))'),
            'lagrange_norm': ('power(Euclidean_norm(vectorproduct(u,v)),2)',
                              'minus(times(power(Euclidean_norm(u),2),power(Euclidean_norm(v),2)),'
                              'power(scalarproduct(u,v),2))'),
        }
        for key, pair in expected.items():
            with self.subTest(rule=key):
                r = self.rules[key]
                self.assertEqual((form(r['pattern']), form(r['replacement'])), pair)

    def test_ordered_swap(self):
        r = self.rules['cross_anticommutative']
        self.assertEqual(r['pattern'], {'kind': 'OMA', 'applicant': CROSS, 'arguments': [var('u'), var('v')]})
        self.assertEqual(r['replacement']['applicant']['name'], 'unary_minus')
        self.assertEqual(r['replacement']['arguments'][0]['arguments'], [var('v'), var('u')])
        guard = r['application_guard']
        self.assertEqual(guard, {'kind': 'strict_variable_name_order', 'less': 'v', 'greater': 'u'})
        self.assertTrue(guard_allows(guard, {'u': var('z'), 'v': var('a')}))
        self.assertFalse(guard_allows(guard, {'u': var('a'), 'v': var('z')}))
        self.assertFalse(guard_allows(guard, {'u': var('a'), 'v': var('a')}))
        self.assertFalse(guard_allows(guard, {'u': r['pattern'], 'v': var('a')}))
        self.assertFalse(guard_allows(guard, {}))
        with self.assertRaises(ModelError):
            guard_allows({'kind': 'unknown'}, {})

    def test_orientation_and_unsupported_inputs(self):
        r = self.rules['cross_anticommutative']
        env = {'u': [1, 0, 0], 'v': [0, 1, 0]}
        self.assertEqual(interpret(r['pattern'], r['context'], env), [0, 0, 1])
        for field, value in [('dimension', 4), ('orientation', 'left_handed'),
                             ('metric', 'indefinite'), ('coordinates', 'arbitrary_basis')]:
            ctx = copy.deepcopy(r['context'])
            ctx['space'][field] = value
            with self.assertRaises(ModelError):
                interpret(r['pattern'], ctx, env)
        ctx = dict(r['context'], scalar_domains=['setname1#C'])
        with self.assertRaises(ModelError):
            interpret(r['pattern'], ctx, env)
        for invalid in ([1, 2], [1j, 2, 3]):
            with self.assertRaises(ModelError):
                interpret(r['pattern'], r['context'], dict(env, u=invalid))
        bad = copy.deepcopy(r['pattern'])
        bad['applicant']['cd'] = 'unknown'
        with self.assertRaises(ModelError):
            interpret(bad, r['context'], env)

    def test_scalar_triple_columns(self):
        r = self.rules['scalar_triple_columns']
        env = {'u': [1, 2, 3], 'v': [4, 5, 6], 'w': [-1, 3, 2]}
        determinant = r['replacement']
        self.assertEqual(determinant['applicant'], {'kind': 'OMS', 'cd': 'linalg1', 'name': 'determinant'})
        self.assertEqual(interpret(determinant['arguments'][0], r['context'], env),
                         [[1, 4, -1], [2, 5, 3], [3, 6, 2]])
        for v, w, expected in (([0, 1, 0], [0, 0, 1], 1), ([0, 0, 1], [0, 1, 0], -1)):
            env = {'u': [1, 0, 0], 'v': v, 'w': w}
            self.assertEqual(interpret(determinant, r['context'], env), expected)

    def test_zero_and_norm_signatures(self):
        r = self.rules['cross_self']
        self.assertEqual(r['replacement']['applicant']['name'], 'zero')
        self.assertEqual(interpret(r['replacement'], r['context'], {'u': [2, 3, 4]}), [0, 0, 0])
        bad_zero = copy.deepcopy(r['replacement'])
        bad_zero['arguments'][0]['integer'] = 2
        with self.assertRaises(ModelError):
            interpret(bad_zero, r['context'], {'u': [2, 3, 4]})
        r = self.rules['lagrange_norm']
        self.assertEqual(r['pattern']['applicant']['name'], 'power')
        self.assertEqual(r['pattern']['arguments'][0]['applicant'],
                         {'kind': 'OMS', 'cd': 'norm1', 'name': 'Euclidean_norm'})
