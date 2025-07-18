"""
writing_api.py

机械臂书写API

Author: Zhu Jiahao
Date: 2025-07-18
"""

import pickle
from pymycobot.ultraArmP340 import ultraArmP340
from src.utils.config import __config__
from src.utils.logger import __logger__

writing_logger = __logger__.get_module_logger("Writing")

class RobotWritingClient:
    """机器人书写服务类
    """
    def __init__(self, com_port: str, baudrate: int, z_up: float, z_down: float, speed_move: int, speed_write: int, chinese_font_path: str):
        """
        初始化

        Args:
            com_port (str): 端口号
            baudrate (int): 波特率
            z_up (float): 抬笔高度
            z_down (float): 落笔高度
            speed_move (int): 移动画笔的速度
            speed_write (int): 写字的速度    
        """
        self.z_up = z_up
        self.z_down = z_down
        self.speed_move = speed_move
        self.speed_write = speed_write

        try:
            self.ua = ultraArmP340(com_port, baudrate)
        except:
            writing_logger.error("机器人无法连接")
            exit()
        
        try:
            with open(chinese_font_path, "rb") as f:
                self.chinese_font = pickle.load(f)
        except FileNotFoundError:
            writing_logger.error("找不到中文字体")
            exit()

            
