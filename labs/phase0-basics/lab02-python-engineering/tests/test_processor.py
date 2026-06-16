"""
测试 processor 模块 —— 纯函数最容易测试，不需要 mock 任何东西。
"""

from datetime import date

import pytest

from order_processor.models import CustomerStats, Order, OrderReport
from order_processor.processor import (
    generate_report,
    filter_completed,
    top_customers,
)


# --- 测试用的 fixture（公共测试数据）---

@pytest.fixture
def sample_orders() -> list[Order]:
    """3 条测试订单，覆盖正常场景"""
    return [
        Order(
            order_id=1,
            customer_name="张三",
            product="键盘",
            amount=399.00,
            order_date=date(2026, 6, 1),
            status="completed",
        ),
        Order(
            order_id=2,
            customer_name="李四",
            product="显示器",
            amount=1899.00,
            order_date=date(2026, 6, 2),
            status="completed",
        ),
        Order(
            order_id=3,
            customer_name="张三",
            product="鼠标",
            amount=49.00,
            order_date=date(2026, 6, 4),
            status="pending",
        ),
    ]


# --- 测试用例 ---

class TestGenerateReport:
    """测试 generate_report 函数"""

    def test_basic_report(self, sample_orders: list[Order]) -> None:
        report = generate_report(sample_orders)

        assert report.total_orders == 3
        assert report.total_revenue == 2347.00  # 399 + 1899 + 49
        assert report.customer_count == 2
        assert report.avg_revenue_per_order == 782.33

    def test_customer_ranking(self, sample_orders: list[Order]) -> None:
        report = generate_report(sample_orders)

        # 李四应该排第一（消费 1899 > 张三 448）
        assert report.customers[0].name == "李四"
        assert report.customers[0].total_spent == 1899.00
        assert report.customers[0].order_count == 1
        assert report.customers[0].avg_order == 1899.00

        assert report.customers[1].name == "张三"
        assert report.customers[1].total_spent == 448.00
        assert report.customers[1].order_count == 2
        assert report.customers[1].avg_order == 224.00

    def test_empty_orders(self) -> None:
        """边缘情况：空列表"""
        report = generate_report([])

        assert report.total_orders == 0
        assert report.total_revenue == 0.0
        assert report.customer_count == 0
        assert report.avg_revenue_per_order == 0.0

    def test_single_order(self) -> None:
        """边缘情况：只有一个订单"""
        orders = [
            Order(
                order_id=1,
                customer_name="测试",
                product="商品",
                amount=100.00,
                order_date=date(2026, 1, 1),
            )
        ]
        report = generate_report(orders)
        assert report.total_orders == 1
        assert report.total_revenue == 100.0
        assert report.customer_count == 1


class TestFilterCompleted:
    """测试 filter_completed 函数"""

    def test_filters_correctly(self, sample_orders: list[Order]) -> None:
        completed = filter_completed(sample_orders)
        assert len(completed) == 2
        assert all(o.status == "completed" for o in completed)

    def test_empty_when_none_completed(self) -> None:
        orders = [
            Order(
                order_id=1,
                customer_name="测试",
                product="x",
                amount=1.0,
                order_date=date(2026, 1, 1),
                status="pending",
            )
        ]
        assert filter_completed(orders) == []


class TestTopCustomers:
    """测试 top_customers 函数"""

    def test_returns_top_n(self) -> None:
        report = OrderReport(
            total_orders=3,
            total_revenue=300.0,
            customer_count=3,
            customers=[
                CustomerStats("A", 1, 1000.0),
                CustomerStats("B", 1, 500.0),
                CustomerStats("C", 1, 100.0),
            ],
        )
        top = top_customers(report, n=2)
        assert len(top) == 2
        assert top[0].name == "A"
        assert top[1].name == "B"


class TestOrderModel:
    """测试数据模型校验"""

    def test_negative_amount_raises(self) -> None:
        with pytest.raises(ValueError, match="金额不能为负"):
            Order(
                order_id=1,
                customer_name="测试",
                product="x",
                amount=-10.0,
                order_date=date(2026, 1, 1),
            )

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="客户名不能为空"):
            Order(
                order_id=1,
                customer_name="   ",
                product="x",
                amount=10.0,
                order_date=date(2026, 1, 1),
            )

    def test_default_status(self) -> None:
        order = Order(
            order_id=1,
            customer_name="测试",
            product="x",
            amount=10.0,
            order_date=date(2026, 1, 1),
            status="",  # 空字符串
        )
        assert order.status == "pending"
