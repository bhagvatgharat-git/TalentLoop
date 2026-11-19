"""Application service handling workflow, status transitions, and recruitment lifecycle."""

from datetime import date
from typing import List, Optional

from rpms.dao.application_dao import ApplicationDAO
from rpms.exception import (
    CandidateNotEligibleError,
    DuplicateApplicationError,
    InvalidStatusTransitionError,
    RPMSException,
    ValidationError,
)
from rpms.model.application import Application
from rpms.model.status import (
    ALLOWED_TRANSITIONS,
    STATUS_APPLIED,
    STATUS_INTERVIEW,
    STATUS_JOINED,
    STATUS_OFFERED,
    STATUS_REJECTED,
    STATUS_SELECTED,
    STATUS_SHORTLISTED,
    is_valid_transition,
)
from rpms.service.eligibility_service import EligibilityResult, EligibilityService
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import validate_non_empty

STATUS_LOG_ACTIONS = {
    STATUS_SHORTLISTED: "Candidate Shortlisted",
    STATUS_INTERVIEW: "Candidate Interview Stage",
    STATUS_SELECTED: "Candidate Selected",
    STATUS_OFFERED: "Candidate Offered",
    STATUS_JOINED: "Candidate Joined",
    STATUS_REJECTED: "Candidate Rejected",
}


class ApplicationService:
    """Manages candidate application submissions and recruitment stage transitions."""

    def __init__(
        self,
        application_dao: Optional[ApplicationDAO] = None,
        eligibility_service: Optional[EligibilityService] = None,
    ):
        self.application_dao = application_dao or ApplicationDAO()
        self.eligibility_service = eligibility_service or EligibilityService(
            application_dao=self.application_dao
        )

    def check_eligibility(self, candidate_id: str, job_id: str) -> EligibilityResult:
        """Evaluate candidate eligibility for a job opening."""
        return self.eligibility_service.check_by_ids(candidate_id, job_id)

    def apply(self, candidate_id: str, job_id: str) -> Application:
        """Run eligibility checks and submit a candidate job application."""
        clean_cand_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        clean_job_id = validate_non_empty(job_id, "Job ID").upper()

        result = self.eligibility_service.check_by_ids(clean_cand_id, clean_job_id)
        if not result.is_eligible:
            if result.rule_failed == 4:
                raise DuplicateApplicationError(result.reason)
            raise CandidateNotEligibleError(result.reason)

        app_id = generate_next_id("applications")
        today = date.today()
        application = Application(
            application_id=app_id,
            candidate_id=clean_cand_id,
            job_id=clean_job_id,
            applied_date=today,
            status=STATUS_APPLIED,
        )

        saved = self.application_dao.add(application)
        log_activity(f"Candidate Applied: {app_id}")
        return self.application_dao.find_by_id(app_id) or saved

    def update_status(self, application_id: str, new_status: str) -> Application:
        """Validate status transition rules and update application state."""
        clean_app_id = validate_non_empty(application_id, "Application ID").upper()
        clean_status = validate_non_empty(new_status, "New status").upper()

        existing = self.application_dao.find_by_id(clean_app_id)
        if not existing:
            raise RPMSException(f"Application with ID '{clean_app_id}' does not exist.")

        if not is_valid_transition(existing.status, clean_status):
            allowed = ALLOWED_TRANSITIONS.get(existing.status, [])
            allowed_desc = ", ".join(allowed) if allowed else "None"
            raise InvalidStatusTransitionError(
                f"Cannot transition application '{clean_app_id}' from '{existing.status}' "
                f"to '{clean_status}'. Allowed next statuses: [{allowed_desc}]."
            )

        self.application_dao.update_status(clean_app_id, clean_status)

        action_desc = STATUS_LOG_ACTIONS.get(
            clean_status, f"Candidate Status Updated to {clean_status}"
        )
        log_activity(f"{action_desc}: {clean_app_id}")

        updated = self.application_dao.find_by_id(clean_app_id)
        if not updated:
            raise RPMSException(f"Failed to retrieve updated application '{clean_app_id}'.")
        return updated

    def shortlist(self, application_id: str) -> Application:
        """Transition an application to SHORTLISTED."""
        return self.update_status(application_id, STATUS_SHORTLISTED)

    def reject(self, application_id: str) -> Application:
        """Transition an application to REJECTED."""
        return self.update_status(application_id, STATUS_REJECTED)

    def get_application_by_id(self, application_id: str) -> Application:
        """Fetch application details by ID."""
        clean_id = validate_non_empty(application_id, "Application ID").upper()
        app = self.application_dao.find_by_id(clean_id)
        if not app:
            raise RPMSException(f"Application with ID '{clean_id}' does not exist.")
        return app

    def get_applications_by_job(self, job_id: str) -> List[Application]:
        """Fetch all applications submitted for a job opening."""
        clean_id = validate_non_empty(job_id, "Job ID").upper()
        return self.application_dao.find_by_job(clean_id)

    def get_applications_by_candidate(self, candidate_id: str) -> List[Application]:
        """Fetch all applications submitted by a candidate."""
        clean_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        return self.application_dao.find_by_candidate(clean_id)

    def get_applications_by_status(self, status: str) -> List[Application]:
        """Fetch all applications in a specific status."""
        clean_status = validate_non_empty(status, "Status").upper()
        return self.application_dao.find_by_status(clean_status)

    def get_all_applications(self) -> List[Application]:
        """Fetch all applications."""
        return self.application_dao.get_all()
