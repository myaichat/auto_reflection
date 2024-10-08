from .include.config import init_config
from .include.utils import execute_pipeline

# Initialize apc globally
init_config.init(**{})  # Initialize the configuration
apc = init_config.apc  # Expose apc

__all__ = ['execute_pipeline', 'apc']