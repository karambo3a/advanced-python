from multiprocessing import Process, Pipe, Queue
from multiprocessing.connection import Connection
from threading import Thread, Event
import sys
import time
import codecs


def write_to_file(str):
    with open("artifacts/task3/proc_and_pipes.txt", "a") as f:
        f.write(str)


def a_func(queue: Queue, a_b_conn: Connection, is_running: Event) -> None:
    try:
        while is_running.is_set():
            if not queue.empty():
                data: str = queue.get()
                write_to_file(
                    f"[{time.ctime()}] Process A received from Main process: {data} \n"
                )
                processed = data.lower()
                write_to_file(f"[{time.ctime()}] Process A processed: {processed} \n")
                a_b_conn.send(processed)
                time.sleep(5)
    except KeyboardInterrupt:
        is_running.clear()


def b_func(b_a_conn: Connection, b_main_conn: Connection, is_running: Event) -> None:
    try:
        while is_running.is_set():
            if b_a_conn.poll(0.1):
                data = b_a_conn.recv()
                write_to_file(f"[{time.ctime()}] Process B received from A: {data} \n")
                encoded = codecs.encode(data, "rot_13")
                print(encoded)
                write_to_file(f"[{time.ctime()}] Process B encoded: {encoded}\n")
                b_main_conn.send(encoded)
    except KeyboardInterrupt:
        is_running.clear()


def sender_func(queue: Queue, is_running: Event) -> None:
    try:
        while is_running.is_set():
            line = sys.stdin.readline().strip()
            queue.put(line)
            write_to_file(f"[{time.ctime()}] Input: {line}\n")
    except KeyboardInterrupt:
        is_running.clear()


def getter_func(main_b_conn: Connection, is_running: Event):
    queue: Queue = Queue()
    try:
        while is_running.is_set():
            if main_b_conn.poll(0.1):
                data = main_b_conn.recv()
                queue.put(data)
                write_to_file(
                    f"[{time.ctime()}] Main process received from B: {data}\n"
                )
    except KeyboardInterrupt:
        is_running.clear()


def shutdown(
    sender_thread: Thread,
    getter_thread: Thread,
    A: Process,
    B: Process,
    conns: list[Connection],
) -> None:
    sender_thread.join(timeout=0.5)
    getter_thread.join(timeout=0.5)
    if A.is_alive():
        A.terminate()
    if B.is_alive():
        B.terminate()
    for conn in conns:
        conn.close()


def main():
    is_running = Event()
    is_running.set()

    queue: Queue = Queue()
    a_b_conn, b_a_conn = Pipe()
    main_b_conn, b_main_conn = Pipe()

    A: Process = Process(
        target=a_func, name="A process", args=(queue, a_b_conn, is_running)
    )
    B: Process = Process(
        target=b_func, name="B process", args=(b_a_conn, b_main_conn, is_running)
    )
    sender_thread: Thread = Thread(
        target=sender_func,
        name="sender thread",
        args=(queue, is_running),
        daemon=True,
    )
    getter_thread: Thread = Thread(
        target=getter_func,
        name="getter thread",
        args=(main_b_conn, is_running),
        daemon=True,
    )
    write_to_file("Program started\n")

    A.start()
    B.start()
    sender_thread.start()
    getter_thread.start()

    try:
        A.join()
        B.join()
    except KeyboardInterrupt:
        is_running.clear()
        write_to_file(f"[{time.ctime()}] Stopping\n")
    finally:

        shutdown(
            sender_thread,
            getter_thread,
            A,
            B,
            [a_b_conn, b_a_conn, main_b_conn, b_main_conn],
        )

        write_to_file(f"[{time.ctime()}] Program stopped\n")


if __name__ == "__main__":
    main()
