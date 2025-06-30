from typing import Optional

import logging

DEFAULT_NAME = 'coin-surfer'


def get_logger(name: Optional[str] = DEFAULT_NAME):
    logger = logging.getLogger(name)
    return logger
