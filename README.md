# P340_AI Intelligent Answering Robot System

## Overview

P340_AI is an intelligent answering robot system that combines computer vision, AI, and robotic control. It can automatically recognize test paper content, generate answers using large language models, and write the answers onto the answer area using a robotic arm - ultraArm P340.

## Features
- Image capture and processing
- OCR text recognition
- AI-powered answer generation
- precise robotic arm writing control

## Requirements
### Hardware
- 4K camera with stand
- UltraArm P340 robotic arm with pen holder module
- Soft board and pins for paper fixation

### Software
- Python 3.8+
- Dependencies:
    ``` Plain Text
    Hershey_Fonts==2.1.0
    numpy==2.3.2
    openai==1.98.0
    opencv_python==4.11.0.86
    Pillow==11.3.0
    pymycobot==3.9.9
    PyYAML==6.0.2
    ```

## Installation
1. Clone the repository:
   ``` bash
   git clone https://github.com/elephantrobotics/p340_ai.git
   cd p340_ai
   ```
2. Install dependencies:
   ``` bash
   pip install -r requirements.txt
   ```
3. Configure the system:
   - Edit `config/config.yaml` with your API keys and hardware settings.
   - Place Chinese font files in `assets/` directory.

## Quick Start
1. Set up hardware:
   - Mount the camera above the writing area.
   - Position the robotic arm at the bottom center.
   - Secure answer paper on the soft board.
2. Run the system:
    ``` bash
    python main.py
    ```
3. Follow on-screen instructions:
   - Position the test paper when prompted.
   - Press spacebar to capture image.
   - The system will automatically process and write answers.

## Configuration
Key configuration options in `config/config.yaml`:
- **API keys for DeepSeek and Qwen services**
- Camera ID
- Robotic arm parameters (**COM port**, speed, **writing height**)
- File paths for input/output

## [中文文档](README_zh.md)