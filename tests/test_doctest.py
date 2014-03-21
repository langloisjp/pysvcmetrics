import unittest
import doctest
import metrics
import statsdclient

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(metrics))
    tests.addTests(doctest.DocTestSuite(statsdclient))
    return tests
