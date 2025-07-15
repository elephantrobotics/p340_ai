"""
config.py
This module provides the loading and managing of the configs

Author: Zhu Jiahao
Date: 2025-07-14
"""

import os
import shutil
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """ConfigManager

    @TODO: Describe the detailed api of this class
    """

    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self._config = {}
        self.load_config()

    def load_config(self) -> None:
        """load the config file
        """
        try:
            print("Loading System Configuration files ...")

            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)

            # @TODO: process environment variables

            # create the dict
            self.create_dict()


        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not exist: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Configuration file format error: {e}")

    def create_dict(self) -> None:
        """create the directory for the input and output data
        """
        paths = self._config.get('paths', {})
        for path_type, path_config in paths.items():
            if isinstance(path_config, dict):
                for key, path_str in path_config.items():
                    # Path(path_str).mkdir(parents=True, exist_ok=True)
                    self.ensure_empty_dir(path_str)
            elif isinstance(path_config, str):
                # Path(path_config).mkdir(parents=True, exist_ok=True)
                self.ensure_empty_dir(path_config)  

        print("All directories are generated!")

    def ensure_empty_dir(self, path_str: str) -> None:
        """Ensure all the directories is empty

        Args:
            path_str: the specific path.
        """
        path = Path(path_str)
        
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
        
        path.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """Get values from nested dictionaries by dot-separated key path

        Args:
            key: dot-separated key path string
            default: default value to return when path does not exist (defaults to None)

        Returns:
            Found value, or default value (when path does not exist)
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    def get_api_config(self, service: str) -> Dict[str, str]:
        """ Get API Config
        """
        return self.get(f'api.{service}', {})
    
    def get_path_config(self) -> Dict[str, Any]:
        """ Get Path Config
        """
        return self.get('paths', {})
    
    def get_robot_config(self) -> Dict[str, Any]:
        """ Get Robot Config
        """
        return self.get('robot', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """ Get Logging Config
        """
        return self.get('logging', {})

# Global instance of config manager
config_manager = ConfigManager()