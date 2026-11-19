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
        candidate_name: Optional[str] = None,
        job_title: Optional[str] = None,
    ):
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.applied_date = applied_date
        self.status = status
        self.created_at = created_at
        self.candidate_name = candidate_name
        self.job_title = job_title

    def __str__(self) -> str:
        cand_str = f"{self.candidate_name} ({self.candidate_id})" if self.candidate_name else self.candidate_id
        job_str = f"{self.job_title} ({self.job_id})" if self.job_title else self.job_id
        return (
            f"Application({self.application_id}, Candidate: {cand_str}, "
            f"Job: {job_str}, Status: {self.status}, Applied: {self.applied_date})"
        )
