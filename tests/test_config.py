"""Configuration foundation tests."""

from app.config import validate_config


def test_config_is_valid() -> None:
    """Verify startup configuration passes validation.

    Returns:
        None.

    Raises:
        AssertionError: If configuration validation fails.

    Example:
        >>> test_config_is_valid()
    """
    validate_config()
