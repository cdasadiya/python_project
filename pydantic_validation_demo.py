"""
Pydantic validation examples for user profiles and orders.

This module demonstrates practical Pydantic v2 features:
- nested models
- constrained fields
- enum values
- field and model validators
- computed fields
- JSON parsing and serialization helpers

Author: Chaitanya Dasadiya
GitHub: https://github.com/cdasadiya
LinkedIn: https://in.linkedin.com/in/chaitanya-dasadiya
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


class UserRole(str, Enum):
    """Supported user roles."""

    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPPORT = "support"


class Address(BaseModel):
    """Validated mailing address."""

    street: str = Field(min_length=1, max_length=120)
    city: str = Field(min_length=1, max_length=80)
    state: str = Field(min_length=2, max_length=50)
    postal_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")
    country: str = Field(default="US", min_length=2, max_length=2)

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    @field_validator("country")
    @classmethod
    def normalize_country(cls, value: str) -> str:
        """Store country codes in uppercase ISO-like form."""

        return value.upper()


class UserProfile(BaseModel):
    """Validated user profile data."""

    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    age: int = Field(ge=13, le=120)
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True
    address: Address
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value: Any) -> list[str]:
        """Accept a comma-separated string or list and return unique lowercase tags."""

        if value is None or value == "":
            return []
        if isinstance(value, str):
            raw_tags = value.split(",")
        elif isinstance(value, list):
            raw_tags = value
        else:
            raise ValueError("tags must be a list or comma-separated string")

        normalized: list[str] = []
        seen: set[str] = set()
        for tag in raw_tags:
            cleaned = str(tag).strip().lower()
            if cleaned and cleaned not in seen:
                normalized.append(cleaned)
                seen.add(cleaned)
        return normalized


class Product(BaseModel):
    """Validated product catalog entry."""

    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


class OrderItem(BaseModel):
    """A single order line with a computed line total."""

    product: Product
    quantity: int = Field(gt=0, le=100)

    @computed_field
    @property
    def line_total(self) -> float:
        """Return the item subtotal rounded to cents."""

        return round(self.product.price * self.quantity, 2)


class Order(BaseModel):
    """Validated order with cross-field status checks."""

    order_id: str = Field(pattern=r"^ORD-\d{6}$")
    customer: UserProfile
    items: list[OrderItem] = Field(min_length=1)
    status: Literal["draft", "paid", "shipped", "delivered", "cancelled"] = "draft"
    shipped_at: datetime | None = None

    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def validate_shipping_state(self) -> "Order":
        """Keep shipped timestamp consistent with the order status."""

        shipping_statuses = {"shipped", "delivered"}
        if self.shipped_at is not None and self.status not in shipping_statuses:
            raise ValueError("shipped_at is only allowed for shipped or delivered orders")
        if self.status in shipping_statuses and self.shipped_at is None:
            raise ValueError("shipped_at is required for shipped or delivered orders")
        return self

    @computed_field
    @property
    def total(self) -> float:
        """Return the complete order total rounded to cents."""

        return round(sum(item.line_total for item in self.items), 2)


def build_user_profile(data: dict[str, Any]) -> UserProfile:
    """Create a validated ``UserProfile`` from a dictionary."""

    return UserProfile.model_validate(data)


def build_order(data: dict[str, Any]) -> Order:
    """Create a validated ``Order`` from a dictionary."""

    return Order.model_validate(data)


def parse_user_json(raw_json: str) -> UserProfile:
    """Create a validated ``UserProfile`` from a JSON string."""

    return UserProfile.model_validate_json(raw_json)


def serialize_model(model: BaseModel) -> dict[str, Any]:
    """Serialize a Pydantic model to a JSON-friendly dictionary."""

    return model.model_dump(mode="json")


def example_order_payload() -> dict[str, Any]:
    """Return a complete sample payload that passes all validations."""

    return {
        "order_id": "ORD-123456",
        "customer": {
            "id": 1,
            "name": "Chaitanya Dasadiya",
            "email": "chaitanya@example.com",
            "age": 28,
            "role": "customer",
            "address": {
                "street": "123 Python Road",
                "city": "Ahmedabad",
                "state": "GJ",
                "postal_code": "38001",
                "country": "in",
            },
            "tags": "Python, Pydantic, python, Validation",
        },
        "items": [
            {
                "product": {"sku": "PYD-2026", "name": "Pydantic Course", "price": 49.99},
                "quantity": 2,
            },
            {
                "product": {"sku": "API-1001", "name": "API Workbook", "price": 15.5},
                "quantity": 1,
            },
        ],
        "status": "paid",
    }


def run_demo() -> None:
    """Run a small command-line demonstration."""

    order = build_order(example_order_payload())
    print("Validated Pydantic order")
    print(f"Customer: {order.customer.name} <{order.customer.email}>")
    print(f"Tags: {', '.join(order.customer.tags) or 'none'}")
    print(f"Items: {len(order.items)}")
    print(f"Total: ${order.total:.2f}")


if __name__ == "__main__":
    run_demo()
