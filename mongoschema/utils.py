import logging


# Exports
__all__ = ["logger"]

# Handle logging
logger = logging.getLogger('MongoSchema')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime) - %(message)"))
logger.addHandler(console_handler)
