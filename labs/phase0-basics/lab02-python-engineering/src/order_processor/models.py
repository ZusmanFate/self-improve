"""
数据模型 —— 用 dataclass 定义类型安全的数据结构。
对比 v1 的 dict：类型检查、IDE 补全、字段明确。
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Order:
    """单条订单记录"""

    order_id: int
    customer_name: str
    product: str
    amount: float
    order_date: date
    status: str = "pending"

    def __post_init__(self) -> None:
        """数据校验 —— 在创建对象时自动运行"""
        if self.amount < 0:
            raise ValueError(f"订单金额不能为负: {self.amount}")
        if not self.customer_name.strip():
            raise ValueError("客户名不能为空")
        if not self.status:
            self.status = "pending"


@dataclass
class CustomerStats:
    """单个客户的统计"""

    name: str
    order_count: int = 0
    total_spent: float = 0.0

    @property
    def avg_order(self) -> float:
        if self.order_count == 0:
            return 0.0
        return round(self.total_spent / self.order_count, 2)


@dataclass
class OrderReport:
    """最终汇总报告"""

    total_orders: int
    total_revenue: float
    customer_count: int
    customers: list[CustomerStats] = field(default_factory=list)

    @property
    def avg_revenue_per_order(self) -> float:
        if self.total_orders == 0:
            return 0.0
        return round(self.total_revenue / self.total_orders, 2)
