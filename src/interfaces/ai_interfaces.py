"""
ai_interfaces.py

AI相关功能的接口定义

Author: Zhu Jiahao
Date: 2025-07-15
"""

from typing import List, Dict, Any
from openai import OpenAI
from ..core.config import config_manager
from ..utils.logger import logger_manager

ai_logger = logger_manager.get_module_logger("AIService")

class AIService:
    """ AI接口

    @TODO: add some async interfaces
    """
    
    def __init__(self, model_type: str = 'deepseek'):
        api_config = config_manager.get_api_config(model_type)
        self.client = OpenAI(
            api_key=api_config.get('api_key'),
            base_url=api_config.get('base_url')
        )
        self.model = api_config.get('model')
        self.model_type = model_type

    def generate_text(self, messages, **kwargs) -> str:
        """ 生成文本(同步, 非流式)

        Args:
            messages (List[Dict[str, str]]): 历史信息列表

        Returns:
            str: 生成的回复
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            ai_logger.error(f"{self.model_type}API调用失败: {e}")
            
    def generate_text_stream(self, messages, **kwargs):
        """ 生成文本(同步, 流式)

        Args:
            messages (List[Dict[str, str]]): 历史信息列表

        Returns:
            str: 生成的回复流
        """
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs
            )
        except Exception as e:
            ai_logger.error(f"{self.model_type}流式API调用失败: {e}")

    def image_ocr(self, image_path: str, prompt: str, **kwargs) -> str:
        """OCR处理 (仅限: QWen-vl)

        Args:
            image_path str: 图片路径
            prompt str: 提示词

        Returns:
            生成的结果
        """
        if self.model_type != 'qwen-vl':
            raise Exception(f"{self.model_type}不支持OCR, 请重新检查模型选择")
        
        try:
            messages = [
                {"role": "user", "content": [
                    {"image": image_path},
                    {"text": prompt}
                ]}
            ]
            return self.generate_text(messages, **kwargs)
        except Exception as e:
            ai_logger.error(f"OCR失败")