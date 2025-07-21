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
from src.utils.config import __config__
from utils.logger import __logger__

__all__ = ['OpenCVImageClient']

cv_logger = __logger__.get_module_logger("OpenCV")

class OpenCVImageClient:
    """ OpenCV图像处理类
    """
    def __init__(self, camera_id: int):
        """
        初始化

        Args:
            camera_id (int): 摄像头索引
        """
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
