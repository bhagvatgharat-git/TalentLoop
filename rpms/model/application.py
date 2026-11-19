"""Job application data model."""

from datetime import date, datetime
from typing import Optional, Union


class Application:
    """Represents a candidate's application for a specific job."""

    def __init__(
        self,
        application_id: str,
        candidate_id: str,
        job_id: str,
        applied_date: Union[date, str],
        status: str = "APPLIED",
        created_at: Optional[datetime] = None,
    ):
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.applied_date = applied_date
        self.status = status
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"Application({self.application_id}, Candidate: {self.candidate_id}, "
            f"Job: {self.job_id}, Status: {self.status}, Applied: {self.applied_date})"
        )
