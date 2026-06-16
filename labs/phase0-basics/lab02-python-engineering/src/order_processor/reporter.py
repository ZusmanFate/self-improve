"""
输出层 —— 格式化报告为各种输出格式。
"""

import json
from pathlib import Path

from .models import OrderReport


def to_console(report: OrderReport) -> str:
    """生成控制台输出文本"""
    lines = [
        "=" * 50,
        "订单汇总报告",
        "=" * 50,
        f"总订单数:   {report.total_orders}",
        f"总营收:     ¥{report.total_revenue:,.2f}",
        f"客户数:     {report.customer_count}",
        f"平均订单额: ¥{report.avg_revenue_per_order:,.2f}",
        "",
        "客户排名（按消费额）:",
    ]
    for i, c in enumerate(report.customers, 1):
        lines.append(
            f"  {i}. {c.name:<8}  {c.order_count} 单  "
            f"¥{c.total_spent:>10,.2f}  (均价 ¥{c.avg_order:,.2f})"
        )
    return "\n".join(lines)


def to_json_file(report: OrderReport, filepath: Path) -> None:
    """保存为 JSON 文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "total_orders": report.total_orders,
        "total_revenue": report.total_revenue,
        "customer_count": report.customer_count,
        "avg_revenue_per_order": report.avg_revenue_per_order,
        "top_customers": [
            {
                "name": c.name,
                "order_count": c.order_count,
                "total_spent": c.total_spent,
            }
            for c in report.customers[:5]
        ],
    }
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
