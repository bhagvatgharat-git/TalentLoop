"""Company data model."""

from datetime import datetime
from typing import Optional


class Company:
    """Represents a hiring partner or recruiting organization."""

    def __init__(
        self,
        company_id: str,
        name: str,
        industry: str,
        location: str,
        contact_person: str,
        contact_email: str,
        created_at: Optional[datetime] = None,
    ):
        self.company_id = company_id
        self.name = name
        self.industry = industry
        self.location = location
        self.contact_person = contact_person
        self.contact_email = contact_email
        self.created_at = created_at

    def __str__(self) -> str:
        return f"Company({self.company_id}, {self.name}, {self.industry}, {self.location})"
