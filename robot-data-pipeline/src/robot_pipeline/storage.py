"""存储模块 — 将处理后的数据持久化"""

import json
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from .models import SensorFrame, DatasetSummary


def save_to_parquet(frames: list[SensorFrame], output_dir: str | Path) -> Path:
    """保存为 Parquet 格式（机器人数据常用格式）"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建 Arrow Table
    table = pa.table({
        "frame_index": [f.frame_index for f in frames],
        "timestamp": [f.timestamp for f in frames],
        "image_width": [f.image_width for f in frames],
        "image_height": [f.image_height for f in frames],
        "joint_positions": [json.dumps(f.joint_positions) for f in frames],
        "gripper_position": [f.gripper_position for f in frames],
        "quality": [f.quality.value for f in frames],
        "quality_reasons": [json.dumps(f.quality_reasons) for f in frames],
    })

    path = output_dir / "robot_frames.parquet"
    pq.write_table(table, path)
    print(f"[storage] 已保存 {len(frames)} 帧到 {path}")

    return path


def save_summary(summary: DatasetSummary, output_dir: str | Path) -> Path:
    """保存数据集摘要报告"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / "dataset_summary.json"

    data = {
        "name": summary.name,
        "total_frames": summary.total_frames,
        "duration_seconds": summary.duration_seconds,
        "fps": summary.fps,
        "image_resolution": summary.image_resolution,
        "joint_count": summary.joint_count,
        "quality": {
            "pass_rate": summary.quality_pass_rate,
            "warn_rate": summary.quality_warn_rate,
            "fail_rate": summary.quality_fail_rate,
        },
        "processed_at": summary.processed_at,
    }

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[storage] 摘要已保存到 {path}")

    return path
