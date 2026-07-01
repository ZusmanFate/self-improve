"""运行机器人数据 Pipeline — 本地模拟版"""
import sys
sys.path.insert(0, "src")

from robot_pipeline.simulator import generate_synthetic_frames
from robot_pipeline.quality import check_dataset
from robot_pipeline.storage import save_to_parquet, save_summary
from robot_pipeline.reporter import generate_summary, print_summary, print_failures
from pathlib import Path

print("=" * 55)
print("  🤖 机器人数据 Pipeline（本地模拟）")
print("  📦 生成 → 质检 → 存储 → 报告")
print("=" * 55)

# Step 1: 生成模拟机器人数据（7-DOF 机械臂，20Hz 采样）
print("\n[Step 1/4] 生成模拟传感器数据...")
frames = generate_synthetic_frames(num_frames=500)

# Step 2: 质量检查
print(f"\n[Step 2/4] 质量检查（关节异常检测、速度突变、时间戳连续性）...")
frames = check_dataset(frames)

# Step 3: 存储为 Parquet
print(f"\n[Step 3/4] 存储到 Parquet...")
out = Path("data")
save_to_parquet(frames, out)

# Step 4: 生成数据质量报告
print(f"\n[Step 4/4] 生成报告...")
summary = generate_summary(frames, name="7dof_robot_arm_simulated")
save_summary(summary, out)
print_summary(summary)
print_failures(frames)

print(f"\n✅ Pipeline 完成!")
print(f"   Parquet 文件: {(out / 'robot_frames.parquet').absolute()}")
print(f"   摘要报告:     {(out / 'dataset_summary.json').absolute()}")
