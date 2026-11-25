"""Independent numerical reader for the standard oriented real three-space profile."""

import math
import operator

from numerical import add, cross, det, dot, vecadd, vecscale


class ModelError(ValueError):
    """The requested model, signature or binding is outside this profile."""


SPACE = {'dimension': 3, 'metric': 'euclidean', 'orientation': 'right_handed',
         'coordinates': 'standard_orthonormal_basis'}


def validate_context(ctx):
    if (not isinstance(ctx, dict) or set(ctx) != {'variables', 'space', 'scalar_domains'}
            or ctx['space'] != SPACE or ctx['scalar_domains'] != ['setname1#R']):
        raise ModelError('expected the standard oriented real Euclidean three-space')
    names = ctx['variables']
    if (not isinstance(names, dict) or not names
            or any(not isinstance(n, str) or not n or d != {'kind': 'vector', 'dimension': 3}
                   for n, d in names.items())):
        raise ModelError('expected real three-vector declarations')
    return names


def guard_allows(guard, bindings):
    if guard is None:
        return True
    if (not isinstance(guard, dict) or set(guard) != {'kind', 'less', 'greater'}
            or guard['kind'] != 'strict_variable_name_order'
            or not all(isinstance(guard[k], str) for k in ('less', 'greater'))):
        raise ModelError('unsupported application guard')
    operands = [bindings.get(guard[k]) for k in ('less', 'greater')]
    if not all(isinstance(o, dict) and set(o) == {'kind', 'name'} and o['kind'] == 'OMV'
               and isinstance(o['name'], str) and o['name'] for o in operands):
        return False
    return operands[0]['name'] < operands[1]['name']


def zero(size):
    if size != 3:
        raise ModelError('expected a three-dimensional zero vector')
    return [0, 0, 0]


def square(x, exponent):
    if exponent != 2:
        raise ModelError('only squared real scalars are in this profile')
    return x ** 2


SIGNATURES = {
    ('linalg1', 'vectorproduct', ('vector', 'vector')): ('vector', cross),
    ('linalg1', 'scalarproduct', ('vector', 'vector')): ('scalar', dot),
    ('linalg1', 'outerproduct', ('vector', 'vector')):
        ('matrix', lambda a, b: [[x * y for y in b] for x in a]),
    ('linalg1', 'determinant', ('matrix',)): ('scalar', det),
    ('linalg3', 'vector', ('integer', 'integer', 'integer')): ('vector', lambda *args: list(args)),
    ('linalg4vec', 'zero', ('integer',)): ('vector', zero),
    ('norm1', 'Euclidean_norm', ('vector',)): ('scalar', lambda v: math.hypot(*v)),
    ('arith1', 'unary_minus', ('vector',)): ('vector', lambda v: vecscale(-1, v)),
    ('arith1', 'plus', ('vector', 'vector')): ('vector', vecadd),
    ('arith1', 'plus', ('matrix', 'matrix')): ('matrix', add),
    ('arith1', 'minus', ('vector', 'vector')): ('vector', lambda u, v: vecadd(u, vecscale(-1, v))),
    ('arith1', 'minus', ('scalar', 'scalar')): ('scalar', operator.sub),
    ('arith1', 'times', ('scalar', 'vector')): ('vector', vecscale),
    ('arith1', 'times', ('scalar', 'scalar')): ('scalar', operator.mul),
    ('arith1', 'power', ('scalar', 'integer')): ('scalar', square),
}


def _read(term, env):
    if not isinstance(term, dict):
        raise ModelError('expected an OpenMath object')
    if term.get('kind') == 'OMI' and set(term) == {'kind', 'integer'} and type(term['integer']) is int:
        return 'integer', term['integer']
    if term.get('kind') == 'OMV' and set(term) == {'kind', 'name'}:
        if isinstance(term['name'], str) and term['name'] in env:
            return 'vector', env[term['name']]
        raise ModelError('undeclared variable')
    if term.get('kind') != 'OMA' or set(term) != {'kind', 'applicant', 'arguments'}:
        raise ModelError('expected a symbol application')
    head = term['applicant']
    if (not isinstance(head, dict) or set(head) != {'kind', 'cd', 'name'}
            or head['kind'] != 'OMS' or not all(isinstance(head[k], str) for k in ('cd', 'name'))
            or not isinstance(term['arguments'], list)):
        raise ModelError('malformed application')
    args = [_read(arg, env) for arg in term['arguments']]
    signature = head['cd'], head['name'], tuple(kind for kind, _ in args)
    if signature not in SIGNATURES:
        raise ModelError(f'unsupported symbol or signature {signature}')
    kind, operation = SIGNATURES[signature]
    return kind, operation(*(value for _, value in args))


def interpret(term, ctx, env):
    if set(env) != set(validate_context(ctx)):
        raise ModelError('bindings must match the declared variables')
    for v in env.values():
        if not isinstance(v, (list, tuple)) or len(v) != 3 or any(type(x) not in (int, float) for x in v):
            raise ModelError('expected three real coordinates')
    return _read(term, env)[1]
