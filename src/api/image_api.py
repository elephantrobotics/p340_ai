"""
qwen_api.py

OpenCV调用模块, 主要负责进行图像处理

Author: Zhu Jiahao
Date: 2025-07-17
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image
import base64
import os
from utils.logger import __logger__

cv_logger = __logger__.get_module_logger("OpenCV")

def read_image(path: str) -> np.ndarray:
    """ 读取图片, 返回OpenCV格式(BGR)"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"图片文件不存在: {path}")
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"无法读取图片: {path}")
    return img

def save_image(path: str, image: np.ndarray) -> None:
    """保存图片到指定路径"""
    cv2.imwrite(path, image)

def show_image(window_name: str, image: np.ndarray, wait_time: int = 0) -> None:
    """显示图片，wait_time=0时需手动关闭窗口"""
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time)

def close_all_windows() -> None:
    """关闭所有OpenCV窗口"""
    cv2.destroyAllWindows()

def capture_image() -> List:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cv_logger.error("无法打开摄像头")
        return []
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)