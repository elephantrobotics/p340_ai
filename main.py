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
    assets_confog = __config__.get_assets_config()

    robot_writer = RobotWritingClient(
        robot_config.get("com_port"),
        robot_config.get("baudrate"),
        robot_config.get("z_up"),
        robot_config.get("z_down"),
        robot_config.get("speed_move"),
        robot_config.get("speed_write"),
        robot_config.get("origin_x"),
        robot_config.get("origin_y"),
        assets_confog.get("chinese_fonts")
    )

    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Start the Pipeline              ===")
    pipeline_logger.info("=====================================================")

    # robot_writer.write_chinese_char("你", 235.55, 0, 10)
    # robot_writer.write_ascii_char("D", 235.55, 0, 10)
    # robot_writer.write_text_line("牛的", 235.55, 0, 10, 10)
    robot_writer.calibrate_origin()
    # robot_writer.stand_by()
    robot_writer.write_text_line("你好, 高考试卷", 20, 10, 10, 1.1)
    robot_writer.stand_by()

    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Pipeline Finished               ===")
    pipeline_logger.info("=====================================================")

if __name__ == "__main__":
    main()