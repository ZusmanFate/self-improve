"""
数据读取层 —— 职责单一：从各种来源读取原始数据。
"""

import csv
from datetime import date
from pathlib import Path
from typing import Iterator

from .models import Order


class ReadError(Exception):
    """读取数据时的异常"""

    pass


def read_orders_csv(filepath: Path) -> list[Order]:
    """
    从 CSV 文件读取订单数据。

    - 明确的参数类型（Path，不是 str）
    - 返回类型明确（list[Order]，不是 list[dict]）
    - 异常用自定义类型，调用方可以精准捕获
    """
    if not filepath.exists():
        raise ReadError(f"文件不存在: {filepath}")

    orders: list[Order] = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # start=2 因为第 1 行是 header
            try:
                order = _parse_row(row, row_num)
                orders.append(order)
            except (ValueError, KeyError) as e:
                # 不中断整个批处理，记录错误继续处理
                print(f"[WARN] 第 {row_num} 行解析失败: {e}，跳过")

    if not orders:
        raise ReadError(f"文件中没有有效订单数据: {filepath}")

    return orders


def _parse_row(row: dict[str, str], row_num: int) -> Order:
    """解析单行数据，包含清洗逻辑"""
    # 用 get 防止 KeyError，设置默认值
    raw_amount = row.get("amount", "").strip()
    if not raw_amount:
        raise ValueError(f"金额为空")

    raw_date = row.get("order_date", "").strip()
    if not raw_date:
        raise ValueError(f"日期为空")

    raw_status = row.get("status", "").strip()
    if not raw_status:
        raw_status = "pending"

    return Order(
        order_id=int(row.get("id", 0)),
        customer_name=row.get("customer_name", "").strip(),
        product=row.get("product", "(未知商品)"),
        amount=float(raw_amount),
        order_date=date.fromisoformat(raw_date),
        status=raw_status,
    )
