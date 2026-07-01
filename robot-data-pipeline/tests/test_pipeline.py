"""测试"""

import sys
sys.path.insert(0, "src")

from robot_pipeline.models import SensorFrame, QualityStatus
from robot_pipeline.quality import check_frame
from robot_pipeline.reporter import generate_summary


def test_check_frame_pass():
    """正常帧应该通过"""
    frame = SensorFrame(
        timestamp=1.0, frame_index=0,
        image_width=640, image_height=480,
        joint_positions=[0.5, -0.3, 1.2],
    )
    result = check_frame(frame)
    assert result.quality == QualityStatus.PASS


def test_check_frame_anomaly():
    """异常关节值应该失败"""
    frame = SensorFrame(
        timestamp=1.0, frame_index=0,
        image_width=640, image_height=480,
        joint_positions=[10.0, -0.3, 1.2],  # 关节 0 超出范围
    )
    result = check_frame(frame)
    assert result.quality == QualityStatus.FAIL


def test_check_frame_velocity():
    """速度突变应该失败"""
    prev = SensorFrame(
        timestamp=0.05, frame_index=0,
        joint_positions=[0.1, 0.0],
    )
    curr = SensorFrame(
        timestamp=0.10, frame_index=1,
        joint_positions=[5.0, 0.0],  # 速度突变
    )
    result = check_frame(curr, prev)
    assert result.quality == QualityStatus.FAIL


def test_generate_summary():
    """测试摘要生成"""
    frames = [
        SensorFrame(timestamp=0.0, frame_index=0, image_width=640, image_height=480,
                     joint_positions=[0.1], quality=QualityStatus.PASS),
        SensorFrame(timestamp=0.05, frame_index=1, image_width=640, image_height=480,
                     joint_positions=[0.2], quality=QualityStatus.PASS),
    ]
    summary = generate_summary(frames, name="test")
    assert summary.total_frames == 2
    assert summary.quality_pass_rate == 100.0
    assert summary.fps == 40.0  # 2 frames / 0.05s


if __name__ == "__main__":
    test_check_frame_pass()
    test_check_frame_anomaly()
    test_check_frame_velocity()
    test_generate_summary()
    print("✅ 所有测试通过!")
