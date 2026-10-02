import logging
import inspect
from pathlib import Path


# ANSI Escape Codes for Terminal Colors
class LogColors:
    RESET = "\033[0m"
    DEBUG = "\033[36m"  # Cyan
    INFO = "\033[32m"  # Green
    WARNING = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red
    CRITICAL = "\033[41m"  # Red Background / White text


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Pick the color based on the log level
        color = getattr(LogColors, record.levelname, LogColors.RESET)

        # Format the standard message first
        formatted_message = super().format(record)

        # Wrap it in color and reset at the end
        return f"{color}{formatted_message}{LogColors.RESET}"


def log() -> logging.Logger:

    # 1. FIND THE CORRECT PATH

    # Make sure the logs folder exists
    logs_dir = Path.cwd() / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Inspect the stack to find the script that called the logger
    caller_frame = inspect.stack()[1]
    caller_file = Path(caller_frame.filename).resolve()
    script_name = caller_file.stem

    # Construct file path
    log_file_path = logs_dir / f"{script_name}.log"

    # 2. SET UP THE LOGGER

    # Create the customer logger and set the base level
    pipeline_logger = logging.getLogger(script_name)
    pipeline_logger.setLevel(logging.INFO)

    # Prevent duplicates handlers
    if pipeline_logger.handlers:
        return pipeline_logger

    # Define the format

    # 1. Standard white format for the file
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # 2. Custom colored format for the console
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    pipeline_logger.addHandler(file_handler)
    pipeline_logger.addHandler(console_handler)

    return pipeline_logger
