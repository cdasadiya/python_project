import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

pydantic = pytest.importorskip("pydantic")
ValidationError = pydantic.ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic_validation_demo import (
    Address,
    Order,
    Product,
    UserProfile,
    build_order,
    build_user_profile,
    example_order_payload,
    parse_user_json,
    serialize_model,
)


def valid_user_payload():
    return {
        "id": 10,
        "name": "  Ada Lovelace  ",
        "email": "ada@example.com",
        "age": 36,
        "address": {
            "street": "1 Algorithm Lane",
            "city": "London",
            "state": "LN",
            "postal_code": "12345-6789",
            "country": "gb",
        },
        "tags": " Math, Programming, math,  ",
    }


def test_build_user_profile_normalizes_whitespace_country_and_tags():
    user = build_user_profile(valid_user_payload())

    assert user.name == "Ada Lovelace"
    assert user.address.country == "GB"
    assert user.tags == ["math", "programming"]
    assert user.role == "customer"
    assert user.is_active is True


def test_user_profile_rejects_invalid_email_age_and_id():
    payload = valid_user_payload()
    payload.update({"id": 0, "email": "not-an-email", "age": 12})

    with pytest.raises(ValidationError) as error_info:
        build_user_profile(payload)

    error_fields = {error["loc"][0] for error in error_info.value.errors()}
    assert {"id", "email", "age"}.issubset(error_fields)


def test_address_rejects_invalid_postal_code():
    with pytest.raises(ValidationError, match="postal_code"):
        Address(
            street="123 Main Street",
            city="Boston",
            state="MA",
            postal_code="ABC123",
        )


def test_tags_accept_empty_values_as_empty_list():
    payload = valid_user_payload()
    payload["tags"] = None

    user = build_user_profile(payload)

    assert user.tags == []


def test_tags_reject_unsupported_container_type():
    payload = valid_user_payload()
    payload["tags"] = {"bad": "container"}

    with pytest.raises(ValidationError, match="tags must be a list"):
        build_user_profile(payload)


def test_product_rejects_bad_sku_and_non_positive_price():
    with pytest.raises(ValidationError) as error_info:
        Product(sku="bad-sku", name="Course", price=0)

    error_fields = {error["loc"][0] for error in error_info.value.errors()}
    assert {"sku", "price"} == error_fields


def test_order_computes_line_totals_and_order_total():
    order = build_order(example_order_payload())

    assert order.items[0].line_total == 99.98
    assert order.items[1].line_total == 15.5
    assert order.total == 115.48


def test_order_requires_at_least_one_item():
    payload = example_order_payload()
    payload["items"] = []

    with pytest.raises(ValidationError, match="items"):
        build_order(payload)


def test_order_rejects_invalid_order_id_and_quantity():
    payload = example_order_payload()
    payload["order_id"] = "123456"
    payload["items"][0]["quantity"] = 0

    with pytest.raises(ValidationError) as error_info:
        build_order(payload)

    locations = {error["loc"] for error in error_info.value.errors()}
    assert ("order_id",) in locations
    assert ("items", 0, "quantity") in locations


def test_order_requires_shipped_at_for_shipped_status():
    payload = example_order_payload()
    payload["status"] = "shipped"

    with pytest.raises(ValidationError, match="shipped_at is required"):
        build_order(payload)


def test_order_rejects_shipped_at_for_non_shipping_status():
    payload = example_order_payload()
    payload["status"] = "paid"
    payload["shipped_at"] = datetime.now(timezone.utc).isoformat()

    with pytest.raises(ValidationError, match="shipped_at is only allowed"):
        build_order(payload)


def test_order_accepts_shipped_status_with_shipped_at():
    payload = example_order_payload()
    payload["status"] = "shipped"
    payload["shipped_at"] = datetime.now(timezone.utc).isoformat()

    order = build_order(payload)

    assert order.status == "shipped"
    assert order.shipped_at is not None


def test_parse_user_json_validates_json_input():
    user = parse_user_json(json.dumps(valid_user_payload()))

    assert user.email == "ada@example.com"


def test_serialize_model_returns_json_friendly_dictionary():
    order = build_order(example_order_payload())
    serialized = serialize_model(order)

    assert serialized["customer"]["created_at"].endswith("Z")
    assert serialized["total"] == 115.48


def test_validate_assignment_applies_after_model_creation():
    user = build_user_profile(valid_user_payload())

    with pytest.raises(ValidationError):
        user.age = 121


def test_order_model_can_be_created_from_existing_model_instances():
    user = build_user_profile(valid_user_payload())
    order = Order(
        order_id="ORD-654321",
        customer=user,
        items=[
            {
                "product": Product(sku="TST-0001", name="Test Product", price=9.5),
                "quantity": 3,
            }
        ],
    )

    assert order.customer is user
    assert order.total == 28.5
