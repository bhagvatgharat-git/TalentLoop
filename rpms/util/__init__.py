"""Utility package exports."""

from rpms.util.branding import APP_NAME, APP_SUBTITLE, APP_TAGLINE
from rpms.util.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from rpms.util.console_input import pause_for_user, prompt_validated_input
from rpms.util.db_connection import get_connection
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.table_printer import print_table
from rpms.util.validators import (
    validate_date,
    validate_email,
    validate_future_date,
    validate_mobile,
    validate_non_empty,
    validate_non_negative_int,
    validate_percentage,
    validate_positive_int,
)

__all__ = [
    "APP_NAME",
    "APP_SUBTITLE",
    "APP_TAGLINE",
    "DB_HOST",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "get_connection",
    "log_activity",
    "generate_next_id",
    "print_table",
    "prompt_validated_input",
    "pause_for_user",
    "validate_non_empty",
    "validate_email",
    "validate_mobile",
    "validate_percentage",
    "validate_non_negative_int",
    "validate_positive_int",
    "validate_date",
    "validate_future_date",
]
