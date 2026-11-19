"""Custom domain exceptions for the RPMS application."""


class RPMSException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str = "An unexpected application error occurred."):
        super().__init__(message)


class ValidationError(RPMSException):
    """Raised when user input fails validation constraints."""

    def __init__(self, message: str = "Invalid input data provided."):
        super().__init__(message)


class DatabaseConnectionError(RPMSException):
    """Raised when connection to MySQL database cannot be established."""

    def __init__(self, message: str = "Failed to connect to the database."):
        super().__init__(message)


class CandidateNotFoundError(RPMSException):
    """Raised when a requested candidate record is not found."""

    def __init__(self, message: str = "Candidate record not found."):
        super().__init__(message)


class JobNotFoundError(RPMSException):
    """Raised when a requested job opening is not found."""

    def __init__(self, message: str = "Job opening not found."):
        super().__init__(message)


class CompanyNotFoundError(RPMSException):
    """Raised when a requested company record is not found."""

    def __init__(self, message: str = "Company record not found."):
        super().__init__(message)


class DuplicateApplicationError(RPMSException):
    """Raised when a candidate has already applied for the specified job."""

    def __init__(self, message: str = "Candidate has already applied for this job."):
        super().__init__(message)


class CandidateNotEligibleError(RPMSException):
    """Raised when a candidate does not meet job criteria."""

    def __init__(self, message: str = "Candidate does not meet the eligibility criteria."):
        super().__init__(message)


class InvalidStatusTransitionError(RPMSException):
    """Raised when an application status transition is invalid."""

    def __init__(self, message: str = "Invalid status transition requested."):
        super().__init__(message)
