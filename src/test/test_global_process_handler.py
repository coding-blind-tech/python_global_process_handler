import unittest
from time import sleep
from unittest.mock import MagicMock, patch
from src.global_process_handler import GlobalProcessHandler


def generic_function_add(n):
    # sleep for 2 seconds
    sleep(2)
    print(f'Returning {n + 4}')
    return n + 4


class CustomMockExecutor:
    def __init__(self, max_workers=None):
        self._max_workers = max_workers
        self.submit = MagicMock(return_value="result")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class TestGlobalProcessHandler(unittest.TestCase):

    def setUp(self):
        self.funcs_to_run = [generic_function_add]
        self.handler = GlobalProcessHandler(self.funcs_to_run)

    @patch('src.test.test_global_process_handler.CustomMockExecutor')
    @patch('src.global_process_handler.concurrent.futures.as_completed')
    def test_submit_modules(self, mock_as_completed, mock_executor_class):
        # Mocking as_completed to return mock future objects
        mock_future = MagicMock()
        mock_future.result.return_value = "result"
        mock_as_completed.return_value.__iter__.return_value = [mock_future]

        # Test with some data
        data_set = [1, 2, 3]
        
        # Capture the instance of CustomMockExecutor used in the test
        with patch('src.test.test_global_process_handler.CustomMockExecutor') as mock_executor_class:
            self.handler.submit_modules(data_set)
            # Get the instance of CustomMockExecutor
            mock_executor_instance = mock_executor_class.return_value

        # Assertions
        expected_calls = len(self.funcs_to_run) * len(data_set)
        # self.assertEqual(mock_executor_instance.submit.call_count, expected_calls)
        # mock_executor_instance.submit.assert_called()
        mock_as_completed.assert_called_with([mock_future])
