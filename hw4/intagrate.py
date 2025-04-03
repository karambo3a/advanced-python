import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from multiprocessing import cpu_count


def integrate_part(f, a, b, start, end, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(
    f,
    a,
    b,
    executor_type: str,
    n_jobs=1,
    n_iter=10_000_000,
):
    part_size = n_iter // n_jobs
    futures = []
    executor = None
    if executor_type == "thread":
        executor = ThreadPoolExecutor(max_workers=n_jobs)
    else:
        executor = ProcessPoolExecutor(max_workers=n_jobs)

    for i in range(n_jobs):
        start = i * part_size
        end = (i + 1) * part_size
        futures.append(executor.submit(integrate_part, f, a, b, start, end, n_iter))

    result = sum(future.result() for future in futures)

    return result


def benchmark(executor: str, f, a, b, n_jobs=1) -> int:
    start = time.time()
    integrate(f, a, b, executor, n_jobs)
    end = time.time()
    return end - start


if __name__ == "__main__":
    data = (math.cos, 0, math.pi / 2)

    with open("artifacts/task2/benchmarks.txt", "w") as benchmarks:
        for n_jobs in range(1, cpu_count() * 2 + 1):
            benchmarks.write(f"{n_jobs} jobs\n")
            benchmarks.write(f"threads {benchmark("thread", *data, n_jobs)}\n")
            benchmarks.write(f"processes {benchmark("process", *data, n_jobs)}\n\n")
