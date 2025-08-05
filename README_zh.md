# P340_AI 智能答题机器人系统

## 项目概述

P340_AI是一个结合计算机视觉、人工智能和机器人控制的智能答题系统。能够自动识别试卷内容，通过大语言模型生成答案，并使用ultraArm P340机械臂将答案书写到答题区域。

## 功能特性
- 图像捕获与处理
- OCR文字识别
- AI智能答题
- 高精度机械臂书写控制

## 环境要求
### 硬件需求
- 4K摄像头及支架
- UltraArm P340机械臂 (带笔夹模组)
- 软木板和图钉 (用于固定纸张)

### 软件需求
- Python 3.8+
- 依赖:
    ``` Plain Text
    Hershey_Fonts==2.1.0
    numpy==2.3.2
    openai==1.98.0
    opencv_python==4.11.0.86
    Pillow==11.3.0
    pymycobot==3.9.9
    PyYAML==6.0.2
    ```

## 安装指南
1. 克隆仓库:
   ``` bash
   git clone https://github.com/elephantrobotics/p340_ai.git
   cd p340_ai
   ```
2. 安装依赖:
   ``` bash
   pip install -r requirements.txt
   ```
3. 系统配置:
   - 修改 `config/config.yaml` 中的API Key和硬件参数
   - 将中文字体放入 `assets/` 目录

## 运行流程
1. 硬件准备:
   - 将摄像头架设在书写区域正上方
   - 将机械臂置于底部中央位置
   - 用图钉将答题纸固定在软木板上
  
2. 运行程序:
    ``` bash
    python main.py
    ```
3. 按照屏幕提示操作:
   - 根据提示放置试卷
   - 按空格键捕获图像
   - 系统将自动处理并书写答案

## 配置说明
关键配置项（位于 `config/config.yaml`）:
- **DeepSeek和Qwen服务的API密钥**
- 摄像头ID
- 机械臂参数 (**串口**, 速度, **提笔/落笔高度**)
- 输入输出文件路径

## [English Documentation](README.md)