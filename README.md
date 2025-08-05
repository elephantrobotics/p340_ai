# AI_Answering 系统设计文档

## 项目名称：AI_Answering智能答题机器人系统
**文档版本：** 1.0  
**编写日期：** 2025-8-1  
**主要撰写人：** Python工程师-朱嘉豪  
**协助撰写人：** 无  

## 文档修订记录

| 版本 | 修订日期 | 修订内容 | 修订人 | 审核人 |
|------|----------|----------|--------|--------|
| 1.0 | 2025-8-1 | 初稿 | 朱嘉豪 |  |

## 1. 引言

### 1.1 目的
本文档描述AI_Answering智能问答机器人系统的概要设计方案，定义系统架构、核心模块、接口及技术选型，为详细设计和开发提供依据。该系统是一个集成了计算机视觉、人工智能和机器人控制的智能答题系统，能够自动识别试卷内容、生成答案并通过机械臂书写到答题区域。

### 1.2 项目背景
AI_Answering是一个基于人工智能的智能答题机器人系统，主要应用于教育领域的自动化答题场景。系统通过摄像头捕获试卷图像，利用OCR技术识别文字内容，调用大语言模型生成答案，最后通过机械臂将答案书写到指定的答题区域。该系统能够处理多种类型的题目，包括推理题、翻译题和算数题。

软件在整体系统中扮演核心控制角色，负责协调图像处理、AI推理和机器人控制三个主要模块，实现端到端的智能答题流程。

### 1.3 参考文档
- OpenCV官方文档: https://docs.opencv.org/
- PyMyCobot机械臂控制库文档: https://github.com/elephantrobotics/pymycobot
- OpenAI API文档: https://platform.openai.com/docs/overview
- 阿里云Qwen API文档: https://bailian.console.aliyun.com/&tab=model?tab=api&utm_content=se_1021866466#/api
- DeepSeek API文档: https://api-docs.deepseek.com/

### 1.4 术语表

| 术语 | 定义 |
|------|------|
| API | 应用程序编程接口 |
| OCR | 光学字符识别 |
| AI | 人工智能 |
| LLM | 大语言模型 |
| GUI | 图形用户界面 |
| JSON | JavaScript对象表示法 |
| YAML | YAML Ain't Markup Language |
| COM | 串行通信端口 |
| A4 | A4纸张尺寸标准 |

## 2. 系统描述

### 2.1 系统架构

AI_Answering采用模块化设计，主要包含以下核心组件：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   图像处理模块   │    │   AI推理模块     │    │  机器人控制模块  │
│  (OpenCV)       │    │  (Qwen/DeepSeek)│    │  (PyMyCobot)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    核心控制模块 (main.py)                        │
│                    协调各模块工作流程                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    配置管理模块 (config.py)                      │
│                    统一管理系统配置                              │
└─────────────────────────────────────────────────────────────────┘
```

**系统架构特点：**
- **模块化设计**：各功能模块独立开发，便于维护和扩展
- **配置驱动**：通过YAML配置文件统一管理系统参数
- **日志记录**：完整的日志系统记录运行状态和错误信息
- **异常处理**：各模块具备完善的错误处理机制

**项目文件结构：**
``` Plain Text
AI_Answering/
├── main.py                     # 主程序入口
├── src/                        # 源代码目录
│   ├── api/                    # API模块
│   │   ├── image_api.py        # 图像处理
│   │   ├── qwen_api.py         # Qwen AI服务
│   │   ├── deepseek_api.py     # DeepSeek AI服务
│   │   └── writing_api.py      # 机器人控制
│   └── utils/                  # 工具模块
│       ├── config.py           # 配置管理
│       ├── logger.py           # 日志系统
│       └── utils.py            # 通用工具
├── config/                     # 配置文件
├── data/                       # 数据目录
├── assets/                     # 资源文件
└── docs/                       # 文档目录
```

### 2.2 主要功能

1. **图像捕获模块**
   - 摄像头实时预览和图像捕获
   - 图像增强和预处理
   - 答题区域检测和定位
   - 坐标映射和书写任务生成

2. **OCR文字识别模块**
   - 基于Qwen-VL模型的图像文字识别
   - 支持中英文混合文本识别
   - 输出格式化的文本数据

3. **AI模块**
   - 支持多种题型：推理题、翻译题和算数题
   - 基于DeepSeek和Qwen大语言模型进行答题
   - 答案生成和格式化

4. **机器人书写控制**
   - 机械臂精确位置控制
   - 中英文字符书写支持
   - 字体路径规划和笔画生成
   - 实时状态监控

5. **系统管理**
   - 配置文件管理
   - 日志记录和监控
   - 数据存储和输出

## 3. 模块设计

### 3.1 图像捕获模块 (image_api.py)

**类结构设计：**
```python
class OpenCVImageClient:
    def __init__(self, camera_id: int)
    def capture_single_image(self, capture_path: str) -> None
    def capture_multi_images(self, capture_path: str) -> List
    def load_image_and_get_scale(self, image_path: str) -> Tuple
    def detect_single_black_box(self, img: np.ndarray, log_path: str) -> Tuple
    def generate_writing_task(self, img, box, answer, ...) -> None
```

**核心功能：**
- `capture_single_image()`: 单张图像捕获
- `detect_single_black_box()`: 黑色答题框检测
- `generate_writing_task()`: 生成书写任务

**辅助算法：**
1. **图像增强算法**：对比度调整、噪声去除
2. **答题框检测算法**：基于颜色阈值和轮廓检测
3. **坐标映射算法**：像素坐标到A4纸张坐标的转换

### 3.2 AI推理模块

#### 3.2.1 Qwen API模块 (qwen_api.py)

**类结构设计：**
```python
class QwenClient:
    def __init__(self, api_key, base_url, vl_model, text_model)
    def ocr_image(self, image_path: str, log_path: str) -> None
    def text_split(self, text: str) -> str
```

**核心功能：**
- OCR图像文字识别
- 文本分割和格式化

#### 3.2.2 DeepSeek API模块 (deepseek_api.py)

**类结构设计：**
```python
class DeepSeekClient:
    def __init__(self, api_key, base_url, model)
    def answer_reasoning_question(self, question_path: str, log_path: str) -> None
    def answer_translation_question(self, question_path: str, log_path: str) -> None
    def answer_math_question(self, question_path: str, log_path: str) -> None
```

**核心功能：**
- 推理题：逻辑推理和结论分析
- 翻译题：文言文翻译成白话文
- 算数题：复杂计算

### 3.3 机器人控制模块 (writing_api.py)

**类结构设计：**
```python
class RobotWritingClient:
    def __init__(self, com_port, baudrate, z_up, z_down, ...)
    def stand_by(self) -> None
    def go_center(self) -> None
    def write_chinese_char(self, ch: str, center_x: float, center_y: float, height: float) -> None
    def write_ascii_char(self, ch: str, center_x: float, center_y: float, height: float) -> None
    def write_text_line(self, text: str, start_x: float, start_y: float, height: float, spacing_ratio: float) -> None
    def load_writing_tasks(self, json_path) -> list
```

**辅助算法：**
1. **字体路径规划**：将字符转换为笔画路径
2. **坐标转换**：A4坐标到机器人坐标的转换
3. **运动控制**：机械臂的精确位置控制

### 3.4 配置管理模块 (config.py)

**类结构设计：**
```python
class ConfigManager:
    def __init__(self, config_path="config/config.yaml")
    def load_config(self) -> None
    def create_dict(self) -> None
    def get(self, key: str, default: Any = None) -> Any
    def get_api_config(self, service: str) -> Dict[str, str]
    def get_path_config(self) -> Dict[str, Any]
    def get_robot_config(self) -> Dict[str, Any]
```

**配置项分类：**
- API配置：各AI服务的密钥和端点
- 机器人配置：串口、速度、坐标等参数
- 路径配置：输入输出文件路径
- 日志配置：日志级别和格式

### 3.5 工具模块 (utils.py)

**核心功能：**
- 文件读写操作
- 图像编码和格式转换
- 文本处理和格式化
- 数据验证和清理

## 4. 接口设计

### 4.1 外部API接口

#### 4.1.1 Qwen API接口
- **OCR接口**：`ocr_image(image_path, log_path, prompt=None)`
- **文本分割接口**：`text_split(text)`
- **错误处理**：API调用失败时记录错误日志并退出

#### 4.1.2 DeepSeek API接口
- **推理题接口**：`answer_reasoning_question(question_path, log_path)`
- **翻译题接口**：`answer_translation_question(question_path, log_path)`
- **算数题接口**：`answer_math_question(question_path, log_path)`

### 4.2 机器人控制接口

#### 4.2.1 串口通信接口
- **连接参数**：COM端口、波特率
- **运动控制**：坐标设置、速度控制
- **状态查询**：位置、速度、状态信息

#### 4.2.2 书写控制接口
- **字符书写**：`write_chinese_char()`, `write_ascii_char()`
- **文本行书写**：`write_text_line()`
- **任务加载**：`load_writing_tasks()`

### 4.3 数据接口

#### 4.3.1 文件接口
- **图像文件**：JPEG/PNG格式
- **文本文件**：UTF-8编码的TXT文件
- **任务文件**：JSON格式的书写任务
- **日志文件**：系统运行日志(TXT文件)

#### 4.3.2 配置接口
- **YAML配置文件**：系统参数配置
- **字体文件**：pickle格式的中文字体数据

## 5. 数据设计

### 5.1 数据类型

#### 5.1.1 数据格式
- **图像文件**：JPEG/PNG格式
- **文本文件**：UTF-8编码的TXT文件
- **配置文件**：YAML格式
- **任务文件**：JSON格式
- **字体文件**：pickle格式

#### 5.1.2 数据流
```
┌────────────────────┐ 
│   印有题目的A4纸    │ 
└────────────────────┘ 
         │  经过图像捕获模块
         ▼             
┌──────────────────────────────┐ 
│   原始图片（raw_image.jpg）   │ 
└──────────────────────────────┘ 
         │  经过OCR模块
         ▼        
┌───────────────────────────────┐ 
│   题目文本（ocr_result.txt）   │ 
└───────────────────────────────┘ 
         │  经过AI推理模块
         ▼ 
┌───────────────────────────────┐ 
│   答案文本（answer.txt）       │ 
└───────────────────────────────┘ 
         │  经过机械臂书写模块
         ▼ 
┌───────────────────────────┐ 
│   机械臂在A4纸上书写       │ 
└───────────────────────────┘ 
```

### 5.2 存储方式

#### 5.2.1 本地存储
- **数据目录**：
  - `data/input/images/`：输入图像
  - `data/output/logs/`：输出日志和结果
  - `assets/`：字体和资源文件