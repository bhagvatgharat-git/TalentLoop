"""Input validation utility functions."""

from datetime import date, datetime
import re
from typing import Any, Union

from rpms.exception import ValidationError

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
MOBILE_REGEX = re.compile(r"^[6-9]\d{9}$")


def validate_non_empty(value: Any, field_name: str = "Field") -> str:
    """Validate that a string value is not empty or whitespace."""
    if value is None:
        raise ValidationError(f"{field_name} cannot be empty.")
    cleaned = str(value).strip()
    if not cleaned:
        raise ValidationError(f"{field_name} cannot be empty.")
    return cleaned


def validate_email(value: Any) -> str:
    """Validate and normalize an email address."""
    cleaned = validate_non_empty(value, "Email").lower()
    if not EMAIL_REGEX.match(cleaned):
        raise ValidationError(f"Invalid email address: '{value}'.")
    return cleaned


def validate_mobile(value: Any) -> str:
    """Validate a 10-digit Indian mobile number starting with 6-9."""
    cleaned = validate_non_empty(value, "Mobile number")
    if not MOBILE_REGEX.match(cleaned):
        raise ValidationError("Mobile number must be a 10-digit Indian number starting with 6-9.")
    return cleaned


def validate_percentage(value: Any) -> float:
    """Validate that an academic percentage is between 0 and 100."""
    try:
        val = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Percentage must be a numeric value.") from exc

    if not (0.0 <= val <= 100.0):
        raise ValidationError("Percentage must be between 0.0 and 100.0.")
    return round(val, 2)


def validate_non_negative_int(value: Any, field_name: str = "Value") -> int:
    """Validate that an integer value is greater than or equal to zero."""
    try:
        val = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid integer.") from exc

    if val < 0:
        raise ValidationError(f"{field_name} must be a non-negative integer.")
    return val


def validate_positive_int(value: Any, field_name: str = "Value") -> int:
    """Validate that an integer value is strictly positive."""
    try:
        val = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid integer.") from exc

    if val <= 0:
        raise ValidationError(f"{field_name} must be a positive integer.")
    return val


def validate_date(value: Any, field_name: str = "Date") -> date:
    """Validate and parse a date formatted as YYYY-MM-DD."""
    if isinstance(value, date):
        return value
    cleaned = validate_non_empty(value, field_name)
    try:
        return datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be formatted as YYYY-MM-DD.") from exc


def validate_future_date(value: Any, field_name: str = "Date") -> date:
    """Validate that a date is today or in the future."""
    parsed_date = validate_date(value, field_name)
    if parsed_date < date.today():
        raise ValidationError(f"{field_name} must be today or a future date.")
    return parsed_date
