"""
Environment configuration module for managing test environments and settings.
"""

import yaml
import os
from pathlib import Path


class Environment:
    """
    Environment configuration class to manage different test environments.
    """
    
    def __init__(self, env_name=None):
        """
        Initialize environment configuration.
        
        Args:
            env_name: Environment name (dev, staging, prod). If None, uses ENV environment variable or defaults to 'dev'
        """
        self.env_name = env_name or os.getenv('ENV', 'dev')
        self.config = self._load_config()
        self.current_env = self.config['environments'][self.env_name]
    
    def _load_config(self):
        """
        Load configuration from YAML file.
        
        Returns:
            dict: Configuration dictionary
        """
        config_path = Path(__file__).parent / 'config.yaml'
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")
    
    def get_base_url(self):
        """Get base URL for current environment."""
        return self.current_env['base_url']
    
    def get_username(self):
        """Get username for current environment."""
        return self.current_env['username']
    
    def get_password(self):
        """Get password for current environment."""
        return self.current_env['password']
    
    def get_browser_config(self):
        """Get browser configuration."""
        return self.config['browser']
    
    def get_logging_config(self):
        """Get logging configuration."""
        return self.config['logging'] 