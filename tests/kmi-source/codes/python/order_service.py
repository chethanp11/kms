# Python domain sample: order service
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int = 1

    def extended_price(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)

@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[LineItem] = field(default_factory=list)
    discount: Decimal = Decimal("0.00")

    def subtotal(self) -> Decimal:
        return sum((item.extended_price() for item in self.items), Decimal("0.00"))

    def total(self) -> Decimal:
        return max(Decimal("0.00"), self.subtotal() - self.discount)

def normalize_sku(value: str) -> str:
    return value.strip().upper().replace(" ", "-")

def add_item(order: Order, sku: str, price: str, quantity: int) -> Order:
    order.items.append(LineItem(normalize_sku(sku), Decimal(price), quantity))
    return order

def validate_order(order: Order) -> list[str]:
    issues: list[str] = []
    if not order.order_id:
        issues.append("missing order id")
    if not order.customer_id:
        issues.append("missing customer id")
    if not order.items:
        issues.append("no items")
    if order.discount < Decimal("0.00"):
        issues.append("negative discount")
    return issues

def describe_order(order: Order) -> str:
    lines = [f"Order {order.order_id}", f"Customer: {order.customer_id}"]
    for item in order.items:
        lines.append(f"- {item.sku} x{item.quantity} @ {item.unit_price}")
    lines.append(f"Subtotal: {order.subtotal()}")
    lines.append(f"Discount: {order.discount}")
    lines.append(f"Total: {order.total()}")
    return "\n".join(lines)

def build_sample_order() -> Order:
    order = Order("ord-1001", "cust-42")
    add_item(order, "widget alpha", "12.50", 2)
    add_item(order, "service plan", "4.75", 1)
    order.discount = Decimal("1.25")
    return order
# python filler line 1
# python filler line 2
# python filler line 3
# python filler line 4
# python filler line 5
# python filler line 6
# python filler line 7
# python filler line 8
# python filler line 9
# python filler line 10
# python filler line 11
# python filler line 12
# python filler line 13
# python filler line 14
# python filler line 15
# python filler line 16
# python filler line 17
# python filler line 18
# python filler line 19
# python filler line 20
# python filler line 21
# python filler line 22
# python filler line 23
# python filler line 24
# python filler line 25
# python filler line 26
# python filler line 27
# python filler line 28
# python filler line 29
# python filler line 30
# python filler line 31
# python filler line 32
# python filler line 33
# python filler line 34
# python filler line 35
# python filler line 36
# python filler line 37
# python filler line 38
