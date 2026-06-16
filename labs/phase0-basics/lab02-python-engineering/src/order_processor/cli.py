"""
命令行入口 —— 把上面的模块组装成一个可执行的工具。

用法:
  python -m order_processor.cli orders.csv
  python -m order_processor.cli orders.csv --output report.json
  python -m order_processor.cli orders.csv --status completed
"""

import argparse
import sys
from pathlib import Path

from .reader import read_orders_csv, ReadError
from .processor import generate_report, filter_completed
from .reporter import to_console, to_json_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="订单数据处理工具 — 读取 CSV 并生成汇总报告",
    )
    parser.add_argument("input", type=Path, help="输入的 CSV 文件路径")
    parser.add_argument("--output", "-o", type=Path, default=None, help="JSON 输出路径")
    parser.add_argument("--status", "-s", type=str, default=None, help="按状态过滤")
    return parser


def main(argv: list[str] | None = None) -> int:
    """返回 0 表示成功，非 0 表示失败 —— 用于 CI/CD 流水线"""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        # 1. 读取
        orders = read_orders_csv(args.input)
        print(f"[OK] 读取到 {len(orders)} 条订单")

        # 2. 可选过滤
        if args.status:
            count_before = len(orders)
            orders = [o for o in orders if o.status == args.status]
            print(f"[FILTER] 按状态 '{args.status}' 过滤: {count_before} -> {len(orders)}")

        # 3. 处理
        report = generate_report(orders)

        # 4. 输出
        print(to_console(report))

        if args.output:
            to_json_file(report, args.output)
            print(f"[SAVED] JSON 报告已保存: {args.output}")

        return 0

    except ReadError as e:
        print(f"[ERROR] 读取失败: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
