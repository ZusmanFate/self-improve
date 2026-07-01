"""命令行入口 — robot-pipeline"""

import argparse
import sys
from pathlib import Path

from .loader import load_pusht_dataset
from .quality import check_dataset
from .storage import save_to_parquet, save_summary
from .reporter import generate_summary, print_summary, print_failures


def main():
    parser = argparse.ArgumentParser(
        description="🤖 机器人数据处理 Pipeline"
    )
    parser.add_argument(
        "--max-frames", type=int, default=500,
        help="最大处理帧数（默认 500）"
    )
    parser.add_argument(
        "--output-dir", type=str, default="./data",
        help="输出目录（默认 ./data）"
    )
    parser.add_argument(
        "--dataset", type=str, default="pusht",
        choices=["pusht"],
        help="数据集名称（默认 pusht）"
    )
    args = parser.parse_args()

    print("=" * 55)
    print("  🤖 机器人数据 Pipeline")
    print("  📦 数据集 → 解析 → 质检 → 存储 → 报告")
    print("=" * 55)

    # Step 1: 加载数据
    print("\n[Step 1/4] 加载数据...")
    if args.dataset == "pusht":
        frames = load_pusht_dataset(max_frames=args.max_frames)
    else:
        print(f"未知数据集: {args.dataset}")
        sys.exit(1)

    if not frames:
        print("❌ 没有加载到数据")
        sys.exit(1)

    # Step 2: 质量检查
    print(f"\n[Step 2/4] 质量检查...")
    frames = check_dataset(frames)

    # Step 3: 存储
    print(f"\n[Step 3/4] 存储结果...")
    output_dir = Path(args.output_dir)
    save_to_parquet(frames, output_dir)

    # Step 4: 生成报告
    print(f"\n[Step 4/4] 生成报告...")
    summary = generate_summary(frames, name=f"pusht_{args.max_frames}frames")
    save_summary(summary, output_dir)
    print_summary(summary)
    print_failures(frames)

    print(f"\n✅ Pipeline 完成！数据保存在 {output_dir.absolute()}")


if __name__ == "__main__":
    main()
