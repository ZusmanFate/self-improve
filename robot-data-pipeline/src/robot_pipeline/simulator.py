"""模拟机器人数据生成器 — 不依赖外部数据集"""

import numpy as np

def generate_synthetic_frames(num_frames: int = 500) -> list:
    """生成模拟的机器人传感器数据"""
    from robot_pipeline.models import SensorFrame

    frames = []
    t = 0.0
    dt = 0.05  # 20Hz 传感器采样

    # 模拟 7 自由度机械臂
    joint_count = 7

    for i in range(num_frames):
        # 模拟关节位置：做正弦运动
        joints = [
            np.sin(t * 2.0 + j * 0.5) * 0.8
            for j in range(joint_count)
        ]

        # 偶尔插入异常数据（模拟真实传感器故障）
        if i > 0 and i % 50 == 0:
            joints[0] = np.nan if np.random.random() > 0.5 else 100.0

        frame = SensorFrame(
            timestamp=round(t, 3),
            frame_index=i,
            image_width=640,
            image_height=480,
            image_channels=3,
            joint_positions=joints,
            gripper_position=joints[-1],
        )
        frames.append(frame)
        t += dt

    print(f"[loader] 生成 {len(frames)} 帧模拟机器人数据 (20Hz, {num_frames * dt:.1f}s)")
    return frames
