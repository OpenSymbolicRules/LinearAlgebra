"""Research-only shape guard for a finite, explicitly listed OpenMath fragment.

This is not a schema validator, a rule matcher, or a semantic interpretation.
All variables are assumed to use the same scalar carrier. Symbolic dimensions
are equal only when their declarations are identical; no inference is guessed.
"""


class ContextError(ValueError):
    """An unsupported, ill-formed, or incompatible expression was supplied."""


def _checked_type(value):
    if not isinstance(value, tuple) or not value:
        raise ContextError('invalid type declaration')
    if value[0] == 'scalar' and len(value) == 1:
        return value
    if value[0] == 'vector' and len(value) == 2:
        dims = value[1:]
    elif value[0] == 'matrix' and len(value) == 3:
        dims = value[1:]
    else:
        raise ContextError('unsupported type declaration')
    if not all((type(x) is int and x > 0) or (isinstance(x, str) and x)
               for x in dims):
        raise ContextError('invalid dimension')
    return value


def _dimension(expr, context, dimensions):
    if isinstance(expr, dict):
        if set(expr) == {'kind', 'name'} and expr['kind'] == 'OMV':
            name = expr['name']
            if isinstance(name, str) and dimensions is not None and name in dimensions and name not in context:
                return name
        if set(expr) == {'kind', 'integer'} and expr['kind'] == 'OMI':
            value = expr['integer']
            if type(value) is int and value > 0:
                return value
    raise ContextError('expected a declared dimension or positive integer size')


def infer(expr, context, dimensions=None):
    """Return a declared or derived shape; reject unknown constructs."""
    if not isinstance(expr, dict):
        raise ContextError('expected an OpenMath expression object')
    if set(expr) == {'kind', 'integer'} and expr.get('kind') == 'OMI':
        if type(expr['integer']) is not int:
            raise ContextError('invalid integer literal')
        return ('scalar',)
    if expr.get('kind') == 'OMV' and set(expr) == {'kind', 'name'}:
        name = expr['name']
        if not isinstance(name, str) or name not in context or (dimensions is not None and name in dimensions):
            raise ContextError('undeclared or ambiguous variable')
        shape = _checked_type(context[name])
        if dimensions is not None and any(isinstance(d, str) and
                                          (d not in dimensions or d in context) for d in shape[1:]):
            raise ContextError('undeclared or ambiguous shape dimension')
        return shape
    if expr.get('kind') != 'OMA' or set(expr) != {'kind', 'applicant', 'arguments'}:
        raise ContextError('unsupported expression')
    op, args = expr['applicant'], expr['arguments']
    if (not isinstance(op, dict) or set(op) != {'kind', 'cd', 'name'}
            or op['kind'] != 'OMS' or not isinstance(args, list)):
        raise ContextError('invalid application')
    symbol = (op['cd'], op['name'])
    if symbol == ('linalg5', 'identity') and len(args) == 1:
        size = _dimension(args[0], context, dimensions)
        return ('matrix', size, size)
    if symbol == ('arith1', 'power') and len(args) == 2:
        if infer(args[0], context, dimensions) != ('scalar',):
            raise ContextError('expected a scalar power base')
        _dimension(args[1], context, dimensions)
        return ('scalar',)
    if symbol == ('linalg1', 'determinant') and len(args) == 1:
        operand = infer(args[0], context, dimensions)
        if operand[0] != 'matrix' or operand[1] != operand[2]:
            raise ContextError('determinant requires a square matrix')
        return ('scalar',)
    if symbol == ('linalg1', 'transpose') and len(args) == 1:
        operand = infer(args[0], context, dimensions)
        if operand[0] != 'matrix':
            raise ContextError('transpose requires a matrix')
        return ('matrix', operand[2], operand[1])
    if symbol in (('arith1', 'plus'), ('arith1', 'times')) and len(args) == 2:
        a, b = (infer(arg, context, dimensions) for arg in args)
        if symbol[1] == 'plus':
            if a != b:
                raise ContextError('addition requires identical types')
            return a
        if a == ('scalar',):
            return b
        if b == ('scalar',):
            return a
        if a[0] == 'matrix' and b[0] == 'matrix' and a[2] == b[1]:
            return ('matrix', a[1], b[2])
        if a[0] == 'matrix' and b[0] == 'vector' and a[2] == b[1]:
            return ('vector', a[1])
        raise ContextError('unsupported or incompatible ordered product')
    raise ContextError('unknown symbol or unsupported arity')


def validate_equality(lhs, rhs, context, dimensions=None):
    if infer(lhs, context, dimensions) != infer(rhs, context, dimensions):
        raise ContextError('sides have different types')
    return True
