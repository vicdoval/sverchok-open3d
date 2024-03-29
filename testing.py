
from os.path import join, dirname, basename
import logging
import unittest
from io import StringIO
from contextlib import contextmanager

import sverchok
from sverchok.utils.sv_logging import sv_logger
import sverchok_open3d

try:
    import coverage
    coverage_available = True
except ImportError:
    sv_logger.info("Coverage module is not installed")
    coverage_available = False

@contextmanager
def coverage_report():
    if not coverage_available:
        yield None
    else:
        try:
            cov = coverage.Coverage()
            cov.start()
            yield cov
        finally:
            cov.stop()
            cov.save()
            cov.html_report()

def get_tests_path():
    sv_ex_init = sverchok_open3d.__file__
    return join(dirname(sv_ex_init), "tests")

def run_all_tests(pattern=None):
    if pattern is None:
        pattern = "*_tests.py"

    tests_path = get_tests_path()
    log_handler = logging.FileHandler(join(tests_path, "sverchok_tests.log"), mode='w')
    logging.getLogger().addHandler(log_handler)
    try:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir = tests_path, pattern = pattern)
        buffer = StringIO()
        runner = unittest.TextTestRunner(stream = buffer, verbosity=2)
        with coverage_report():
            result = runner.run(suite)
            sv_logger.info("Test cases result:\n%s", buffer.getvalue())
            return result
    finally:
        logging.getLogger().removeHandler(log_handler)

if __name__ == "__main__":
    import sys
    try:
        #register()
        result = run_all_tests()
        if not result.wasSuccessful():
            # We have to raise an exception for Blender to exit with specified exit code.
            raise Exception("Some tests failed")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)

