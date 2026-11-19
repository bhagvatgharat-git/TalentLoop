"""Candidate data model."""

from datetime import datetime
from typing import Optional


class Candidate:
    """Represents a student or job seeker profile."""

    def __init__(
        self,
        candidate_id: str,
        name: str,
        email: str,
        mobile: str,
        technology: str,
        percentage: float,
        passing_year: int,
        backlog_count: int = 0,
        is_active: int = 1,
        created_at: Optional[datetime] = None,
    ):
        self.candidate_id = candidate_id
        self.name = name
        self.email = email
        self.mobile = mobile
        self.technology = technology
        self.percentage = percentage
        self.passing_year = passing_year
        self.backlog_count = backlog_count
        self.is_active = is_active
        self.created_at = created_at

    def __str__(self) -> str:
        status_text = "Active" if self.is_active else "Inactive"
        return (
            f"Candidate({self.candidate_id}, {self.name}, {self.technology}, "
            f"{self.percentage}%, Year: {self.passing_year}, Status: {status_text})"
        )

