"""Placement data model."""

from datetime import date, datetime
from typing import Optional, Union


class Placement:
    """Represents a finalized student placement record."""

    def __init__(
        self,
        placement_id: str,
        application_id: str,
        company_id: str,
        designation: str,
        final_package_lpa: float,
        actual_joining_date: Optional[Union[date, str]] = None,
        joining_status: str = "JOINED",
        created_at: Optional[datetime] = None,
    ):
        self.placement_id = placement_id
        self.application_id = application_id
        self.company_id = company_id
        self.designation = designation
        self.final_package_lpa = final_package_lpa
        self.actual_joining_date = actual_joining_date
        self.joining_status = joining_status
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"Placement({self.placement_id}, App: {self.application_id}, Company: {self.company_id}, "
            f"Role: {self.designation}, Package: {self.final_package_lpa} LPA, Status: {self.joining_status})"
        )
