# Global Process Handler

## How To Use

### Import:
```python
import utils.Global_processing_handler as GPH
```

### Declaration:
```python
GPH.Global_processing_handler(inputlist, [worker_function])
```

## Properties

### Store Initial Available Cores
- `os_core_count`: The initial amount of logical cores.

### Properties for Process Pool Executor
- `max_workers`: The total amount of cores to use. A positive integer greater than 0. If not provided or set to None, the `max_workers` will equal the total amount of logical cores on the host machine. For Windows, it will be at most 61 cores even if the total amount of cores is more.
- `mp_context`: `mp_context` can be a multiprocessing context or None. It will be used to launch the workers. If `mp_context` is None or not given, the default multiprocessing context is used.
- `initializer`: A callable that is called at the start of each process. This is an optional parameter.
- `initargs`: A tuple of arguments passed to the initializer.
- `max_tasks_per_child`: An optional argument that specifies the maximum number of tasks a single process can execute before it will exit and be replaced with a fresh worker process. By default `max_tasks_per_child` is None which means worker processes will live as long as the pool.

## Methods
