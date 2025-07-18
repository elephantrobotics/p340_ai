"""
main.py
运行整个项目完整的流程管线

Author: Zhu Jiahao
Date: 2025-07-14
"""

import sys
from src.api.writing_api import RobotWritingClient
from src.utils.config import __config__
from src.utils.logger import __logger__

def main():
    """
    @TODO: Describe the whole pipeline
    """
    pipeline_logger = __logger__.get_module_logger("pipeline")

    # 初始化
    robot_config = __config__.get_robot_config()
    robot_writer = RobotWritingClient(
        robot_config.get("com_port"),
        robot_config.get("baudrate"),
        robot_config.get("z_up"),
        robot_config.get("z_down"),
        robot_config.get("speed_move"),
        robot_config.get("speed_write"),
    )

    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Start the Pipeline              ===")
    pipeline_logger.info("=====================================================")







    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Pipeline Finished               ===")
    pipeline_logger.info("=====================================================")

if __name__ == "__main__":
    main()