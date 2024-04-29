import concurrent.futures
import logging
import os

logger = logging.getLogger(f'app.global_process.{__name__}')


class GlobalProcessHandler():
    """ This class is used to run multiple functions in parallel using the ProcessPoolExecutor"""
    
    def __init__(self, funcs_to_run, cpus_to_use=0):
        logger.info('Initializing GlobalProcessHandler')

        self.funcs_to_run = funcs_to_run
        self.os_core_count = os.cpu_count()
        self.cpus_to_use = cpus_to_use

        if self.cpus_to_use == 0:
            self.max_workers = self.os_core_count
        else:
            self.max_workers = self.cpus_to_use


    def determine_cpus_to_use(self):
        """ This function determines the number of cpus to use"""

        logger.info('Determining cpus to use')
        if self.os_core_count >= 4:
            return self.os_core_count - 2
        else:
            return 1


    def submit_modules(self, data_set=[]):
        """ This function submits the modules to the ProcessPoolExecutor"""

        logger.info('Submitting modules')
        result_store = []

        # Determine CPU count
        if self.cpus_to_use == 0:
            self.max_workers = self.determine_cpus_to_use()

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            requests_to_make = []
            for module in self.funcs_to_run:
                for data in data_set:
                    try:
                        job_req = executor.submit(module, data)
                    except Exception as e:
                        logger.error(f'Error submitting process: {e}')
                        raise e
                    requests_to_make.append(job_req)

            for fn in concurrent.futures.as_completed(requests_to_make):
                try:
                    result = fn.result()
                    logger.info(f"the result is {result}")
                    result_store.append(result)
                except Exception as e:
                    logger.error(f'Error getting result: {e}')
                    raise e
        return result_store
