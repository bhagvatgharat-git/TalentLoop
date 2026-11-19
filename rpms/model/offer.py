"""Job offer data model."""

from datetime import date, datetime
from typing import Optional, Union


class Offer:
    """Represents a formal job offer issued to a selected candidate."""

    def __init__(
        self,
        offer_id: str,
        application_id: str,
        designation: str,
        package_lpa: float,
        offer_date: Union[date, str],
        joining_date: Union[date, str],
        offer_status: str = "OFFERED",
        created_at: Optional[datetime] = None,
        candidate_name: Optional[str] = None,
        company_name: Optional[str] = None,
        job_title: Optional[str] = None,
    ):
        self.offer_id = offer_id
        self.application_id = application_id
        self.designation = designation
        self.package_lpa = package_lpa
        self.offer_date = offer_date
        self.joining_date = joining_date
        self.offer_status = offer_status
        self.created_at = created_at
        self.candidate_name = candidate_name
        self.company_name = company_name
        self.job_title = job_title

    def __str__(self) -> str:
        cand_display = f"{self.candidate_name} ({self.application_id})" if self.candidate_name else self.application_id
        return (
            f"Offer({self.offer_id}, Candidate: {cand_display}, Role: {self.designation}, "
            f"Package: {self.package_lpa} LPA, Status: {self.offer_status})"
        )
