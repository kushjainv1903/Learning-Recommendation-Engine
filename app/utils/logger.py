"""Logging setup utilities for LearnPath AI."""

import logging

from app.config import LOG_FORMAT, LOG_LEVEL


def configure_logging() -> None:
    """Configure application logging.

    Returns:
        None.

    Raises:
        ValueError: If the configured logging level is invalid.

    Example:
        >>> configure_logging()
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        force=True,
    )
