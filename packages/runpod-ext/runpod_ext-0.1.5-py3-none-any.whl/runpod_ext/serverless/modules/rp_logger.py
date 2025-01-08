import os
import socket
import logging
import logging.handlers

MAX_MESSAGE_LENGTH = 4096
LOG_LEVELS = ["NOTSET", "TRACE", "DEBUG", "INFO", "WARN", "ERROR"]

class RunPodLogger:
    """Singleton class for logging with Python's logging library."""

    __instance = None
    log_port = int(os.environ.get("LOG_PORT", "10518"))
    log_host = os.environ.get("LOG_HOST", "localhost")

    def __new__(cls):
        if RunPodLogger.__instance is None:
            RunPodLogger.__instance = object.__new__(cls)
            RunPodLogger.__instance._initialize_logger()
        return RunPodLogger.__instance

    def _initialize_logger(self):
        """Initializes the logger."""
        self.logger = logging.getLogger("RunPodLogger")
        self.logger.setLevel(self._validate_log_level(
            os.environ.get("RUNPOD_LOG_LEVEL", os.environ.get("RUNPOD_DEBUG_LEVEL", "DEBUG"))
        ))

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s | %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # TCP Socket Handler
        try:
            sock_handler = TCPSocketHandler(self.log_host, self.log_port)
            formatter = logging.Formatter('%(levelname)s | %(message)s')
            sock_handler.setFormatter(formatter)
            self.logger.addHandler(sock_handler)
        except Exception as e:
            self.logger.error(f"Failed to set up TCP socket logging: {e}")

    def _validate_log_level(self, level):
        """Validates and returns a logging level."""
        level = level.upper()
        if level in LOG_LEVELS:
            return getattr(logging, level, logging.DEBUG)
        raise ValueError(f"Invalid log level: {level}")

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
            job_id = str(job_id).replace('|', '_')  # Sanitize job_id
            message = f"{job_id} | {message}"

        log_method = getattr(self.logger, message_level.lower(), self.logger.info)
        log_method(message)

    def debug(self, message, request_id=None):
        self.log(message, "DEBUG", request_id)

    def info(self, message, request_id=None):
        self.log(message, "INFO", request_id)

    def warn(self, message, request_id=None):
        self.log(message, "WARN", request_id)

    def error(self, message, request_id=None):
        self.log(message, "ERROR", request_id)

    def trace(self, message, request_id=None):
        self.log(message, "TRACE", request_id)

# TCPSocketHandler for network socket
class TCPSocketHandler(logging.Handler):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = None
        self._connect()

    def _connect(self):
        """Establishes TCP connection"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print(f"TCP connection error: {e}")
            self.sock = None

    def emit(self, record):
        """Sends log message over TCP socket"""
        try:
            if not self.sock:
                self._connect()
            if self.sock:
                log_entry = self.format(record)
                self.sock.sendall((log_entry + '\n').encode())
        except Exception as e:
            print(f"TCP logging error: {e}")
            self.sock = None  # Reset socket on error for next attempt