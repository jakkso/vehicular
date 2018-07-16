import unittest

from tests.integration_test import WetRunOrCommaFuckTheMan as Command
from tests.test_database import TestDatabase

if __name__ == '__main__':
    # Add additional test classes to this tuple
    test_classes = Command, TestDatabase

    loader = unittest.TestLoader()

    suites = []

    for test in test_classes:
        suites.append(loader.loadTestsFromTestCase(test))

    all_test_suites = unittest.TestSuite(suites)

    runner = unittest.TextTestRunner()
    results = runner.run(all_test_suites)
