"""Job opening data model."""

from datetime import date, datetime
from typing import Optional, Union


class Job:
    """Represents a job vacancy posted by a partner company."""

    def __init__(
        self,
        job_id: str,
        company_id: str,
        job_title: str,
        technology: str,
        openings: int,
        location: str,
        package_lpa: float,
        min_percentage: float = 0.0,
        passing_year: int = 2024,
        max_backlogs: int = 0,
        deadline: Optional[Union[date, str]] = None,
        status: str = "OPEN",
        created_at: Optional[datetime] = None,
    ):
        self.job_id = job_id
        self.company_id = company_id
        self.job_title = job_title
        self.technology = technology
        self.openings = openings
        self.location = location
        self.package_lpa = package_lpa
        self.min_percentage = min_percentage
        self.passing_year = passing_year
        self.max_backlogs = max_backlogs
        self.deadline = deadline
        self.status = status
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"Job({self.job_id}, {self.job_title}, Company: {self.company_id}, "
            f"Tech: {self.technology}, Package: {self.package_lpa} LPA, Status: {self.status})"
        )

