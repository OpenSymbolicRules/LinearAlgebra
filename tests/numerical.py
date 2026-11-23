"""Small real-matrix test oracle; not an OSR evaluator or production CAS."""


def shape(a):
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError('expected a nonempty rectangular matrix')
    return len(a), len(a[0])


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    if shape(a) != shape(b):
        raise ValueError('incompatible shapes')
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(k, a):
    shape(a)
    return [[k * x for x in row] for row in a]


def transpose(a):
    shape(a)
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    _, n = shape(a)
    p, _ = shape(b)
    if n != p:
        raise ValueError('incompatible shapes')
    return [[sum(x * y for x, y in zip(row, col)) for col in transpose(b)] for row in a]


def det(a):
    n, m = shape(a)
    if n != m:
        raise ValueError('expected square matrix')
    if n == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j] * det([r[:j] + r[j + 1:] for r in a[1:]])
               for j in range(n))


def inv(a):
    n, m = shape(a)
    if n != m:
        raise ValueError('expected square matrix')
    rows = [[float(x) for x in row] + unit for row, unit in zip(a, eye(n))]
    for j in range(n):
        pivot = max(range(j, n), key=lambda i: abs(rows[i][j]))
        if abs(rows[pivot][j]) < 1e-12:
            raise ValueError('singular matrix')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        divisor = rows[j][j]
        rows[j] = [x / divisor for x in rows[j]]
        for i in range(n):
            if i != j:
                factor = rows[i][j]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def trace(a):
    n, m = shape(a)
    if n != m:
        raise ValueError('expected square matrix')
    return sum(a[i][i] for i in range(n))


def expm(a):
    n, m = shape(a)
    if n != m:
        raise ValueError('expected square matrix')
    # Fixed Taylor series: only used for small, bounded matrices in this suite.
    result = term = eye(n)
    for k in range(1, 50):
        term = scale(1 / k, matmul(term, a))
        result = add(result, term)
    return result


def vecscale(k, v):
    return [k * x for x in v]


def vecadd(u, v):
    if len(u) != len(v):
        raise ValueError('incompatible vector lengths')
    return [x + y for x, y in zip(u, v)]


def dot(u, v):
    if len(u) != len(v):
        raise ValueError('incompatible vector lengths')
    return sum(x * y for x, y in zip(u, v))


def cross(u, v):
    if len(u) != 3 or len(v) != 3:
        raise ValueError('cross product requires dimension three')
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
