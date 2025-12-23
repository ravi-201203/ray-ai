import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import json
import uuid
import contextvars

# ---------------- Context Variables ----------------
request_id_var = contextvars.ContextVar("request_id", default=None)
trace_id_var = contextvars.ContextVar("trace_id", default=None)

def set_request_id(request_id=None):
    """Set or generate a request_id for current context"""
    if not request_id:
        request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

def set_trace_id(trace_id=None):
    """Set or generate a trace_id for current context"""
    if not trace_id:
        trace_id = str(uuid.uuid4())
    trace_id_var.set(trace_id)

def clear_ids():
    """Clear IDs at end of request"""
    request_id_var.set(None)
    trace_id_var.set(None)

# ---------------- Configurable Log Level ----------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_TXT = os.path.join(LOG_DIR, "rutusoft.log")
LOG_FILE_JSON = os.path.join(LOG_DIR, "rutusoft.json")

# ---------------- JSON Formatter ----------------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.threadName,
            "request_id": request_id_var.get(),
            "trace_id": trace_id_var.get(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# ---------------- Logger Setup ----------------
logger = logging.getLogger("rutusoft")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(process)d - "
        "[%(module)s.%(funcName)s:%(lineno)d] - "
        "request_id=%(request_id)s trace_id=%(trace_id)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # File handler (text)
    file_handler_txt = RotatingFileHandler(LOG_FILE_TXT, maxBytes=1_000_000, backupCount=5)
    file_handler_txt.setLevel(logging.INFO)
    file_handler_txt.setFormatter(console_formatter)

    # File handler (JSON)
    file_handler_json = RotatingFileHandler(LOG_FILE_JSON, maxBytes=2_000_000, backupCount=3)
    file_handler_json.setLevel(logging.INFO)
    file_handler_json.setFormatter(JsonFormatter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler_txt)
    logger.addHandler(file_handler_json)

# ---------------- Inject Correlation IDs into LogRecord ----------------
old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.request_id = request_id_var.get()
    record.trace_id = trace_id_var.get()
    return record
logging.setLogRecordFactory(record_factory)