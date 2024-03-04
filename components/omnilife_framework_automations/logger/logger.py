import logging
import json


class JsonLogHandler(logging.StreamHandler):
    def emit(self, record):
        # Create a dictionary that includes all the information you want to log
        log_record = {
            "message": record.getMessage(),
        }
        # Safely add extra attributes avoiding internal attribute names
        if hasattr(record, "params"):
            log_record["params"] = record.params

        json_log = json.dumps(log_record)
        stream = self.stream
        stream.write(json_log + "\n")
        stream.flush()


def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent the log messages from being duplicated to the default logger
    logger.propagate = False

    # Check if the logger already has handlers attached and skip adding another to avoid duplicate logs
    if not logger.handlers:
        json_handler = JsonLogHandler()
        logger.addHandler(json_handler)

    return logger
