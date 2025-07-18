"""
qwen_api.py

阿里Qwen模型API调用模块, 包含Qwen3文本分割模型和Qwen-VL图像识别模型

Author: Zhu Jiahao
Date: 2025-07-15
"""

import os
import base64
from openai import OpenAI
from src.utils.config import __config__
from src.utils.logger import __logger__

qwen_logger = __logger__.get_module_logger("Qwen")

class QwenClient:
    """Qwen服务API
    """
    def __init__(self, api_key, base_url, vl_model, text_model):
        self.api_key = api_key
        self.base_url = base_url
        self.vl_model = vl_model
        self.text_model = text_model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def ocr_image(self, image_path, prompt=None):
        """
        对图片进行OCR, 返回识别文本。
        prompt: 可选, 系统消息内容。
        """
        try:
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            mime = self._get_mime_type(image_path)
            messages = [
                {"role": "system", "content": [{"type": "text", "text": prompt or "你是一个试卷识别助手，请准确提取试卷中的所有文字内容，不要添加任何解释或说明，直接输出试卷原文。"}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    {"type": "text", "text": "请准确提取这张试卷中的所有文字内容"}
                ]}
            ]
            response = self.client.chat.completions.create(
                model=self.vl_model,
                messages=messages,
                stream=True
            )
            result = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if getattr(delta, "content", None):
                    result += delta.content
            return result
        except Exception as e:
            qwen_logger.error(f"QwenClient OCR error: {e}")
            exit()