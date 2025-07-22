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
from src.utils.logger import __logger__

__all__ = ['OpenCVImageClient']

cv_logger = __logger__.get_module_logger("OpenCV")

class OpenCVImageClient:
    """ OpenCV图像处理类
    """
    def __init__(self,
                camera_id: int,
                input_path: str):
        """
        初始化

        Args:
            camera_id (int): 摄像头索引
            input_path (str): 捕获照片存储目录
        """
        self.camera_id = camera_id
        self.input_path = input_path
        self.image_num = 0
        self.cap: Optional[cv2.VideoCapture] = None

    def capture_image(self) -> None:
        """ 打开摄像头并捕获图像
        """
        cv_logger.info("正在开启摄像头...")

        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            cv_logger.error("无法打开摄像头")
        
        # 设置分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

        cv_logger.info("摄像头已启动, 按空格拍照, ESC结束。")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                cv_logger.error("摄像头获取失败")
                break

            preview = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
            cv2.imshow("image capture", preview)
            key = cv2.waitKey(1)

            if key == 27:       # ESC
                cv_logger.info("用户推出图像捕获模式")
                break
            elif key == 32:     # SPACE
                self.image_num += 1
                cv_logger.info(f"拍摄了第{self.image_num}页")

                rotated = self.__rotate_image(frame, 90, True)
                enhanced = self.__enhance_image(rotated)
                final = self.__process_for_a4(enhanced)

                filename = os.path.join(self.input_path, f"{self.image_num}.jpg")
                cv2.imwrite(filename, final)
                cv_logger.info(f"图片已保存: {filename}")

        self.cap.release()
        cv2.destroyAllWindows()

                
    def __enhance_image(self, image: np.ndarray) -> np.ndarray:
        """ 图像增强: 增加对比度, 突出红色

        Args:
            image (np.ndarray): 输入图像

        Returns:
            np.ndarray: 旋转后的图像
        """
        enhanced_image = cv2.convertScaleAbs(image, alpha=1.3, beta=0)
        hsv = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        red_mask = cv2.inRange(h, 0, 10) + cv2.inRange(h, 170, 180)
        s_red = np.where(red_mask > 0, np.clip(s * 2.0, 0, 255).astype(np.uint8), s)
        non_red_mask = cv2.bitwise_not(red_mask)
        s_combined = np.where(non_red_mask > 0, np.clip(s * 0.6, 0, 255).astype(np.uint8), s_red)

        final_hsv = cv2.merge([h, s_combined, v])
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    def __rotate_image(self, image: np.ndarray, angle: int = 90, clockwise: bool = False) -> np.ndarray:
        """
        旋转图像

        Args:
            image (np.ndarray): 输入图像
            angle (int): 旋转角度，可选值为 90, 180, 270
            clockwise (bool): 是否顺时针旋转，默认 False 表示逆时针

        Returns:
            np.ndarray: 旋转后的图像

        Raises:
            ValueError: 如果角度无效
        """
        angle = angle % 360
        if angle not in (90, 180, 270):
            raise ValueError("仅支持旋转角度为 90, 180, 270")

        # OpenCV 的旋转标志映射
        rotate_map = {
            (90, False): cv2.ROTATE_90_COUNTERCLOCKWISE,
            (90, True): cv2.ROTATE_90_CLOCKWISE,
            (180, False): cv2.ROTATE_180,
            (180, True): cv2.ROTATE_180,
            (270, False): cv2.ROTATE_90_CLOCKWISE,
            (270, True): cv2.ROTATE_90_COUNTERCLOCKWISE,
        }

        rotate_code = rotate_map.get((angle, clockwise))
        return cv2.rotate(image, rotate_code)
    
    def __process_for_a4(self, image: np.ndarray) -> np.ndarray:
        """ 将图像裁剪成A4比例

        Args:
            image (np.ndarray): 输入图像

        Returns:
            np.ndarray: 旋转后的图像
        """
        TARGET_WIDTH = 2100
        TOP_CROP_MM = 62
        BOTTOM_CROP_MM = 10

        h, w, _ = image.shape
        ratio = TARGET_WIDTH / w
        new_height = int(h * ratio)
        resized = cv2.resize(image, (TARGET_WIDTH, new_height), interpolation=cv2.INTER_AREA)

        px_per_mm = TARGET_WIDTH / 210
        top = int(TOP_CROP_MM * px_per_mm)
        bottom = int(BOTTOM_CROP_MM * px_per_mm)

        if top >= new_height - bottom:
            cv_logger.info(f"警告：图像太小无法裁剪，返回原图。")
            return resized
        
        cropped = resized[top:new_height - bottom, :]
        cv_logger.info(f"图片已处理：缩放({TARGET_WIDTH}x{new_height})，裁剪上下({top}px, {bottom}px)")
        return cropped