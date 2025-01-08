import os
import socket
import logging
import logging.handlers

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
            os.environ.get("RUNPOD_LOG_LEVEL", os.environ.get("RUNPOD_DEBUG_LEVEL", "DEBUG"))
        ))

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s | %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Socket Handler (for .sock file)
        if self.sock_file:
            try:
                self._initialize_sock_file()
                sock_handler = UnixSocketHandler(self.sock_file)
                formatter = logging.Formatter('%(levelname)s | %(message)s')
                sock_handler.setFormatter(formatter)
                self.logger.addHandler(sock_handler)
            except Exception as e:
                self.logger.error(f"Failed to set up Unix socket logging: {e}")

    def _initialize_sock_file(self):
        """Creates and initializes the Unix socket file."""
        # Clean up any existing .sock file
        if os.path.exists(self.sock_file):
            os.remove(self.sock_file)

        # Create the socket and bind to the path
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        server_socket.bind(self.sock_file)

        # Optional: Set permissions for the socket file
        os.chmod(self.sock_file, 0o666)

        # Close the server socket if only creating the file
        server_socket.close()

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

# UnixSocketHandler for .sock file
class UnixSocketHandler(logging.Handler):
    def __init__(self, socket_path):
        super().__init__()
        self.socket_path = socket_path
        self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.client_socket.sendto(log_entry.encode(), self.socket_path)
        except Exception as e:
            print(f"Socket logging error: {e}")
