test:
    python3 -m unittest discover -s tests -v

report:
    python3 tests/run_checks.py

docs:
    julia --project=docs docs/make.jl
