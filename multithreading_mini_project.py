"""Core Python Multithreading Mini Project.

Run this file directly to see short, safe demonstrations of the most useful
parts of Python's standard-library threading toolkit::

    python multithreading_mini_project.py

The project is intentionally kept in one file. It models a tiny "order
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

Note: Python threads are excellent for I/O-bound work and coordination. For
CPU-heavy parallelism, use multiprocessing or native/vectorized libraries
because CPython's Global Interpreter Lock (GIL) limits simultaneous execution
of Python bytecode in multiple threads.

Author: Chaitanya Dasadiya
GitHub: https://github.com/cdasadiya
LinkedIn: https://in.linkedin.com/in/chaitanya-dasadiya
"""

from __future__ import annotations

import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Iterable, TextIO


DEFAULT_STOCK = {"book": 3, "pen": 4, "bag": 2}
DEFAULT_ORDER_ITEMS = ("book", "pen", "bag", "book", "pen", "bag", "book", "pen", "pen", "bag")


@dataclass(frozen=True)
class Order:
    """A small unit of work passed safely between threads with Queue."""

    order_id: int
    item: str
    prep_seconds: float

    def __post_init__(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id must be a positive integer")
        if not self.item:
            raise ValueError("item must be a non-empty string")
        if self.prep_seconds < 0:
            raise ValueError("prep_seconds cannot be negative")


@dataclass(frozen=True)
class ProcessingSummary:
    """Immutable result returned by OrderProcessingCenter.run()."""

    reserved_orders: int
    out_of_stock_orders: int
    remaining_stock: dict[str, int]
    audit_lines: tuple[str, ...]
    reached_target: bool


class Inventory:
    """Shared inventory protected by Lock.

    Lock usage: every read or write of stock and reserved order counters is
    done inside ``with self._lock`` so two worker threads cannot update those
    values at the same time.
    """

    def __init__(self, initial_stock: dict[str, int]) -> None:
        if any(quantity < 0 for quantity in initial_stock.values()):
            raise ValueError("initial_stock cannot contain negative quantities")

        self.stock = initial_stock.copy()
        self.reserved_orders = 0
        self.out_of_stock_orders = 0
        self._lock = threading.Lock()

    def reserve_item(self, item: str) -> bool:
        """Reserve one item if available; returns False when stock is empty."""

        with self._lock:
            available = self.stock.get(item, 0)
            if available <= 0:
                self.out_of_stock_orders += 1
                return False
            self.stock[item] = available - 1
            self.reserved_orders += 1
            return True

    def snapshot(self) -> tuple[dict[str, int], int, int]:
        """Return a consistent copy of shared state while holding the lock."""

        with self._lock:
            return self.stock.copy(), self.reserved_orders, self.out_of_stock_orders


class ReentrantAuditLog:
    """Audit logger that demonstrates RLock.

    RLock usage: ``write_order_event`` acquires the lock and calls
    ``_write_line``, which also acquires the same lock. A normal Lock would
    deadlock here; RLock allows re-entry by the owning thread.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._lines: list[str] = []

    def write_order_event(self, order: Order, status: str) -> None:
        """Append a thread-safe audit line for an order status change."""

        with self._lock:
            self._write_line(f"order={order.order_id} item={order.item} status={status}")

    def _write_line(self, text: str) -> None:
        with self._lock:
            self._lines.append(f"{threading.current_thread().name}: {text}")

    def snapshot(self) -> tuple[str, ...]:
        """Return an immutable copy of audit lines for safe external reading."""

        with self._lock:
            return tuple(self._lines)


class OrderProcessingCenter:
    """Mini application that combines the low-level threading primitives."""

    def __init__(
        self,
        orders: Iterable[Order],
        worker_count: int = 3,
        initial_stock: dict[str, int] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        output: TextIO | None = None,
    ) -> None:
        if worker_count <= 0:
            raise ValueError("worker_count must be greater than zero")

        self.orders = list(orders)
        self.worker_count = worker_count
        self.tasks: queue.Queue[Order | None] = queue.Queue()
        self.inventory = Inventory(DEFAULT_STOCK if initial_stock is None else initial_stock)
        self.audit_log = ReentrantAuditLog()
        self.sleep = sleep
        self.output = output
        self.worker_errors: list[BaseException] = []
        self._worker_errors_lock = threading.Lock()
        self._orders_loaded = False

        # Event: workers wait until the manager signals that work may start.
        self.start_event = threading.Event()

        # Event: a graceful stop flag checked by workers between tasks.
        self.stop_event = threading.Event()

        # Condition: manager waits until reserved_orders reaches a target.
        self.progress_condition = threading.Condition()

        # Barrier: all workers announce readiness before the manager starts work.
        self.ready_barrier = threading.Barrier(worker_count + 1)

        # Semaphore: only two orders can use the packing station at once.
        self.packing_stations = threading.Semaphore(2)

        # BoundedSemaphore: catches accidental over-release bugs.
        self.printers = threading.BoundedSemaphore(1)

        # local: each thread gets its own independent attributes.
        self.thread_context = threading.local()

    def _emit(self, message: str) -> None:
        print(message, file=self.output)

    def load_orders(self) -> None:
        """Put orders into Queue, followed by one sentinel per worker.

        Queue usage: Queue handles internal locking, so producers and consumers
        can safely call ``put`` and ``get`` from different threads.
        """

        if self._orders_loaded:
            raise RuntimeError("orders have already been loaded")

        for order in self.orders:
            self.tasks.put(order)
        for _ in range(self.worker_count):
            self.tasks.put(None)
        self._orders_loaded = True

    def worker(self, worker_number: int) -> None:
        """Thread target that processes orders until a sentinel is received."""

        try:
            self.thread_context.worker_number = worker_number
            self._emit(
                f"{threading.current_thread().name} ready "
                f"with local worker_number={self.thread_context.worker_number}"
            )
            self.ready_barrier.wait(timeout=5)
            self.start_event.wait(timeout=5)

            while not self.stop_event.is_set():
                try:
                    order = self.tasks.get(timeout=1)
                except queue.Empty:
                    if self.stop_event.is_set():
                        return
                    continue

                try:
                    if order is None:
                        return
                    self._process_order(order)
                finally:
                    self.tasks.task_done()
        except BaseException as exc:
            self.stop_event.set()
            with self._worker_errors_lock:
                self.worker_errors.append(exc)
            self._discard_pending_tasks()
            self._notify_progress()

    def _process_order(self, order: Order) -> None:
        """Reserve inventory, simulate I/O, and report progress."""

        if not self.inventory.reserve_item(order.item):
            self.audit_log.write_order_event(order, "out-of-stock")
            self._notify_progress()
            return

        self.sleep(order.prep_seconds)

        with self.packing_stations:
            self.sleep(0.03)

        with self.printers:
            self.sleep(0.01)
            self.audit_log.write_order_event(order, "packed-and-labeled")

        self._notify_progress()

    def _discard_pending_tasks(self) -> None:
        """Mark queued-but-unstarted tasks done after a worker failure.

        This keeps ``Queue.join`` from blocking forever if an unexpected worker
        exception occurs before every queued item has been consumed.
        """

        while True:
            try:
                self.tasks.get_nowait()
            except queue.Empty:
                return
            else:
                self.tasks.task_done()

    def _notify_progress(self) -> None:
        """Wake threads waiting on the Condition after progress changes."""

        with self.progress_condition:
            self.progress_condition.notify_all()

    def wait_until_processed(self, target: int, timeout: float = 3.0) -> bool:
        """Wait with Condition until at least ``target`` orders were reserved."""

        if target < 0:
            raise ValueError("target cannot be negative")

        def enough_orders_processed() -> bool:
            _stock, reserved, _out_of_stock = self.inventory.snapshot()
            return reserved >= target or bool(self.worker_errors)

        with self.progress_condition:
            return self.progress_condition.wait_for(enough_orders_processed, timeout=timeout)

    def run(self, progress_target: int = 4) -> ProcessingSummary:
        """Create Thread objects, coordinate them, print final state, and return it."""

        self.load_orders()
        workers = [
            threading.Thread(target=self.worker, args=(number,), name=f"worker-{number}")
            for number in range(1, self.worker_count + 1)
        ]

        for thread in workers:
            thread.start()

        self.ready_barrier.wait(timeout=5)
        self._emit(f"Active threads after start: {threading.active_count()}")
        self._emit("Thread names: " + ", ".join(thread.name for thread in threading.enumerate()))

        self.start_event.set()
        reached_target = self.wait_until_processed(target=progress_target)
        self._emit(f"Condition reached target of {progress_target} reserved orders: {reached_target}")

        self.tasks.join()
        for thread in workers:
            thread.join(timeout=5)
            if thread.is_alive():
                raise RuntimeError(f"{thread.name} did not stop cleanly")

        if self.worker_errors:
            raise RuntimeError("worker thread failed") from self.worker_errors[0]

        stock, reserved, out_of_stock = self.inventory.snapshot()
        audit_lines = self.audit_log.snapshot()
        self._emit(f"Reserved orders: {reserved}")
        self._emit(f"Out-of-stock orders: {out_of_stock}")
        self._emit(f"Remaining stock: {stock}")
        self._emit("Audit sample:")
        for line in audit_lines[:5]:
            self._emit(f"  {line}")

        return ProcessingSummary(
            reserved_orders=reserved,
            out_of_stock_orders=out_of_stock,
            remaining_stock=stock,
            audit_lines=audit_lines,
            reached_target=reached_target,
        )


def demonstrate_timer(delay: float = 0.05, output: TextIO | None = None) -> bool:
    """Timer usage: run a function after a short delay, then join it."""

    fired = threading.Event()

    def reminder() -> None:
        print("Timer fired: remember to review thread results.", file=output)
        fired.set()

    timer = threading.Timer(delay, reminder)
    timer.start()
    timer.join(timeout=delay + 1)
    return fired.is_set()


def demonstrate_thread_pool_executor(
    order_ids: Iterable[int] = range(1, 6),
    max_workers: int = 3,
    output: TextIO | None = None,
) -> list[str]:
    """ThreadPoolExecutor usage: submit callables and collect Future results."""

    if max_workers <= 0:
        raise ValueError("max_workers must be greater than zero")

    def fetch_tracking_status(order_id: int) -> str:
        time.sleep(0.01 + (order_id % 3) * 0.005)
        return f"order {order_id}: tracking-ready"

    results: list[str] = []
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="pool-worker") as executor:
        futures = [executor.submit(fetch_tracking_status, order_id) for order_id in order_ids]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"ThreadPoolExecutor result: {result}", file=output)
    return sorted(results)


def demonstrate_daemon_thread(output: TextIO | None = None) -> bool:
    """Daemon Thread usage: background work that should not block program exit.

    Daemon threads are useful for best-effort background tasks, but they can be
    stopped abruptly when only daemon threads remain. Do not use them for work
    that must be completed or cleaned up reliably.
    """

    stop_heartbeat = threading.Event()
    heartbeat_count = 0
    heartbeat_lock = threading.Lock()

    def heartbeat() -> None:
        nonlocal heartbeat_count
        while not stop_heartbeat.is_set():
            with heartbeat_lock:
                heartbeat_count += 1
            print("daemon heartbeat", file=output)
            time.sleep(0.03)

    thread = threading.Thread(target=heartbeat, name="daemon-heartbeat", daemon=True)
    thread.start()
    time.sleep(0.07)
    stop_heartbeat.set()
    thread.join(timeout=1)

    with heartbeat_lock:
        return heartbeat_count > 0 and not thread.is_alive()


def build_sample_orders(seed: int = 7) -> list[Order]:
    """Create predictable demo data for the mini project without global randomness."""

    rng = random.Random(seed)
    return [
        Order(order_id=index, item=item, prep_seconds=rng.uniform(0.01, 0.05))
        for index, item in enumerate(DEFAULT_ORDER_ITEMS, start=1)
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
