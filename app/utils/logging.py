import logging
try:
    from python_json_logger import jsonlogger
except Exception:
    jsonlogger = None

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if jsonlogger:
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            "%(levelname)s %(asctime)s %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.handlers = [handler]
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(asctime)s %(name)s %(message)s",
        )
