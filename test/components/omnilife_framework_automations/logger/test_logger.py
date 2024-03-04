import logging
from io import StringIO
from omnilife_framework_automations.logger.logger import JsonLogHandler, setup_logger


def test_setup_logger_default():
    # Test setup_logger function with default level
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1


def test_setup_logger_custom_log_level():
    # Test setup_logger function with custom level
    logger = setup_logger("test_logger", level=logging.DEBUG)
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1


def test_setup_logger_existing_handlers():
    # Test setup_logger function with existing handlers
    existing_handler = logging.StreamHandler()
    logger = logging.getLogger("other_test_logger")
    logger.addHandler(existing_handler)
    logger = setup_logger("other_test_logger")
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert logger.handlers[0] is existing_handler


def test_json_log_handler_emit():
    # Test emit method of JsonLogHandler class
    handler = JsonLogHandler()
    record = logging.LogRecord(
        "test_logger", logging.INFO, "", 0, "Test message", (), None
    )
    stream = StringIO()
    handler.stream = stream

    handler.emit(record)

    expected_log = '{"message": "Test message"}\n'
    assert stream.getvalue() == expected_log


def test_json_log_handler_emit_with_params():
    # Test emit method of JsonLogHandler class with params
    handler = JsonLogHandler()
    record = logging.LogRecord(
        "test_logger", logging.INFO, "", 0, "Test message", (), None
    )
    record.params = {"param1": "value1", "param2": "value2"}
    stream = StringIO()
    handler.stream = stream

    handler.emit(record)

    expected_log = '{"message": "Test message", "params": {"param1": "value1", "param2": "value2"}}\n'
    assert stream.getvalue() == expected_log
