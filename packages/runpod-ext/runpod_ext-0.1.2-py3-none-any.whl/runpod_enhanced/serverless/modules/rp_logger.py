import json
import os
import socket
import logging
from logging import Handler
from typing import Optional

MAX_MESSAGE_LENGTH = 4096
LOG_LEVELS = ["NOTSET", "TRACE", "DEBUG", "INFO", "WARN", "ERROR"]
SOCKET_PATH = "/var/run/log.sock"  # Path for the Unix socket

class UnixSocketHandler(Handler):
    """Custom handler that sends log messages to a Unix socket."""
    
    def __init__(self, socket_path: str):
        super().__init__()
        self.socket_path = socket_path
        self.socket_connection = self._initialize_socket()

    def _initialize_socket(self):
        """Initialize a Unix socket connection."""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            sock.connect(self.socket_path)
            return sock
        except socket.error as e:
            # If unable to connect, fallback to stdout logging
            print(f"Unable to connect to {self.socket_path}: {e}")
            return None

    def emit(self, record):
        """Emit a log record to the Unix socket."""
        log_message = self.format(record)
        
        # If the socket connection exists, send the log message
        if self.socket_connection:
            try:
                self.socket_connection.sendall(log_message.encode())
            except socket.error:
                # If an error occurs while sending, fall back to stdout logging
                print("Error sending log message to Datadog. Falling back to stdout.")
                self._log_to_stdout(log_message)

        # If socket connection is not available, log to stdout
        else:
            self._log_to_stdout(log_message)

    def _log_to_stdout(self, message):
        """Fallback to stdout logging if the socket connection fails."""
        print(message)

class RunPodLogger:
    """Singleton class for logging with custom handler."""
    
    __instance = None
    level = "DEBUG"  # Default log level
    logger = None

    def __new__(cls):
        if RunPodLogger.__instance is None:
            RunPodLogger.__instance = object.__new__(cls)
            cls.logger = cls._initialize_logger()
        return RunPodLogger.__instance

    @staticmethod
    def _initialize_logger():
        """Initialize the logger and add custom UnixSocketHandler."""
        logger = logging.getLogger("RunPodLogger")
        logger.setLevel(logging.DEBUG)
        
        # Add the custom UnixSocketHandler
        socket_handler = UnixSocketHandler(SOCKET_PATH)
        formatter = logging.Formatter('%(levelname)s | %(message)s')
        socket_handler.setFormatter(formatter)
        logger.addHandler(socket_handler)

        return logger

    def set_level(self, new_level):
        """Set the log level for the logger."""
        self.level = new_level
        self.logger.setLevel(new_level)
        self.info(f"Log level set to {self.level}")

    def log(self, message, message_level="INFO", job_id=None):
        """Log message to Unix socket using the logger."""
        if self.level == "NOTSET":
            return

        if job_id:
            message = f"{job_id} | {message}"

        log_message = f"{message_level.ljust(7)}| {message}"
        
        log_func = getattr(self.logger, message_level.lower())
        log_func(log_message)

    def secret(self, secret_name, secret):
        """Censors secrets for logging."""
        secret = str(secret)
        redacted_secret = secret[0] + "*" * (len(secret) - 2) + secret[-1]
        self.info(f"{secret_name}: {redacted_secret}")

    def debug(self, message, request_id: Optional[str] = None):
        """debug log"""
        self.log(message, "DEBUG", request_id)

    def info(self, message, request_id: Optional[str] = None):
        """info log"""
        self.log(message, "INFO", request_id)

    def warn(self, message, request_id: Optional[str] = None):
        """warn log"""
        self.log(message, "WARN", request_id)

    def error(self, message, request_id: Optional[str] = None):
        """error log"""
        self.log(message, "ERROR", request_id)

    def tip(self, message):
        """tip log"""
        self.log(message, "TIP")

    def trace(self, message, request_id: Optional[str] = None):
        """trace log"""
        self.log(message, "TRACE", request_id)
