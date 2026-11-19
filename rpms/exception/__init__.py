"""Exception package exports."""

from rpms.exception.custom_exceptions import (
    CandidateNotEligibleError,
    CandidateNotFoundError,
    CompanyNotFoundError,
    DatabaseConnectionError,
    DuplicateApplicationError,
    InvalidStatusTransitionError,
    JobNotFoundError,
    RPMSException,
    ValidationError,
)

__all__ = [
    "RPMSException",
    "ValidationError",
    "DatabaseConnectionError",
    "CandidateNotFoundError",
    "JobNotFoundError",
    "CompanyNotFoundError",
    "DuplicateApplicationError",
    "CandidateNotEligibleError",
    "InvalidStatusTransitionError",
]
