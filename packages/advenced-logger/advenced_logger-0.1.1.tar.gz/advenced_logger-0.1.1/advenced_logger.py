import multiprocessing
import os
import sys
import threading
from functools import wraps
from typing import Optional, Dict, Any, Callable

from loguru import logger


class AdvancedLogger:
    """
    Advanced logging configuration with support for multi-threading and multi-processing.
    Provides structured logging, context management, and automatic rotation.
    """
    
    def __init__(
        self,
        log_dir: str = "logs",
        app_log_filename: str = "app_{time}.log",
        error_log_filename: str = "error_{time}.log",
        console_level: str = "INFO",
        file_level: str = "DEBUG",
        error_level: str = "ERROR",
        retention: str = "10 days",
        rotation: str = "500 MB",
        compression: str = "zip",
        extra_handlers: Optional[Dict] = None
    ):
        """
        Initialize the logger with custom configuration.
        
        Args:
            log_dir: Directory for log files
            app_log_filename: Filename pattern for application logs
            error_log_filename: Filename pattern for error logs
            console_level: Minimum level for console output
            file_level: Minimum level for file output
            error_level: Minimum level for error file
            retention: How long to keep logs
            rotation: When to rotate logs
            compression: Compression format for rotated logs
            extra_handlers: Additional log handlers configuration
        """
        self.log_dir = log_dir
        self._create_log_directory()
        
        # Remove default handlers
        logger.remove()

        # Store the logger instance
        self.logger = logger
        
        # Set up handlers
        self.setup_handlers(
            console_level=console_level,
            file_level=file_level,
            error_level=error_level,
            app_log_filename=app_log_filename,
            error_log_filename=error_log_filename,
            retention=retention,
            rotation=rotation,
            compression=compression
        )
        
        # Add any extra handlers
        if extra_handlers:
            self.add_extra_handlers(extra_handlers)        
    
    def _create_log_directory(self) -> None:
        """Create log directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _get_log_format(self) -> str:
        """Define the log format with process and thread information."""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "P:{process.id} T:{thread.id} | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "{extra} | "
            "<level>{message}</level>"
        )
    
    def setup_handlers(
        self,
        console_level: str,
        file_level: str,
        error_level: str,
        app_log_filename: str,
        error_log_filename: str,
        retention: str,
        rotation: str,
        compression: str
    ) -> None:
        """Set up standard log handlers."""
        # Console handler
        self.logger.add(
            sys.stdout,
            format=self._get_log_format(),
            level=console_level,
            colorize=True,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )
        
        # File handler
        self.logger.add(
            os.path.join(self.log_dir, app_log_filename),
            format=self._get_log_format(),
            level=file_level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            mode="a",
            buffering=1
        )
        
        # Error file handler
        self.logger.add(
            os.path.join(self.log_dir, error_log_filename),
            format=self._get_log_format(),
            filter=lambda record: record["level"].name in ["ERROR", "CRITICAL"],
            level=error_level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            mode="a",
            buffering=1
        )
    
    def add_extra_handlers(self, handlers: Dict[str, Dict[str, Any]]) -> None:
        """Add additional log handlers from configuration."""
        for name, config in handlers.items():
            self.logger.add(**config)
    
    @staticmethod
    def exception_decorator(func: Callable) -> Callable:
        """Decorator for catching and logging exceptions."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    f"Exception in {func.__name__}: {str(e)} "
                    f"[Process:{multiprocessing.current_process().name}, "
                    f"Thread:{threading.current_thread().name}]"
                )
                raise
        return wrapper
    
    def get_logger(self):
        """Get the configured logger instance."""
        return self.logger

# Create a default logger instance
default_logger = AdvancedLogger()
logger = default_logger.get_logger()
exception_decorator = default_logger.exception_decorator

# Convenience functions
def setup_logger(**kwargs) -> AdvancedLogger:
    """Create a new logger instance with custom configuration."""
    return AdvancedLogger(**kwargs)

def get_default_logger():
    """Get the default logger instance."""
    return logger