"""
logger.py

This module provides the logging service for the whole program
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from ..core.config import config_manager

class Logger:
    """The Logging Manager
    
    @TODO: Describe the specific api
    """

    def __init__(self):
        self._loggers = {}
        self.setup_root_logger()

    def setup_root_logger(self) -> None:
        """ Setup Root Logger
        """
        log_config = config_manager.get_logging_config()
        log_level = getattr(logging, log_config.get('level', 'INFO'))

        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.handlers.clear()
        formatter = logging.Formatter(
            log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # File Handler
        log_path = config_manager.get('paths.output.logs')
        if log_path:
            log_file = Path(log_path) / "AIExam.log"
            file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file,
                when='midnight',
                interval=1,
                backupCount=log_config.get('max_files', 7),
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """ Get the logger with the given name
        
        Args:
            name: the name of the logger
        """
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)
        return self._loggers[name]

    def get_module_logger(self, module_name: str) -> logging.Logger:
        """ Get the logger with the given module

        Args:
            module_name: the name of the module
        """
        return self.get_logger(f"AIExam.{module_name}")
    
# Global Instance
logger_manager = Logger()
