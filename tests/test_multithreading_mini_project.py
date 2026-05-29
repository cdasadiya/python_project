import io
import random

import pytest

from multithreading_mini_project import (
    DEFAULT_ORDER_ITEMS,
    Inventory,
    Order,
    OrderProcessingCenter,
    ReentrantAuditLog,
    build_sample_orders,
    demonstrate_daemon_thread,
    demonstrate_thread_pool_executor,
    demonstrate_timer,
)


def no_sleep(_seconds: float) -> None:
    """Avoid real delays in tests while keeping the workflow intact."""


def test_order_validates_input():
    with pytest.raises(ValueError, match="order_id"):
        Order(order_id=0, item="book", prep_seconds=0)
    with pytest.raises(ValueError, match="item"):
        Order(order_id=1, item="", prep_seconds=0)
    with pytest.raises(ValueError, match="prep_seconds"):
        Order(order_id=1, item="book", prep_seconds=-0.1)


def test_inventory_reserves_items_and_tracks_out_of_stock():
    inventory = Inventory({"book": 1})

    assert inventory.reserve_item("book") is True
    assert inventory.reserve_item("book") is False
    assert inventory.reserve_item("unknown") is False

    stock, reserved, out_of_stock = inventory.snapshot()
    assert stock == {"book": 0}
    assert reserved == 1
    assert out_of_stock == 2


def test_inventory_rejects_negative_stock():
    with pytest.raises(ValueError, match="negative"):
        Inventory({"book": -1})


def test_reentrant_audit_log_records_thread_safe_snapshot():
    log = ReentrantAuditLog()
    order = Order(order_id=1, item="book", prep_seconds=0)

    log.write_order_event(order, "packed-and-labeled")

    assert log.snapshot() == ("MainThread: order=1 item=book status=packed-and-labeled",)


def test_build_sample_orders_is_deterministic_and_does_not_touch_global_random_state():
    random.seed(12345)
    before = random.random()
    orders = build_sample_orders(seed=7)
    after = random.random()

    random.seed(12345)
    assert before == random.random()
    assert after == random.random()
    assert [order.item for order in orders] == list(DEFAULT_ORDER_ITEMS)
    assert [order.order_id for order in orders] == list(range(1, len(DEFAULT_ORDER_ITEMS) + 1))


def test_order_processing_center_runs_full_workflow_and_returns_summary():
    output = io.StringIO()
    orders = [
        Order(order_id=1, item="book", prep_seconds=0),
        Order(order_id=2, item="book", prep_seconds=0),
        Order(order_id=3, item="pen", prep_seconds=0),
    ]
    center = OrderProcessingCenter(
        orders,
        worker_count=2,
        initial_stock={"book": 1, "pen": 1},
        sleep=no_sleep,
        output=output,
    )

    summary = center.run(progress_target=2)

    assert summary.reserved_orders == 2
    assert summary.out_of_stock_orders == 1
    assert summary.remaining_stock == {"book": 0, "pen": 0}
    assert summary.reached_target is True
    assert len(summary.audit_lines) == 3
    assert any("status=out-of-stock" in line for line in summary.audit_lines)
    assert center.tasks.unfinished_tasks == 0
    text = output.getvalue()
    assert "Condition reached target of 2 reserved orders: True" in text
    assert "Out-of-stock orders: 1" in text


def test_order_processing_center_worker_failure_raises_without_deadlock():
    def broken_sleep(_seconds: float) -> None:
        raise RuntimeError("simulated worker failure")

    orders = [
        Order(order_id=1, item="book", prep_seconds=0),
        Order(order_id=2, item="book", prep_seconds=0),
    ]
    center = OrderProcessingCenter(
        orders,
        worker_count=1,
        initial_stock={"book": 2},
        sleep=broken_sleep,
        output=io.StringIO(),
    )

    with pytest.raises(RuntimeError, match="worker thread failed"):
        center.run(progress_target=1)

    assert center.tasks.unfinished_tasks == 0


def test_order_processing_center_validates_configuration():
    with pytest.raises(ValueError, match="worker_count"):
        OrderProcessingCenter([], worker_count=0)

    center = OrderProcessingCenter([], worker_count=1, sleep=no_sleep, output=io.StringIO())
    with pytest.raises(ValueError, match="target"):
        center.wait_until_processed(-1)


def test_order_processing_center_load_orders_only_once():
    center = OrderProcessingCenter([], worker_count=1, sleep=no_sleep, output=io.StringIO())

    center.load_orders()

    with pytest.raises(RuntimeError, match="already been loaded"):
        center.load_orders()


def test_timer_demo_fires_and_reports_message():
    output = io.StringIO()

    assert demonstrate_timer(delay=0.001, output=output) is True
    assert "Timer fired" in output.getvalue()


def test_daemon_thread_demo_stops_cleanly():
    output = io.StringIO()

    assert demonstrate_daemon_thread(output=output) is True
    assert "daemon heartbeat" in output.getvalue()


def test_thread_pool_executor_returns_tracking_statuses():
    output = io.StringIO()

    results = demonstrate_thread_pool_executor(order_ids=[1, 2, 3], max_workers=2, output=output)

    assert results == [
        "order 1: tracking-ready",
        "order 2: tracking-ready",
        "order 3: tracking-ready",
    ]
    assert output.getvalue().count("ThreadPoolExecutor result:") == 3


def test_thread_pool_executor_validates_worker_count():
    with pytest.raises(ValueError, match="max_workers"):
        demonstrate_thread_pool_executor(max_workers=0)
