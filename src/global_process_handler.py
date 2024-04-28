import concurrent.futures
import logging
import os

# logger = logging.getLogger(f'global_process.{__name__}')


class GlobalProcessHandler():
    def __init__(self, funcs_to_run, cpus_to_use=0):
        self.funcs_to_run = funcs_to_run
        self.os_core_count = os.cpu_count()

        if cpus_to_use < 1:
            self.max_workers = self.os_core_count
        else:
            self.max_workers = cpus_to_use


    def submit_modules(self, data_set=[]):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            requests_to_make = []
            for module in self.funcs_to_run:
                for data in data_set:
                    try:
                        job_req = executor.submit(module, data)
                    except Exception as e:
                        print(f'Error submitting process: {e}')
                        raise e
                    requests_to_make.append(job_req)

            for fn in concurrent.futures.as_completed(requests_to_make):
                try:
                    result = fn.result()
                    print(f"the result is {result}")
                except Exception as e:
                    print(f'Error getting result: {e}')
                    raise e
