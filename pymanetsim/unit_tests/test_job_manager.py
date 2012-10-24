import pdb
import job_manager
import unittest

import jobs.test_bfg_job
import jobs.test_dsr_job

class TestSimJob(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_bfg_job(self):
        job_manager.run_job_list((jobs.test_bfg_job,))


    def test_simple_dsr_job(self):
        job_manager.run_job_list((jobs.test_dsr_job,))


if __name__ == '__main__':
    unittest.main()
