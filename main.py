"""
main.py
AIExamPlus - An AI-driven automatic exam answering system
The entrance of the system.

Author: Zhu Jiahao
Date: 2025-07-14
"""

import sys
from pathlib import Path
from src.utils.logger import logger_manager
# from src.core.config import config_manager

def main():
    """
    @TODO: Describe the whole pipeline
    """
    main_logger = logger_manager.get_module_logger("main")

    main_logger.info("=====================================================")
    main_logger.info("===               Start the Pipeline              ===")
    main_logger.info("=====================================================")



    main_logger.info("=====================================================")
    main_logger.info("===               Pipeline Finished               ===")
    main_logger.info("=====================================================")

if __name__ == "__main__":
    main()