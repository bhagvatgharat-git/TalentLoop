"""Interview session data model."""

from datetime import date, datetime
from typing import Optional, Union


class Interview:
    """Represents a scheduled or completed interview round."""

    def __init__(
        self,
        interview_id: str,
        application_id: str,
        round_no: int,
        interview_date: Union[date, str],
        mode: str,
        interviewer: str,
        status: str = "SCHEDULED",
        created_at: Optional[datetime] = None,
    ):
        self.interview_id = interview_id
        self.application_id = application_id
        self.round_no = round_no
        self.interview_date = interview_date
        self.mode = mode
        self.interviewer = interviewer
        self.status = status
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"Interview({self.interview_id}, App: {self.application_id}, "
            f"Round: {self.round_no}, Mode: {self.mode}, Status: {self.status})"
        )
