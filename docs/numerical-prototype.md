# Numerical prototype

This prototype checks the formulas in the design, independently of any OSR
rule parser. It is not a validator, a CAS, an official rule collection, or a
formal proof. It uses Python's standard library and adds no dependencies.

Run from the research directory:

```sh
python3 -m unittest discover -s tests -v
python3 tests/run_checks.py
```

The second command prints a JSON report and exits nonzero on a test failure or
error. Four test groups exercise the 28 proposed mathematical identities,
six explicit counterexamples, incompatible matrix shapes and a singular
inverse. Seeds are fixed. Square cases use sizes 1, 2 and 3; the cyclic trace
and product transpose also use compatible rectangular matrices. Invertible
samples are triangular with unit diagonal, and exponential samples commute
because one matrix is a scalar multiple of the other. Vector samples use the
standard oriented real Euclidean space of dimension three.

The exponential uses a 49-term Taylor series for the deliberately small
bounded test inputs, with floating point comparisons at relative and absolute
tolerance `1e-9`. This is not a certified error bound. The inverse uses
floating point elimination and a singularity threshold; this is a test oracle,
not a numerical linear algebra implementation. The test set does not cover
complex matrices, general commuting matrix pairs, or schema-driven rule
execution. It cannot test whether OSR expressions encode these formulas
faithfully. Generated theorems and a reviewed semantic bridge remain necessary.

On Python 3.13.7, all four groups passed; the runner emits the actual Python
version and current failure information on every run.
