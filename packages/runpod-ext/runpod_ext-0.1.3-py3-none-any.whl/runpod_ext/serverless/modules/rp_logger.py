import json
import logging
import logging.handlers
import os
from typing import Optional

MAX_MESSAGE_LENGTH = 4096
LOG_LEVELS = ["NOTSET", "TRACE", "DEBUG", "INFO", "WARN", "ERROR"]

class RunPodLogger:
    """Singleton class for logging with Python's logging library."""

    __instance = None
    sock_file = os.environ.get("LOG_SOCK_FILE", "/var/run/log.sock")

    def __new__(cls):
        if RunPodLogger.__instance is None:
            RunPodLogger.__instance = object.__new__(cls)
            RunPodLogger.__instance._initialize_logger()
        return RunPodLogger.__instance

    def _initialize_logger(self):
        """Initializes the logger."""
        self.logger = logging.getLogger("RunPodLogger")
        self.logger.setLevel(self._validate_log_level(
            os.environ.get(
                "RUNPOD_LOG_LEVEL", os.environ.get("RUNPOD_DEBUG_LEVEL", "DEBUG")
            )
        ))

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s | %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Socket Handler (for .sock file, if configured)
        if self.sock_file:
            try:
                sock_handler = logging.handlers.SocketHandler(self.sock_file, None)
                self.logger.addHandler(sock_handler)
            except Exception as e:
                self.logger.error(f"Failed to set up socket logging: {e}")

    def _validate_log_level(self, level):
        """Validates and returns a logging level."""
        if isinstance(level, str):
            level = level.upper()
            if level in LOG_LEVELS:
                return getattr(logging, level, logging.DEBUG)
            raise ValueError(f"Invalid log level: {level}")
        if isinstance(level, int) and level in range(len(LOG_LEVELS)):
            return level * 10
        raise ValueError(f"Invalid log level: {level}")

    def set_level(self, new_level):
        """Sets a new log level."""
        level = self._validate_log_level(new_level)
        self.logger.setLevel(level)
        self.info(f"Log level set to {logging.getLevelName(level)}")

    def log(self, message, message_level="INFO", job_id=None):
        """Logs a message."""
        if not message:
            return

        message_level = message_level.upper()
        if message_level not in LOG_LEVELS:
            raise ValueError(f"Invalid log level: {message_level}")

        # Truncate long messages
        if len(message) > MAX_MESSAGE_LENGTH:
            half_max_length = MAX_MESSAGE_LENGTH // 2
            truncated_amount = len(message) - MAX_MESSAGE_LENGTH
            truncation_note = f"\n...TRUNCATED {truncated_amount} CHARACTERS...\n"
            message = (
                message[:half_max_length] + truncation_note + message[-half_max_length:]
            )

        # Add job_id if provided
        if job_id:
            message = f"{job_id} | {message}"

        log_method = getattr(self.logger, message_level.lower(), self.logger.info)
        log_method(message)

    def secret(self, secret_name, secret):
        """Censors secrets for logging."""
        secret = str(secret)
        redacted_secret = secret[0] + "*" * (len(secret) - 2) + secret[-1]
        self.info(f"{secret_name}: {redacted_secret}")

    def debug(self, message, request_id: Optional[str] = None):
        self.log(message, "DEBUG", request_id)

    def info(self, message, request_id: Optional[str] = None):
        self.log(message, "INFO", request_id)

    def warn(self, message, request_id: Optional[str] = None):
        self.log(message, "WARN", request_id)

    def error(self, message, request_id: Optional[str] = None):
        self.log(message, "ERROR", request_id)

    def trace(self, message, request_id: Optional[str] = None):
        self.log(message, "TRACE", request_id)

    def tip(self, message):
        self.log(message, "INFO")  # Use INFO for TIP logs

