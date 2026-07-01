# 🤖 Robot Data Pipeline

**机器人数据处理 Pipeline — 从传感器原始数据到模型就绪数据**

一个完整的数据工程 Pipeline，演示如何用你已经会的数据工程技能处理机器人传感器数据。

## 为什么做这个项目

具身智能（Embodied AI）最缺的不是算法工程师，而是**懂数据工程的人**：
- 机器人数据占项目 60-80% 时间
- 传感器数据（图像 + 点云 + 关节状态）需要采集、清洗、质检、入库
- 这些和 SQL/Spark ETL 是同一个思维模型，只是数据格式不同

## Pipeline 流程

```
传感器数据 → 解析 → 质量检查 → Parquet 存储 → 报告生成
   (模拟)     ↓        ↓           ↓            ↓
           20Hz    异常检测    列式存储      JSON 摘要
           7-DOF   速度突变    高效压缩      问题帧列表
                   时间戳
```

## 快速开始

```bash
# 安装依赖
pip install pyarrow

# 运行 Pipeline
python run.py
```

输出：
```
🤖 机器人数据集报告: 7dof_robot_arm_simulated
  总帧数:       500
  时长:         25s
  帧率:         20.0 fps
  关节数量:     7
  质检通过率:   98.8%
  质检失败率:   1.2%
```

## 项目结构

```
robot-data-pipeline/
├── run.py                    # 快速运行入口
├── pyproject.toml            # 项目配置
├── src/robot_pipeline/
│   ├── models.py             # 数据模型（SensorFrame, DatasetSummary）
│   ├── simulator.py          # 模拟机器人数据生成器
│   ├── loader.py             # 真实数据集加载（HuggingFace LeRobot）
│   ├── quality.py            # 质量检查（异常值、速度突变、时间戳）
│   ├── storage.py            # Parquet 存储
│   └── reporter.py           # 报告生成（终端 + JSON）
├── tests/
│   └── test_pipeline.py      # 单元测试
└── data/                     # 输出目录（自动生成）
    ├── robot_frames.parquet  # 处理后的数据
    └── dataset_summary.json  # 质量报告
```

## 技能映射：你的数据工程经验 → 机器人数据工程

| 你会的 | Pipeline 里的对应 |
|--------|------------------|
| SQL 查询优化 | Parquet 列式存储 + 按帧索引查询 |
| ETL Pipeline (Spark/Airflow) | 加载 → 质检 → 存储流水线 |
| 数据质量监控 | 关节异常检测、速度突变检测 |
| 数据仓库建模 | SensorFrame 数据模型 |
| 报表生成 | DatasetSummary + JSON 报告 |

## 下一步可以扩展

- [ ] 接入真实 LeRobot 数据集
- [ ] 支持 ROS bag 文件解析
- [ ] 用 Prefect 调度定时任务
- [ ] 加 Great Expectations 数据质量断言
- [ ] Docker 化部署
- [ ] 接 MinIO/S3 存储海量传感器数据
