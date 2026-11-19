"""Interview feedback data model."""

from datetime import datetime
from typing import Optional


class InterviewFeedback:
    """Represents candidate evaluation scores and remarks for an interview round."""

    def __init__(
        self,
        feedback_id: str,
        interview_id: str,
        technical_rating: int,
        communication_rating: int,
        remarks: str,
        result: str,
        created_at: Optional[datetime] = None,
    ):
        self.feedback_id = feedback_id
        self.interview_id = interview_id
        self.technical_rating = technical_rating
        self.communication_rating = communication_rating
        self.remarks = remarks
        self.result = result
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"InterviewFeedback({self.feedback_id}, Interview: {self.interview_id}, "
            f"Tech: {self.technical_rating}/10, Comm: {self.communication_rating}/10, "
            f"Result: {self.result})"
        )
