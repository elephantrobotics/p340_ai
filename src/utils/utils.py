"""
utils.py 
所有常见工具函数的集合

Author: Zhu Jiahao
Date: 2025-07-17
"""

import base64
import os
import re

def encode_image_to_base64(path: str) -> str:
    """
    将图像文件编码为Base64字符串

        处理过程:
        1. 以二进制模式读取文件内容
        2. 使用base64进行编码
        3. 将bytes类型结果解码为UTF-8字符串
    
    Args:
        path (str): 图像文件的路径
        
    Return:
        str: 经过Base64编码后的UTF-8格式字符串
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def get_image_mime_type(path: str) -> str:
    """
    根据文件扩展名获取对应的MIME类型

        支持格式:
        - .jpg/.jpeg -> image/jpeg
        - .png -> image/png
        - .webp -> image/webp

    Args:
        path (str): 图像文件的路径
        
    Return:
        str: 标准MIME类型字符串
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.webp':
        return 'image/webp'
    else:
        raise ValueError(f"Unsupported image format: {ext}")

def read_txt_file(path: str, encoding: str = "utf-8") -> str:
    """
    读取一个 .txt 文件，并返回其全部内容（str 格式）。

    Args:
        path (str): 文件路径
        encoding (str): 文件编码，默认为 'utf-8'

    Returns:
        str: 文件内容
    """
    with open(path, "r", encoding=encoding) as f:
        return f.read()


# def save_units_from_text(raw: str, output_dir: str = )