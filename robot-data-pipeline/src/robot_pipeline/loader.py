"""数据加载模块 — 支持多种机器人数据集格式"""

import time
import numpy as np
from pathlib import Path
from typing import Iterator, Optional
from datasets import load_dataset

from .models import SensorFrame


def load_pusht_dataset(max_frames: int = 500) -> list[SensorFrame]:
    """加载 LeRobot pusht 数据集（真实机器人推送任务）

    这是最常用的机器人学习基准数据集之一。
    数据格式：每帧包含摄像头图像 + 关节状态 + 动作指令
    """
    print("[loader] 正在加载 pusht 数据集...")
    dataset = load_dataset("lerobot/pusht", split="train", streaming=True)

    frames = []
    start_time = time.time()
    dataset_start_ts = None

    for i, episode in enumerate(dataset):
        if i >= max_frames:
            break

        # 提取图像信息
        image = np.array(episode["observation.image"])
        if dataset_start_ts is None:
            dataset_start_ts = episode.get("timestamp", time.time())

        h, w = image.shape[:2]
        c = image.shape[2] if len(image.shape) > 2 else 1

        # 提取关节状态（如果有）
        joints = episode.get("observation.state", [])
        joint_list = joints.tolist() if hasattr(joints, "tolist") else list(joints)

        frame = SensorFrame(
            timestamp=episode.get("timestamp", i * 0.05),
            frame_index=i,
            image_width=w,
            image_height=h,
            image_channels=c,
            joint_positions=joint_list,
            gripper_position=joint_list[-1] if joint_list else 0.0,
        )
        frames.append(frame)

    elapsed = time.time() - start_time
    print(f"[loader] 加载完成: {len(frames)} 帧, 耗时 {elapsed:.1f}s")

    return frames


def load_local_images(image_dir: str | Path) -> list[SensorFrame]:
    """从本地图片目录加载（模拟传感器采集）"""
    image_dir = Path(image_dir)
    image_files = sorted(image_dir.glob("*.png")) + sorted(image_dir.glob("*.jpg"))

    frames = []
    for i, img_path in enumerate(image_files):
        frame = SensorFrame(
            timestamp=img_path.stat().st_mtime,
            frame_index=i,
            # 模拟传感器数据
            joint_positions=[np.sin(i * 0.1), np.cos(i * 0.1)],
            gripper_position=float(np.sin(i * 0.05)),
        )
        frames.append(frame)

    return frames
