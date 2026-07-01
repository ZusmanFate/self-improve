"""报告生成模块"""

from .models import SensorFrame, DatasetSummary, QualityStatus


def generate_summary(frames: list[SensorFrame], name: str = "robot_dataset") -> DatasetSummary:
    """从帧列表生成数据集摘要"""
    if not frames:
        return DatasetSummary(name=name)

    # 基本统计
    total = len(frames)
    duration = frames[-1].timestamp - frames[0].timestamp if total > 1 else 0
    fps = total / duration if duration > 0 else 0

    # 分辨率
    w = frames[0].image_width
    h = frames[0].image_height
    resolution = f"{w}x{h}" if w and h else "未知"

    # 关节数
    joints = len(frames[0].joint_positions) if frames[0].joint_positions else 0

    # 质量统计
    pass_count = sum(1 for f in frames if f.quality == QualityStatus.PASS)
    warn_count = sum(1 for f in frames if f.quality == QualityStatus.WARN)
    fail_count = sum(1 for f in frames if f.quality == QualityStatus.FAIL)

    return DatasetSummary(
        name=name,
        total_frames=total,
        duration_seconds=round(duration, 2),
        fps=round(fps, 1),
        image_resolution=resolution,
        joint_count=joints,
        quality_pass_rate=round(pass_count / total * 100, 1),
        quality_warn_rate=round(warn_count / total * 100, 1),
        quality_fail_rate=round(fail_count / total * 100, 1),
    )


def print_summary(summary: DatasetSummary):
    """打印漂亮的摘要报告"""
    print()
    print("=" * 55)
    print(f"  🤖 机器人数据集报告: {summary.name}")
    print("=" * 55)
    print(f"  总帧数:       {summary.total_frames}")
    print(f"  时长:         {summary.duration_seconds}s")
    print(f"  帧率:         {summary.fps} fps")
    print(f"  图像分辨率:   {summary.image_resolution}")
    print(f"  关节数量:     {summary.joint_count}")
    print(f"  ───────────────────────────────────────")
    print(f"  质检通过率:   {summary.quality_pass_rate}%")
    print(f"  质检警告率:   {summary.quality_warn_rate}%")
    print(f"  质检失败率:   {summary.quality_fail_rate}%")
    print(f"  处理时间:     {summary.processed_at}")
    print("=" * 55)
    print()


def print_failures(frames: list[SensorFrame]):
    """打印所有质检失败的帧"""
    failed = [f for f in frames if f.quality == QualityStatus.FAIL]
    if not failed:
        print("[reporter] ✅ 所有帧质检通过!")
        return

    print(f"[reporter] ⚠️  发现 {len(failed)} 帧存在问题:")
    for f in failed[:10]:  # 最多显示 10 个
        print(f"  帧 #{f.frame_index} (t={f.timestamp:.2f}):")
        for reason in f.quality_reasons:
            print(f"    - {reason}")
    if len(failed) > 10:
        print(f"  ... 还有 {len(failed) - 10} 帧")
