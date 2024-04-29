import unittest
import logging
from time import sleep
from unittest.mock import Mock
from src.global_process_handler import GlobalProcessHandler
from src.utils.app_logging.app_logging import logging_setup

logging_setup()
logger = logging.getLogger(f'app.test_global_process_handler.{__name__}')

def generic_func(n):
    sleep(1)
    return n * 2

def generic_func_two(n):
    sleep(1)
    return n * 3


class TestGlobalProcessHandler(unittest.TestCase):
    def setUp(self):
        logger.info('Initializing TestGlobalProcessHandler')
        self.funcs_to_run = [generic_func, generic_func_two]
        self.data_set = [1, 2, 3]
        self.global_process_handler = GlobalProcessHandler(self.funcs_to_run)

    def test_submit_modules(self):
        results = self.global_process_handler.submit_modules(self.data_set)
        # Sort results for comparison
        # This is because executor.submit() returns results in order they complete
        sorted_results = sorted(results)
        self.assertEqual(sorted_results, [2, 3, 4, 6, 6, 9])
