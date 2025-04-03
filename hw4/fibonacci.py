from threading import Thread
from multiprocessing import Process
import time


def fibonacci(n: int) -> int:
    if n < 2:
        return n

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, b + a

    return b


def sync_launch(n: int, times: int) -> None:
    for _ in range(times):
        fibonacci(n)


def thread_launch(n: int, times: int) -> None:
    threads: list[Thread] = []

    for i in range(times):
        thread: Thread = Thread(target=fibonacci, name=f"thread {i}", args=(n,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def process_launch(n: int, times: int) -> None:
    processes: list[Process] = []

    for i in range(times):
        process: Process = Process(target=fibonacci, name=f"process {i}", args=(n,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == "__main__":
    n = 250_000
    times = 10
    start_sync = time.time()
    sync_time = sync_launch(n, times)
    end_sync = time.time()

    start_thread = time.time()
    thread_time = thread_launch(n, times)
    end_thread = time.time()

    start_process = time.time()
    process_time = process_launch(n, times)
    end_process = time.time()

    with open("artifacts/task1/benchmarks.txt", "w") as benchmarks:
        benchmarks.write(f"sync time: {end_sync - start_sync} sec\n")
        benchmarks.write(f"threads time: {end_thread - start_thread} sec\n")
        benchmarks.write(f"processes time: {end_process - start_process} sec\n")
