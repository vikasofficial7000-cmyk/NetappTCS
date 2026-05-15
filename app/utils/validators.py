"""Input validation utilities."""

from pydantic import ValidationError
from typing import Any, Type, TypeVar

T = TypeVar('T')


def validate_input(data: Any, model: Type[T]) -> tuple[bool, T | None, str | None]:
    """Validate input against Pydantic model.

    Args:
        data: Data to validate
        model: Pydantic model class

    Returns:
        Tuple of (is_valid, validated_data, error_message)
    """
    try:
        validated = model(**data)
        return True, validated, None
    except ValidationError as e:
        error_msg = str(e)
        return False, None, error_msg
