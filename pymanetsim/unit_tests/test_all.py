import pdb
""" %prog

  To run all the unit tests

"""

import unittest
from unit_tests.test_plane import TestPlane
from unit_tests.test_node import TestNode
from unit_tests.test_sim import TestSim
from unit_tests.test_dsr import TestDSR
from unit_tests.test_bfg import TestBFG
from unit_tests.test_bloom import TestERBBloom, TestBloom
from unit_tests.test_event import TestEvent
from unit_tests.test_messages import TestMessages
from unit_tests.test_plane_builders import TestPlaneBuilder
from unit_tests.test_sim_job import TestSimJob
from unit_tests.test_plot_plane import TestPlotPlane

def suite():
    """
    Runs all unitary tests"
    """
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestPlane))
    test_suite.addTest(unittest.makeSuite(TestNode))
    test_suite.addTest(unittest.makeSuite(TestDSR))
    test_suite.addTest(unittest.makeSuite(TestEvent))
    test_suite.addTest(unittest.makeSuite(TestBloom))
    test_suite.addTest(unittest.makeSuite(TestERBBloom))
    test_suite.addTest(unittest.makeSuite(TestBFG))
    test_suite.addTest(unittest.makeSuite(TestSim))
    test_suite.addTest(unittest.makeSuite(TestMessages))
    test_suite.addTest(unittest.makeSuite(TestPlaneBuilder))
    test_suite.addTest(unittest.makeSuite(TestSimJob))
    test_suite.addTest(unittest.makeSuite(TestPlotPlane))

    return test_suite

def run_unit_tests():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == '__main__':
    run_unit_tests()
