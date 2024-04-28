import concurrent.futures
import logging
import os
import itertools

# logger = logging.getLogger(f'global_process.{__name__}')


class GlobalProcessHandler():
    def __init__(self, funcs_to_run):
        # Can run one function, but allows for parallel processing
        self.funcs_to_run = funcs_to_run
        self.os_core_count = os.cpu_count()

        # properties for process/thread pool executor
        # setting the same defaults here that are set in current futures
        self.max_workers = None
        self.initializer = None
        self.initargs = ()
        self.max_tasks_per_child = None

        print("Getting started with multiprocessing global handler")

    def submit_modules(self, data_set=[]):
        modules_to_run = self.funcs_to_run
        print(f"looking at system total logical cores: {os.cpu_count()}")
        cores_to_use = self.os_core_count
        if cores_to_use <= 16:
            cores_to_use /= 2
        elif cores_to_use <= 96:
            cores_to_use /= 4
        else:
            cores_to_use /= 8

        self.max_workers = int(cores_to_use)
        print(
            f"The cores for max workers is going to be {self.max_workers}")

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            print(f"the max workers is {self.max_workers}")
            requests_to_make = []
            for module in modules_to_run:
                for data in data_set:
                    job_req = executor.submit(module, data)
                    requests_to_make.append(job_req)

            for fn in concurrent.futures.as_completed(requests_to_make):
                print(f"the result is {fn.result()}")
