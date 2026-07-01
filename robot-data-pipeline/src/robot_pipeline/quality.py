"""数据质量检查模块"""

import numpy as np
from .models import SensorFrame, QualityStatus


def check_frame(frame: SensorFrame, prev_frame: SensorFrame | None = None) -> SensorFrame:
    """对单帧执行所有质量检查"""
    reasons = []

    # 检查 1：分辨率异常
    if frame.image_width == 0 or frame.image_height == 0:
        reasons.append("缺少图像尺寸信息")

    # 检查 2：关节位置异常值（超出物理范围 ±2π）
    for j, pos in enumerate(frame.joint_positions):
        if abs(pos) > 2 * np.pi:
            reasons.append(f"关节 {j} 位置异常: {pos:.2f}")

    # 检查 3：关节速度突变（如果前一帧存在）
    if prev_frame and len(frame.joint_positions) == len(prev_frame.joint_positions):
        for j, (curr, prev) in enumerate(zip(frame.joint_positions, prev_frame.joint_positions)):
            velocity = abs(curr - prev)
            if velocity > 1.0:  # 关节速度超过 1 rad/帧视为异常
                reasons.append(f"关节 {j} 速度突变: {velocity:.3f}")

    # 检查 4：时间戳连续性
    if prev_frame and frame.timestamp - prev_frame.timestamp > 1.0:
        reasons.append(f"时间戳跳跃: {(frame.timestamp - prev_frame.timestamp):.2f}s")

    # 判断结果
    if len(reasons) == 0:
        frame.quality = QualityStatus.PASS
    elif any("异常" in r or "突变" in r for r in reasons):
        frame.quality = QualityStatus.FAIL
    else:
        frame.quality = QualityStatus.WARN

    frame.quality_reasons = reasons
    return frame


def check_dataset(frames: list[SensorFrame]) -> list[SensorFrame]:
    """对整个数据集执行质量检查"""
    print(f"[quality] 正在检查 {len(frames)} 帧...")

    checked = []
    for i, frame in enumerate(frames):
        prev = checked[-1] if checked else None
        checked.append(check_frame(frame, prev))

    pass_count = sum(1 for f in checked if f.quality == QualityStatus.PASS)
    warn_count = sum(1 for f in checked if f.quality == QualityStatus.WARN)
    fail_count = sum(1 for f in checked if f.quality == QualityStatus.FAIL)

    print(f"[quality] 完成: {pass_count} 通过, {warn_count} 警告, {fail_count} 失败")
    return checked
