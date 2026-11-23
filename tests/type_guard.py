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


def infer(expr, context):
    """Return a declared or derived shape; reject unknown constructs."""
    if not isinstance(expr, dict):
        raise ContextError('expected an OpenMath expression object')
    if expr.get('kind') == 'OMV' and set(expr) == {'kind', 'name'}:
        name = expr['name']
        if not isinstance(name, str) or name not in context:
            raise ContextError('undeclared variable')
        return _checked_type(context[name])
    if expr.get('kind') != 'OMA' or set(expr) != {'kind', 'applicant', 'arguments'}:
        raise ContextError('unsupported expression')
    op, args = expr['applicant'], expr['arguments']
    if (not isinstance(op, dict) or set(op) != {'kind', 'cd', 'name'}
            or op['kind'] != 'OMS' or not isinstance(args, list)):
        raise ContextError('invalid application')
    symbol = (op['cd'], op['name'])
    if symbol == ('linalg1', 'transpose') and len(args) == 1:
        operand = infer(args[0], context)
        if operand[0] != 'matrix':
            raise ContextError('transpose requires a matrix')
        return ('matrix', operand[2], operand[1])
    if symbol in (('arith1', 'plus'), ('arith1', 'times')) and len(args) == 2:
        a, b = (infer(arg, context) for arg in args)
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


def validate_equality(lhs, rhs, context):
    if infer(lhs, context) != infer(rhs, context):
        raise ContextError('sides have different types')
    return True
