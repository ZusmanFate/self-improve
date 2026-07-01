# 🤖 机器人数据工程学习路线

> 起点：数据工程师（SQL/Spark/Python/Docker）
> 目标：机器人数据管线工程师
> 周期：8-12 周（业余每周 10-15 小时）
> 原则：代码必须自己写，每阶段出成果再往下走

---

## 核心理念

具身智能最缺的不是算法工程师，而是懂数据工程的人：
- 机器人数据占项目 60-80% 时间
- 传感器数据（图像 + 点云 + 关节状态）需要采集、清洗、质检、入库
- 这些和 ETL 是同一个思维模型，只是数据格式不同

---

## 学习资源（全部免费）

| 资源 | 链接 | 学什么 |
|------|------|--------|
| LeRobot 教程 | https://huggingface.co/spaces/lerobot/robot-learning-tutorial | 机器人数据集格式、训练流程 |
| LeRobot 文档 | https://huggingface.co/docs/lerobot | 数据采集、训练、部署全流程 |
| ROS2 入门课程 | https://github.com/henki-robotics/robotics_essentials_ros2 | ROS2 基础、Docker 模拟、传感器 |
| ROS2 Data Pipeline | https://roboticsbackend.com/build-a-ros2-data-pipeline-with-ros2-topics/ | 传感器数据流管道 |
| NVIDIA Isaac Sim | https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-sim/latest/building-your-first-robot-in-isaac-sim/index.html | 仿真环境搭建、传感器数据流 |
| Robot Vision (ROS2) | https://github.com/ARTenshi/robovision_ros2 | ROS2 + OpenCV 图像处理 |

---

## 阶段一：搞懂机器人数据（2 周）

### 目标
能跟别人讲清楚「一个机器人数据集里面有什么、怎么组织的」

### 学习内容

1. 打开 [LeRobot 教程](https://huggingface.co/spaces/lerobot/robot-learning-tutorial)，通读 Quick Start
2. 阅读 LeRobot 文档中「Dataset Structure」部分，理解：
   - `meta/info.json` — 数据集元信息（fps、特征列表、形状）
   - `data/*.parquet` — 帧级别的表格数据（关节状态、动作指令）
   - `videos/*.mp4` — 摄像头视频流
   - episode 的概念：一次完整的任务执行
3. 了解常见机器人数据集：`aloha_mobile_cabinet`、`pusht`、`libero`

### 🔬 项目 1：机器人数据集探查器

> **你自己写一个 Python 脚本**，加载 LeRobot 的 `aloha_mobile_cabinet` 数据集，输出：
>
> - 总共有多少 episode？每 episode 多少帧？
> - 数据包含哪些传感器？（图像、关节状态、动作指令）
> - 每帧数据多大？整个数据集多大？
> - 画一张图：某个关节在 3 个 episode 里的轨迹曲线
>
> 输出格式：终端打印 + 一张 PNG 图
>
> 技术点：`datasets` 库、`matplotlib`、LeRobot API

### 验收标准
- [ ] 能跑通脚本，输出完整的数据集报告
- [ ] 能把 LeRobot 的数据格式口头解释给一个不懂机器人的人听

---

## 阶段二：学会机器人怎么「说话」（2-3 周）

### 目标
能用 ROS2 让两个程序「对话」传递传感器数据，并且能检测异常

### 学习内容

1. 跟着 [ROS2 Essentials 课程](https://github.com/henki-robotics/robotics_essentials_ros2) 做：
   - Exercise 0：Docker 环境搭建
   - Exercise 1：ROS2 基础概念（Topic、Node、Publisher、Subscriber）
   - Exercise 2：SLAM 和导航演示
   - Exercise 3：创建自己的 ROS2 Package
2. 学习 `ros2 topic` 命令行工具：`list`、`echo`、`hz`、`pub`
3. 学习 `rqt_plot` 可视化 topic 数据

### 🔬 项目 2：ROS2 传感器数据 Pipe

> **你自己写两个 ROS2 节点**（都用 Python）：
>
> - **节点 A**：发布模拟的关节角度数据（正弦波，7 个关节，10Hz）
>   - Topic：`/joint_states_sim`
>   - 消息类型：`sensor_msgs/JointState`
> - **节点 B**：订阅节点 A 的数据，执行异常检测：
>   - 关节位置超出 ±π 范围 → 标记为异常
>   - 相邻帧关节速度 > 1.0 rad/s → 标记为突变
>   - 把异常帧的（时间戳、关节名、异常值、原因）写入 CSV 文件
>
> 用 `ros2 topic echo /joint_states_sim` 验证数据流
> 用 `rqt_plot` 可视化关节轨迹

### 验收标准
- [ ] 两个 ROS2 节点能正常通信
- [ ] 异常检测能正确识别（可手动注入异常值验证）
- [ ] CSV 文件记录了所有异常帧

---

## 阶段三：仿真环境搭数据 Pipeline（3-4 周）

> ⚠️ 需要 NVIDIA 显卡。没有的话跳过，把阶段一 + 二的深度做够。

### 目标
能从零搭一个仿真数据生成 Pipeline，产出干净的机器人训练数据

### 学习内容

1. 跟着 [NVIDIA Isaac Sim 入门教程](https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-sim/latest/building-your-first-robot-in-isaac-sim/index.html)：
   - 熟悉 Isaac Sim 界面
   - 构建简单机器人模型
   - 配置物理属性
   - 添加传感器（RGB 相机、LiDAR）
   - 数据流到 ROS2
2. 学习 Isaac Sim Python API：加载机器人、控制关节、读取传感器

### 🔬 项目 3：仿真数据自动采集系统

> **你自己写 Python 脚本**：
>
> 1. 在 Isaac Sim 里加载一个机械臂（Franka 或 UR5）
> 2. 控制机械臂做随机运动（关节空间随机采样）
> 3. 每次运动自动采集：
>    - RGB 图像（保存为 PNG）
>    - 深度图（保存为 NPY）
>    - 关节状态（保存到 Parquet）
> 4. 质检过滤：
>    - 亮度异常的图丢弃（灰度均值 < 20 或 > 235）
>    - 关节速度过大的帧丢弃
> 5. 目标：自动生成 1000 帧有效训练数据
>
> 技术点：Isaac Sim Python API、OpenCV、pyarrow、numpy

### 验收标准
- [ ] 脚本能自动运行，无需人工干预
- [ ] 产出 1000 帧有效数据
- [ ] 质检过滤规则生效，异常数据被丢弃

---

## 可选阶段四：集成项目

把阶段一 + 二 + 三的能力串起来，做成一个完整的端到端系统：

> Isaac Sim 生成数据 → ROS2 传输 → Python 质检 → Parquet 存储 → 质量报告
>
> 全部 Docker 化，一个 `docker-compose up` 全跑起来

---

## 每个阶段应该产出的 GitHub 仓库

| 仓库 | 说明 |
|------|------|
| `robot-dataset-explorer` | 阶段一项目：数据集探查器 |
| `ros2-sensor-pipe` | 阶段二项目：ROS2 数据 Pipe |
| `sim-data-collector` | 阶段三项目：仿真数据采集 |
| `robot-data-pipeline` | 阶段四（可选）：集成 Pipeline |

---

## 提醒

1. **不要同时学所有东西。** 先做阶段一，做完再做二
2. **代码必须自己写。** 可以看文档、看示例、用 AI 解释概念，但敲代码的手指要是你自己的
3. **ROS2 用 Docker 装。** 拉 `osrf/ros:humble-desktop` 镜像，别在 Windows 裸装
4. **每个项目做完推到 GitHub。** 面试时直接甩链接
5. **遇到问题先搜文档，再搜 GitHub Issues，最后再问 AI。** 自己找到答案的才会记住
