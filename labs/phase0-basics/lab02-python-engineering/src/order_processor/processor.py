"""
业务逻辑层 —— 纯函数，不依赖文件 I/O。
容易测试：输入确定，输出确定。
"""

from collections import defaultdict

from .models import CustomerStats, Order, OrderReport


def generate_report(orders: list[Order]) -> OrderReport:
    """
    从订单列表生成汇总报告。

    纯函数：给定同样的输入，永远返回同样的输出。
    没有副作用（不读文件、不写文件、不 print）。
    """
    if not orders:
        return OrderReport(total_orders=0, total_revenue=0.0, customer_count=0)

    total_revenue = sum(o.amount for o in orders)

    # 按客户聚合
    customer_map: dict[str, CustomerStats] = {}
    for order in orders:
        name = order.customer_name
        if name not in customer_map:
            customer_map[name] = CustomerStats(name=name)
        customer_map[name].order_count += 1
        customer_map[name].total_spent += order.amount

    # 按消费总额降序排列
    sorted_customers = sorted(
        customer_map.values(), key=lambda c: c.total_spent, reverse=True
    )

    return OrderReport(
        total_orders=len(orders),
        total_revenue=round(total_revenue, 2),
        customer_count=len(customer_map),
        customers=sorted_customers,
    )


def filter_completed(orders: list[Order]) -> list[Order]:
    """过滤出已完成订单"""
    return [o for o in orders if o.status == "completed"]


def top_customers(report: OrderReport, n: int = 3) -> list[CustomerStats]:
    """取 Top-N 客户"""
    return report.customers[:n]
