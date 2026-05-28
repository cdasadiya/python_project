"""Core Python Multithreading Mini Project.

Run this file directly to see short, safe demonstrations of the most useful
parts of Python's standard-library threading toolkit::

    python multithreading_mini_project.py

The project is intentionally kept in one file.  It models a tiny "order
processing center" where many worker threads prepare orders while shared
state is protected with synchronization primitives.

Covered topics
--------------
* Thread: run functions concurrently inside one Python process.
* current_thread, active_count, enumerate: inspect running threads.
* Lock: protect shared data from race conditions.
* RLock: allow the same thread to acquire a lock multiple times.
* Semaphore and BoundedSemaphore: limit access to a finite resource.
* Event: signal one or more threads to start or stop.
* Condition: wait until shared state reaches a required condition.
* Barrier: make threads meet at a synchronization point.
* Timer: schedule work after a delay.
* local: keep per-thread data isolated.
* queue.Queue: safely pass tasks between threads.
* ThreadPoolExecutor: a higher-level pool API built on threads.

Note: Python threads are excellent for I/O-bound work and coordination.  For
CPU-heavy parallelism, use multiprocessing or native/vectorized libraries
because CPython's Global Interpreter Lock (GIL) limits simultaneous execution
of Python bytecode in multiple threads.
"""

from __future__ import annotations

import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Iterable


# Keep the demo deterministic enough for learning while still looking like work.
random.seed(7)


@dataclass(frozen=True)
class Order:
    """A small unit of work passed safely between threads with Queue."""

    order_id: int
    item: str
    prep_seconds: float


class Inventory:
    """Shared inventory protected by Lock.

    Lock usage: every read or write of ``stock`` and ``processed_orders`` is
    done inside ``with self._lock`` so two worker threads cannot update those
    values at the same time.
    """

    def __init__(self, initial_stock: dict[str, int]) -> None:
        self.stock = initial_stock.copy()
        self.processed_orders = 0
        self._lock = threading.Lock()

    def reserve_item(self, item: str) -> bool:
        """Reserve one item if available; returns False when stock is empty."""

        with self._lock:
            available = self.stock.get(item, 0)
            if available <= 0:
                return False
            self.stock[item] = available - 1
            self.processed_orders += 1
            return True

    def snapshot(self) -> tuple[dict[str, int], int]:
        """Return a consistent copy of shared state while holding the lock."""

        with self._lock:
            return self.stock.copy(), self.processed_orders


class ReentrantAuditLog:
    """Audit logger that demonstrates RLock.

    RLock usage: ``write_order_event`` acquires the lock and calls
    ``_write_line``, which also acquires the same lock.  A normal Lock would
    deadlock here; RLock allows re-entry by the owning thread.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.lines: list[str] = []

    def write_order_event(self, order: Order, status: str) -> None:
        with self._lock:
            self._write_line(f"order={order.order_id} item={order.item} status={status}")

    def _write_line(self, text: str) -> None:
        with self._lock:
            self.lines.append(f"{threading.current_thread().name}: {text}")


class OrderProcessingCenter:
    """Mini application that combines the low-level threading primitives."""

    def __init__(self, orders: Iterable[Order], worker_count: int = 3) -> None:
        self.orders = list(orders)
        self.worker_count = worker_count
        self.tasks: queue.Queue[Order | None] = queue.Queue()
        self.inventory = Inventory({"book": 3, "pen": 4, "bag": 2})
        self.audit_log = ReentrantAuditLog()

        # Event: workers wait until the manager signals that work may start.
        self.start_event = threading.Event()

        # Event: a graceful stop flag checked by workers between tasks.
        self.stop_event = threading.Event()

        # Condition: manager waits until processed_orders reaches a target.
        self.progress_condition = threading.Condition()

        # Barrier: all workers announce readiness before the manager starts work.
        self.ready_barrier = threading.Barrier(worker_count + 1)

        # Semaphore: only two orders can use the packing station at once.
        self.packing_stations = threading.Semaphore(2)

        # BoundedSemaphore: catches accidental over-release bugs.
        self.printers = threading.BoundedSemaphore(1)

        # local: each thread gets its own independent attributes.
        self.thread_context = threading.local()

    def load_orders(self) -> None:
        """Put orders into Queue, followed by one sentinel per worker.

        Queue usage: Queue handles internal locking, so producers and consumers
        can safely call ``put`` and ``get`` from different threads.
        """

        for order in self.orders:
            self.tasks.put(order)
        for _ in range(self.worker_count):
            self.tasks.put(None)

    def worker(self, worker_number: int) -> None:
        """Thread target that processes orders until a sentinel is received."""

        self.thread_context.worker_number = worker_number
        print(f"{threading.current_thread().name} ready with local worker_number={worker_number}")
        self.ready_barrier.wait()
        self.start_event.wait()

        while not self.stop_event.is_set():
            order = self.tasks.get()
            try:
                if order is None:
                    return
                self._process_order(order)
            finally:
                self.tasks.task_done()

    def _process_order(self, order: Order) -> None:
        """Reserve inventory, simulate I/O, and report progress."""

        if not self.inventory.reserve_item(order.item):
            self.audit_log.write_order_event(order, "out-of-stock")
            self._notify_progress()
            return

        time.sleep(order.prep_seconds)

        with self.packing_stations:
            time.sleep(0.03)

        with self.printers:
            time.sleep(0.01)
            self.audit_log.write_order_event(order, "packed-and-labeled")

        self._notify_progress()

    def _notify_progress(self) -> None:
        """Wake threads waiting on the Condition after progress changes."""

        with self.progress_condition:
            self.progress_condition.notify_all()

    def wait_until_processed(self, target: int, timeout: float = 3.0) -> bool:
        """Wait with Condition until at least ``target`` orders were reserved."""

        def enough_orders_processed() -> bool:
            _stock, processed = self.inventory.snapshot()
            return processed >= target

        with self.progress_condition:
            return self.progress_condition.wait_for(enough_orders_processed, timeout=timeout)

    def run(self) -> None:
        """Create Thread objects, coordinate them, and print final state."""

        self.load_orders()
        workers = [
            threading.Thread(target=self.worker, args=(number,), name=f"worker-{number}")
            for number in range(1, self.worker_count + 1)
        ]

        for thread in workers:
            thread.start()

        self.ready_barrier.wait()
        print(f"Active threads after start: {threading.active_count()}")
        print("Thread names:", ", ".join(thread.name for thread in threading.enumerate()))

        self.start_event.set()
        reached_target = self.wait_until_processed(target=4)
        print(f"Condition reached target of 4 reserved orders: {reached_target}")

        self.tasks.join()
        for thread in workers:
            thread.join()

        stock, processed = self.inventory.snapshot()
        print(f"Processed/reserved orders: {processed}")
        print(f"Remaining stock: {stock}")
        print("Audit sample:")
        for line in self.audit_log.lines[:5]:
            print(f"  {line}")


def demonstrate_timer() -> None:
    """Timer usage: run a function after a short delay, then join it."""

    def reminder() -> None:
        print("Timer fired: remember to review thread results.")

    timer = threading.Timer(0.05, reminder)
    timer.start()
    timer.join()


def demonstrate_thread_pool_executor() -> None:
    """ThreadPoolExecutor usage: submit callables and collect Future results."""

    def fetch_tracking_status(order_id: int) -> str:
        time.sleep(random.uniform(0.01, 0.04))
        return f"order {order_id}: tracking-ready"

    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="pool-worker") as executor:
        futures = [executor.submit(fetch_tracking_status, order_id) for order_id in range(1, 6)]
        for future in as_completed(futures):
            print(f"ThreadPoolExecutor result: {future.result()}")


def demonstrate_daemon_thread() -> None:
    """Daemon Thread usage: background work that should not block program exit.

    Daemon threads are useful for best-effort background tasks, but they can be
    stopped abruptly when only daemon threads remain.  Do not use them for work
    that must be completed or cleaned up reliably.
    """

    def heartbeat() -> None:
        while not stop_heartbeat.is_set():
            print("daemon heartbeat")
            time.sleep(0.03)

    stop_heartbeat = threading.Event()
    thread = threading.Thread(target=heartbeat, name="daemon-heartbeat", daemon=True)
    thread.start()
    time.sleep(0.07)
    stop_heartbeat.set()
    thread.join(timeout=1)


def build_sample_orders() -> list[Order]:
    """Create predictable demo data for the mini project."""

    items = ["book", "pen", "bag", "book", "pen", "bag", "book", "pen", "pen", "bag"]
    return [
        Order(order_id=index, item=item, prep_seconds=random.uniform(0.01, 0.05))
        for index, item in enumerate(items, start=1)
    ]


def main() -> None:
    """Run every demonstration in a beginner-friendly order."""

    print("=== Core Python Multithreading Mini Project ===")
    demonstrate_timer()
    demonstrate_daemon_thread()
    center = OrderProcessingCenter(build_sample_orders(), worker_count=3)
    center.run()
    demonstrate_thread_pool_executor()
    print("=== Demo complete ===")


if __name__ == "__main__":
    main()
