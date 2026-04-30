"""
Logger - Simple logging utility for test execution
"""

import logging
import os
from datetime import datetime


class Logger:
    """Custom logger for test automation"""

    @staticmethod
    def setup_logger(name: str, log_dir: str = "logs"):
        """
        Setup and return a configured logger

        Args:
            name (str): Logger name (typically __name__)
            log_dir (str): Directory to store log files

        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create file handler
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(log_dir, f"test_execution_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        if not logger.handlers:  # Avoid duplicate handlers
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger
