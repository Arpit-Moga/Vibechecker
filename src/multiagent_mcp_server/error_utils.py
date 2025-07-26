import logging
import traceback

# Centralized logger setup
def get_logger(name: str = "multiagent_mcp_server"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# Standardized error formatting
def format_exception(e: Exception, context: str = "") -> str:
    tb = traceback.format_exc()
    return f"Exception in {context}: {str(e)}\n{tb}"

# Decorator for standardized error handling
def handle_errors(logger=None, context=""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log = logger or get_logger()
                log.error(format_exception(e, context or func.__name__))
                raise
        return wrapper
    return decorator