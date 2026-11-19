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
    ):
        self.offer_id = offer_id
        self.application_id = application_id
        self.designation = designation
        self.package_lpa = package_lpa
        self.offer_date = offer_date
        self.joining_date = joining_date
        self.offer_status = offer_status
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"Offer({self.offer_id}, App: {self.application_id}, Role: {self.designation}, "
            f"Package: {self.package_lpa} LPA, Status: {self.offer_status})"
        )

