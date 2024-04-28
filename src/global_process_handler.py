import concurrent.futures
import logging
import os
import itertools

# logger = logging.getLogger(f'global_process.{__name__}')


class GlobalProcessHandler():
    def __init__(self, funcs_to_run, cpus_to_use=0):
        # Can run one function, but allows for parallel processing
        self.funcs_to_run = funcs_to_run
        self.os_core_count = os.cpu_count()

        if cpus_to_use < 1:
            self.max_workers = self.os_core_count
        else:
            self.max_workers = cpus_to_use

        self.initializer = None
        self.initargs = ()
        self.max_tasks_per_child = None

        print("Getting started with multiprocessing global handler")

    def submit_modules(self, data_set=[]):
        print(
            f"The cores for max workers is going to be {self.max_workers}")

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            requests_to_make = []
            for module in self.funcs_to_run:
                for data in data_set:
                    job_req = executor.submit(module, data)
                    requests_to_make.append(job_req)

            for fn in concurrent.futures.as_completed(requests_to_make):
                print(f"the result is {fn.result()}")
