"""数据模型"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class QualityStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class SensorFrame:
    """单帧传感器数据"""
    timestamp: float
    frame_index: int
    # 图像数据 (numpy array 在内存中，这里存元信息)
    image_width: int = 0
    image_height: int = 0
    image_channels: int = 3
    # 关节状态
    joint_positions: list[float] = field(default_factory=list)
    joint_velocities: list[float] = field(default_factory=list)
    # 末端执行器
    gripper_position: float = 0.0
    # 质检结果
    quality: QualityStatus = QualityStatus.PASS
    quality_reasons: list[str] = field(default_factory=list)


@dataclass
class DatasetSummary:
    """数据集概览"""
    name: str = ""
    total_frames: int = 0
    duration_seconds: float = 0.0
    fps: float = 0.0
    image_resolution: str = ""
    joint_count: int = 0
    quality_pass_rate: float = 0.0
    quality_warn_rate: float = 0.0
    quality_fail_rate: float = 0.0
    processed_at: str = field(default_factory=lambda: datetime.now().isoformat())
