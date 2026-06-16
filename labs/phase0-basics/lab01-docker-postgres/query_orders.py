"""
Lab 0.1 — Python 连接 PostgreSQL 并做基本数据操作

运行方式：
  pip install psycopg2-binary
  python query_orders.py
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any


# --- 数据库连接配置 ---
DB_CONFIG: dict[str, str] = {
    "host": "localhost",
    "port": "5432",
    "dbname": "labdb",
    "user": "labuser",
    "password": "labpass",
}


def get_connection():
    """创建数据库连接"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def query_all_orders() -> list[dict[str, Any]]:
    """查询所有订单"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders ORDER BY order_date DESC")
            return cur.fetchall()  # type: ignore[return-value]


def query_customer_spending() -> list[dict[str, Any]]:
    """按客户统计消费总额，用你的 SQL 功底"""
    sql = """
        SELECT
            customer_name,
            COUNT(*) AS order_count,
            SUM(amount) AS total_spent,
            AVG(amount)::numeric(10,2) AS avg_order
        FROM orders
        GROUP BY customer_name
        ORDER BY total_spent DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()  # type: ignore[return-value]


def insert_order(name: str, product: str, amount: float) -> int:
    """插入新订单 —— 参数化查询防止 SQL 注入"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO orders (customer_name, product, amount, order_date) "
                "VALUES (%s, %s, %s, CURRENT_DATE) RETURNING id",
                (name, product, amount),
            )
            conn.commit()
            new_id: int = cur.fetchone()["id"]  # type: ignore[index]
            return new_id


def main() -> None:
    print("=" * 50)
    print("Lab 0.1: Docker PostgreSQL 数据操作验证")
    print("=" * 50)

    # 1. 查所有订单
    print("\n📋 所有订单：")
    for row in query_all_orders():
        print(f"  {row['id']:>2} | {row['customer_name']:<6} | {row['product']:<16} | "
              f"¥{row['amount']:>7.2f} | {row['status']}")

    # 2. 按客户统计
    print("\n💰 客户消费统计：")
    for row in query_customer_spending():
        print(f"  {row['customer_name']:<6} | {row['order_count']} 单 | "
              f"总额 ¥{row['total_spent']:>8.2f} | 均价 ¥{row['avg_order']}")

    # 3. 插入新订单
    new_id = insert_order("测试用户", "测试商品", 99.99)
    print(f"\n✅ 新增订单 ID={new_id}，用参数化查询安全写入")

    # 4. 验证 pgvector 扩展已启用
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector'")
            ext = cur.fetchone()
    if ext:
        print(f"✅ pgvector 扩展已启用 (版本 {ext['extversion']})")
    else:
        print("❌ pgvector 扩展未找到")
        return

    print("\n🎉 Lab 0.1 验证通过！Docker + PG + Python 环境就绪。")


if __name__ == "__main__":
    main()
