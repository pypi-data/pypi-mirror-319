import inspect
import warnings
import shutil
import os
import math
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, TextIO, Dict, Any

from .text_color import TextColor


class Logger:
    """Main logger class that handles all logging functionality."""

    # Configuration constants
    DEFAULT_TERMINAL_WIDTH = 80
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    LOG_LEVEL_WIDTH = 23
    MARGIN_WIDTH = 3  # For " | " separator
    
    def __init__(self):
        # Initialize default settings
        self._log_levels: Dict[str, int] = {
            "debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3,
            "critical": 4,
        }

        self._color_map: Dict[str, str] = {
            "warning": TextColor.yellow,
            "error": TextColor.orange,
            "critical": TextColor.red,
        }

        # Logging state
        self.display_level: str = "info"
        self.do_log: bool = True
        self.do_log_to_file: bool = False
        
        # File logging settings
        self._default_log_file_name: str = "%Y-%m-%d_%H-%M-%S.log"
        self.log_file_name: str = datetime.now().strftime(self._default_log_file_name)
        self._log_file: Optional[TextIO] = None

    def _format_timestamp(self) -> str:
        """Format current timestamp for logging."""
        return datetime.now().strftime(self.TIMESTAMP_FORMAT)[:-3]

    @staticmethod
    def _get_caller_info() -> str:
        """Gets information about the caller of the logging function."""
        stack = inspect.stack()
        frame = stack[2]  # The caller's frame
        return f'File "{frame.filename}", line {frame.lineno}, in {frame.function}'

    @staticmethod
    def _get_terminal_width() -> int:
        """Get the current terminal width."""
        try:
            return shutil.get_terminal_size().columns
        except (AttributeError, ValueError, OSError):
            try:
                return int(os.environ.get('COLUMNS', Logger.DEFAULT_TERMINAL_WIDTH))
            except ValueError:
                return Logger.DEFAULT_TERMINAL_WIDTH

    def _format_message_lines(self, msg: str, logging_level: str) -> list[str]:
        """Format message into lines that fit the terminal width."""
        available_width = self._get_terminal_width() - (self.LOG_LEVEL_WIDTH + self.MARGIN_WIDTH)
        msg_length = len(msg)
        num_lines = math.ceil(msg_length / available_width)
        
        # Split message into lines that fit the terminal
        raw_lines = [msg[i * available_width:(i + 1) * available_width] 
                    for i in range(num_lines)]
        
        # Format each line with proper indentation
        formatted_lines = []
        for i, line in enumerate(raw_lines):
            prefix = logging_level.upper() if i == 0 else ""
            formatted_lines.append(f"{prefix:>{self.LOG_LEVEL_WIDTH}} | {line}")
        
        return formatted_lines

    @contextmanager
    def _log_file_context(self):
        """Context manager for handling log file operations."""
        if self.do_log_to_file:
            with open(self.log_file_name, "a") as file:
                yield file
        else:
            yield None

    def _write_to_log(self, file: Optional[TextIO], *messages: str) -> None:
        """Write messages to log file if enabled."""
        if file:
            for message in messages:
                file.write(f"{message}\n")

    def _validate_log_level(self, level: str) -> None:
        """Validate that a log level exists."""
        if level.lower() not in self._log_levels:
            raise ValueError(
                f"Invalid logging level: {level}, must be one of: {list(self._log_levels.keys())}"
            )

    def __call__(self, msg: str, logging_level: str = "info") -> None:
        """Log a message with the specified logging level."""
        logging_level = logging_level.lower()
        self._validate_log_level(logging_level)

        # Check if we should log this message
        if (not self.do_log or 
            self._log_levels[logging_level] < self._log_levels[self.display_level]):
            return

        # Prepare log message components
        header = f"{self._format_timestamp()} | {self._get_caller_info()}"
        detail_lines = self._format_message_lines(msg, logging_level)
        
        # Apply color if specified for this level
        color = self._color_map.get(logging_level, "")
        if color:
            print(color, end="", flush=True)

        # Print and write to file
        with self._log_file_context() as log_file:
            print(header)
            self._write_to_log(log_file, header)
            
            for line in detail_lines:
                print(line)
                self._write_to_log(log_file, line)

        if color:
            print(TextColor.reset, end="", flush=True)

    def set_display_level(self, level: str) -> None:
        """Set the minimum logging level to display."""
        self._validate_log_level(level)
        self.display_level = level.lower()

    def log_to_file(self, file_name: Optional[str] = None) -> None:
        """Enable logging to a file."""
        if file_name is not None:
            self.log_file_name = file_name
        self.do_log_to_file = True

    def set_loglevel_color(self, level: str, color: str) -> None:
        """Set the color for a log level."""
        self._validate_log_level(level)
        
        if color.startswith("#"):
            if not self._is_valid_hex_color(color):
                raise ValueError("Invalid hex color code. Must be in format '#RRGGBB'")
            self._color_map[level] = self._hex_to_ansi(color)
            return

        if not hasattr(TextColor, color.lower()):
            valid_colors = [attr for attr in dir(TextColor) 
                          if not attr.startswith("_") and attr != "reset"]
            raise ValueError(
                f"Invalid color name. Must be a hex color code or one of: {', '.join(valid_colors)}"
            )
        
        self._color_map[level] = getattr(TextColor, color.lower())

    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """Validate hex color format."""
        return (len(color) == 7 and 
                all(c in "0123456789ABCDEFabcdef" for c in color[1:]))

    @staticmethod
    def _hex_to_ansi(hex_color: str) -> str:
        """Convert hex color to ANSI escape sequence."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"\u001b[38;2;{r};{g};{b}m"

    def create_custom_loglevel(self, name: str, color: Optional[str] = None) -> None:
        """Create a custom log level."""
        name = name.lower()
        try:
            self._validate_log_level(name)
            warnings.warn(f'Log level "{name}" already exists. Ignoring creation.')
            return
        except ValueError:
            pass

        self._log_levels[name] = len(self._log_levels)
        if color:
            self.set_loglevel_color(name, color)

    def log_on(self) -> None:
        """Enable logging."""
        self.do_log = True

    def log_off(self) -> None:
        """Disable logging."""
        self.do_log = False


# Global logger instance
log = Logger()
