"""
V1 — 很多人最初写的「能用就行」脚本

场景：从 CSV 读取订单数据，做清洗和聚合，输出汇总报告。
这是你面试时要避免的代码风格。找出它的问题，然后看 v2 怎么改。
"""

import csv
import json

# 全局变量——散落各处
orders = []
total_revenue = 0
customer_stats = {}

# 读取 CSV
with open("orders.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 数据清洗直接写在循环里
        row["amount"] = float(row["amount"]) if row["amount"] else 0.0
        row["order_date"] = row["order_date"].strip()
        if row["amount"] > 0:  # 过滤逻辑混在读取里
            orders.append(row)

# 计算汇总——又一个循环
for o in orders:
    total_revenue += o["amount"]
    name = o["customer_name"]
    if name not in customer_stats:
        customer_stats[name] = {"count": 0, "total": 0.0}
    customer_stats[name]["count"] += 1
    customer_stats[name]["total"] += o["amount"]

# 输出——直接 print，没有返回
print(f"总订单数: {len(orders)}")
print(f"总营收: {total_revenue:.2f}")
print(f"客户数: {len(customer_stats)}")
for name, stats in sorted(customer_stats.items()):
    print(f"  {name}: {stats['count']} 单, ¥{stats['total']:.2f}")

# 保存 JSON — 硬编码路径
with open("report.json", "w") as f:
    json.dump({"total_orders": len(orders), "total_revenue": total_revenue}, f)

print("报告已保存到 report.json")
