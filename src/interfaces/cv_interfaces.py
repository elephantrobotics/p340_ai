"""
cv_interfaces.py

该模块定义了opencv相关的接口

Author: Zhu Jiahao
Date: 2025-07-15
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image
import base64
import os

def read_image(path: str) -> np.ndarray:
    """ 读取图像

    Args:
        path str: 图像路径

    Returns:
        BGR数据
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"图片不存在: {path}")
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"无法读取图片: {path}")
    return img

def save_image(path: str, image: np.ndarray) -> None:
    """ 保存图片

    Args:
        path str: 保存路径
        image np.ndarray: BGR数据
    """
    cv2.imwrite(path, image)

def show_image(window_name: str, image: np.ndarray, wait_time: int = 0) -> None:
    """ 显示图像, 当wait_time == 0时需要手动结束

    Args:
        window_name str: 窗口名称
        image np.ndarray: 图像
        wait_time int: 等待时间, 若为0则代表需要手动结束
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time)

def close_all_windows() -> None:
    """ 关闭所有窗口
    """
    cv2.destroyAllWindows()

def enhance_image(image: np.ndarray, contrast_alpha=1.3, red_saturation=2.0, non_red_saturation=0.6) -> np.ndarray:
    """ 增强图像：增加对比度，并提升颜色饱和度, 尤其是红色

    Args:
        image: 图像
    """
    # 1. 增加对比度 (alpha > 1)，beta是亮度，保持不变
    enhanced = cv2.convertScaleAbs(image, alpha=contrast_alpha, beta=0)

    # 2. 转换到HSV色彩空间以调整饱和度
    hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 3. 调整红色饱和度
    # 定义红色的色调范围 (Hue values for red are approximately 0-10 and 170-180 in OpenCV's 0-179 range)
    lower_red_hue, upper_red_hue = 0, 10
    lower_red_hue_wrap, upper_red_hue_wrap = 170, 180
    # 创建红色区域的掩码
    red_mask = cv2.inRange(h, lower_red_hue, upper_red_hue) + cv2.inRange(h, lower_red_hue_wrap, upper_red_hue_wrap)
    # 对红色区域增加饱和度
    s_red = np.where(red_mask > 0, np.clip(s * red_saturation, 0, 255).astype(np.uint8), s)

    # 4. 降低非红色区域的饱和度
    # 创建非红色区域的掩码
    non_red_mask = cv2.bitwise_not(red_mask)
    s_non_red = np.where(non_red_mask > 0, np.clip(s * non_red_saturation, 0, 255).astype(np.uint8), s_red)

    # 5. 合并通道并将图像转回BGR
    final_hsv = cv2.merge([h, s_non_red, v])
    final_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return final_image

def resize_to_a4(image: np.ndarray, target_width=2100, top_crop_mm=62, bottom_crop_mm=10) -> np.ndarray:
    """ 将图像缩放和裁剪以模拟A4纸张。A4: 210mm x 297mm
    
    Args:
        image: 待裁剪图像
    """
    # 1. 等比例缩放图片，使其宽度达到目标宽度
    h, w, _ = image.shape
    ratio = target_width / w
    new_height = int(h * ratio)
    resized_image = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_AREA)

    # 2. 根据毫米数计算需要裁剪的像素数
    pixels_per_mm = target_width / 210
    top_crop_px = int(top_crop_mm * pixels_per_mm)
    bottom_crop_px = int(bottom_crop_mm * pixels_per_mm)

    # 4. 执行裁剪
    # 裁剪范围：从顶部 Y=top_crop_px 开始，到 Y=(总高度 - bottom_crop_px) 结束
    final_h, final_w, _ = resized_image.shape
    start_row = top_crop_px
    end_row = final_h - bottom_crop_px


    if start_row >= end_row:
        return resized_image
    cropped_image = resized_image[start_row:end_row, :]
    return cropped_image

def rotate_image(image: np.ndarray, dir: str = 'ccw') -> np.ndarray:
    """ 旋转图像

    Args:
        image np.ndarray: 待旋转图像
        dir: 'ccw' == 逆时针, 'cw' == 顺时针
    """
    if dir == 'ccw':
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif dir == 'cw':
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    else:
        raise ValueError("dir参数只能为'ccw'或'cw'")

