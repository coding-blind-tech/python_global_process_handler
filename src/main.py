from src.global_process_handler import GlobalProcessHandler
from time import sleep, time


def generic_function_add(n):
    # sleep for 2 seconds
    sleep(2)
    print(f'Returning {n + 4}')
    return n + 4


def main():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    process_handler = GlobalProcessHandler([generic_function_add])
    # Submit the data with job
    process_handler.submit_modules(data)


if __name__ == '__main__':
    start_time = time() * 1000
    main()
    end_time = time() * 1000

    total_time = int(round((end_time - start_time) / 1000))
    print(f'the total time is {total_time}')