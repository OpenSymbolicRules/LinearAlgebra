"""Run sanity checks and emit a machine-readable report to stdout."""

import json
import platform
import sys
import unittest

suite = unittest.defaultTestLoader.discover('tests', pattern='test_numerical.py')
result = unittest.TestResult()
suite.run(result)
report = {
    'purpose': 'numerical sanity checks; not formal verification',
    'python': platform.python_version(),
    'seeds': [20261123, 47, 81],
    'test_groups_run': result.testsRun,
    'failures': [{'test': str(t), 'details': message} for t, message in result.failures],
    'errors': [{'test': str(t), 'details': message} for t, message in result.errors],
    'successful': result.wasSuccessful(),
}
print(json.dumps(report, indent=2))
sys.exit(0 if result.wasSuccessful() else 1)
