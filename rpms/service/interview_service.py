"""Interview service handling scheduling, status lifecycle, and candidate evaluations."""

from datetime import date
from typing import List, Optional, Union

from rpms.dao.interview_dao import InterviewDAO
from rpms.exception import RPMSException, ValidationError
from rpms.model.interview import Interview
from rpms.model.interview_feedback import InterviewFeedback
from rpms.model.status import (
    STATUS_INTERVIEW,
    STATUS_REJECTED,
    STATUS_SELECTED,
    STATUS_SHORTLISTED,
)
from rpms.service.application_service import ApplicationService
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import (
    validate_future_date,
    validate_non_empty,
    validate_positive_int,
)


class InterviewService:
    """Coordinates interview rounds, reviewer feedback, and outcome status progression."""

    def __init__(
        self,
        interview_dao: Optional[InterviewDAO] = None,
        application_service: Optional[ApplicationService] = None,
    ):
        self.interview_dao = interview_dao or InterviewDAO()
        self.application_service = application_service or ApplicationService()

    def schedule_interview(
        self,
        application_id: str,
        interview_date: Union[date, str],
        mode: str,
        interviewer: str,
        round_no: Optional[int] = None,
    ) -> Interview:
        """Schedule an interview round and progress candidate application state."""
        clean_app_id = validate_non_empty(application_id, "Application ID").upper()
        application = self.application_service.get_application_by_id(clean_app_id)

        if application.status not in (STATUS_SHORTLISTED, STATUS_INTERVIEW):
            raise ValidationError(
                f"Cannot schedule interview. Application status is '{application.status}'. "
                f"Allowed statuses: ['{STATUS_SHORTLISTED}', '{STATUS_INTERVIEW}']."
            )

        if application.status == STATUS_SHORTLISTED:
            self.application_service.update_status(clean_app_id, STATUS_INTERVIEW)

        existing_rounds = self.interview_dao.find_by_application(clean_app_id)
        if round_no is None:
            clean_round = len(existing_rounds) + 1
        else:
            clean_round = validate_positive_int(round_no, "Round number")

        clean_date = validate_future_date(interview_date, "Interview date")
        clean_mode = validate_non_empty(mode, "Mode").capitalize()
        if clean_mode not in ("Online", "Offline"):
            raise ValidationError("Interview mode must be either 'Online' or 'Offline'.")

        clean_interviewer = validate_non_empty(interviewer, "Interviewer name")
        interview_id = generate_next_id("interviews")

        interview = Interview(
            interview_id=interview_id,
            application_id=clean_app_id,
            round_no=clean_round,
            interview_date=clean_date,
            mode=clean_mode,
            interviewer=clean_interviewer,
            status="SCHEDULED",
        )

        saved = self.interview_dao.add_interview(interview)
        log_activity(f"Interview Scheduled: {interview_id}")
        return self.interview_dao.find_by_id(interview_id) or saved

    def update_interview_status(self, interview_id: str, new_status: str) -> Interview:
        """Update interview session status."""
        clean_id = validate_non_empty(interview_id, "Interview ID").upper()
        clean_status = validate_non_empty(new_status, "Interview status").upper()

        if clean_status not in ("SCHEDULED", "COMPLETED", "CANCELLED"):
            raise ValidationError("Status must be 'SCHEDULED', 'COMPLETED', or 'CANCELLED'.")

        existing = self.interview_dao.find_by_id(clean_id)
        if not existing:
            raise ValidationError(f"Interview with ID '{clean_id}' does not exist.")

        self.interview_dao.update_status(clean_id, clean_status)
        log_activity(f"Interview Status Updated: {clean_id} to {clean_status}")

        updated = self.interview_dao.find_by_id(clean_id)
        if not updated:
            raise RPMSException(f"Failed to retrieve updated interview '{clean_id}'.")
        return updated

    def add_feedback(
        self,
        interview_id: str,
        technical_rating: int,
        communication_rating: int,
        remarks: str,
        result: str,
        is_final_round: bool = False,
    ) -> InterviewFeedback:
        """Record evaluation feedback and trigger status transitions."""
        clean_id = validate_non_empty(interview_id, "Interview ID").upper()
        interview = self.interview_dao.find_by_id(clean_id)
        if not interview:
            raise ValidationError(f"Interview with ID '{clean_id}' does not exist.")

        if interview.status != "COMPLETED":
            raise ValidationError(
                f"Feedback can only be added to COMPLETED interviews. Current status is '{interview.status}'."
            )

        if self.interview_dao.get_feedback_by_interview_id(clean_id):
            raise ValidationError(f"Feedback has already been recorded for interview '{clean_id}'.")

        tech_rating = int(validate_positive_int(technical_rating, "Technical rating"))
        if not (1 <= tech_rating <= 10):
            raise ValidationError("Technical rating must be an integer between 1 and 10.")

        comm_rating = int(validate_positive_int(communication_rating, "Communication rating"))
        if not (1 <= comm_rating <= 10):
            raise ValidationError("Communication rating must be an integer between 1 and 10.")

        clean_remarks = validate_non_empty(remarks, "Remarks")
        clean_result = validate_non_empty(result, "Result").upper()
        if clean_result not in ("PASS", "FAIL"):
            raise ValidationError("Interview result must be 'PASS' or 'FAIL'.")

        feedback_id = generate_next_id("interview_feedback")
        feedback = InterviewFeedback(
            feedback_id=feedback_id,
            interview_id=clean_id,
            technical_rating=tech_rating,
            communication_rating=comm_rating,
            remarks=clean_remarks,
            result=clean_result,
        )

        saved = self.interview_dao.add_feedback(feedback)
        log_activity(f"Interview Feedback Recorded: {feedback_id}")

        if clean_result == "FAIL":
            self.application_service.update_status(interview.application_id, STATUS_REJECTED)
        elif clean_result == "PASS" and is_final_round:
            self.application_service.update_status(interview.application_id, STATUS_SELECTED)

        return saved

    def get_interviews_by_candidate(self, candidate_id: str) -> List[Interview]:
        """Fetch all interviews conducted for a candidate."""
        clean_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        return self.interview_dao.find_by_candidate(clean_id)

    def get_interviews_by_company(self, company_id: str) -> List[Interview]:
        """Fetch all interviews conducted by a company."""
        clean_id = validate_non_empty(company_id, "Company ID").upper()
        return self.interview_dao.find_by_company(clean_id)

