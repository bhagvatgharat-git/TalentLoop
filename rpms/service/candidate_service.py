"""Candidate service handling business logic and input validation."""

from typing import List, Optional

from rpms.dao.candidate_dao import CandidateDAO
from rpms.exception import CandidateNotFoundError, ValidationError
from rpms.model.candidate import Candidate
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import (
    validate_email,
    validate_mobile,
    validate_non_empty,
    validate_non_negative_int,
    validate_percentage,
    validate_positive_int,
)


class CandidateService:
    """Provides business logic for candidate registration, updates, and searches."""

    def __init__(self, candidate_dao: Optional[CandidateDAO] = None):
        self.candidate_dao = candidate_dao or CandidateDAO()

    def create_candidate(
        self,
        name: str,
        email: str,
        mobile: str,
        technology: str,
        percentage: float,
        passing_year: int,
        backlog_count: int = 0,
    ) -> Candidate:
        """Validate input, generate ID, ensure uniqueness, and register candidate."""
        clean_name = validate_non_empty(name, "Candidate name")
        clean_email = validate_email(email)
        clean_mobile = validate_mobile(mobile)
        clean_tech = validate_non_empty(technology, "Technology")
        clean_percentage = validate_percentage(percentage)
        clean_year = validate_positive_int(passing_year, "Passing year")
        clean_backlogs = validate_non_negative_int(backlog_count, "Backlog count")

        if self.candidate_dao.find_by_email(clean_email):
            raise ValidationError(f"A candidate with email '{clean_email}' already exists.")

        if self.candidate_dao.find_by_mobile(clean_mobile):
            raise ValidationError(f"A candidate with mobile '{clean_mobile}' already exists.")

        candidate_id = generate_next_id("candidates")
        candidate = Candidate(
            candidate_id=candidate_id,
            name=clean_name,
            email=clean_email,
            mobile=clean_mobile,
            technology=clean_tech,
            percentage=clean_percentage,
            passing_year=clean_year,
            backlog_count=clean_backlogs,
            is_active=1,
        )

        saved = self.candidate_dao.add(candidate)
        log_activity(f"Candidate Created: {candidate_id}")
        return saved

    def update_candidate(
        self,
        candidate_id: str,
        name: str,
        email: str,
        mobile: str,
        technology: str,
        percentage: float,
        passing_year: int,
        backlog_count: int,
        is_active: int = 1,
    ) -> Candidate:
        """Validate input, verify existence, check uniqueness, and update candidate."""
        clean_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        existing = self.candidate_dao.find_by_id(clean_id)
        if not existing:
            raise CandidateNotFoundError(f"Candidate with ID '{clean_id}' does not exist.")

        clean_name = validate_non_empty(name, "Candidate name")
        clean_email = validate_email(email)
        clean_mobile = validate_mobile(mobile)
        clean_tech = validate_non_empty(technology, "Technology")
        clean_percentage = validate_percentage(percentage)
        clean_year = validate_positive_int(passing_year, "Passing year")
        clean_backlogs = validate_non_negative_int(backlog_count, "Backlog count")
        clean_active = 1 if int(is_active) else 0

        existing_by_email = self.candidate_dao.find_by_email(clean_email)
        if existing_by_email and existing_by_email.candidate_id != clean_id:
            raise ValidationError(f"Email '{clean_email}' is already in use by another candidate.")

        existing_by_mobile = self.candidate_dao.find_by_mobile(clean_mobile)
        if existing_by_mobile and existing_by_mobile.candidate_id != clean_id:
            raise ValidationError(f"Mobile '{clean_mobile}' is already in use by another candidate.")

        updated_candidate = Candidate(
            candidate_id=clean_id,
            name=clean_name,
            email=clean_email,
            mobile=clean_mobile,
            technology=clean_tech,
            percentage=clean_percentage,
            passing_year=clean_year,
            backlog_count=clean_backlogs,
            is_active=clean_active,
        )

        self.candidate_dao.update(updated_candidate)
        log_activity(f"Candidate Updated: {clean_id}")
        return updated_candidate

    def get_candidate_by_id(self, candidate_id: str) -> Candidate:
        """Fetch candidate by primary key or raise CandidateNotFoundError."""
        clean_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        candidate = self.candidate_dao.find_by_id(clean_id)
        if not candidate:
            raise CandidateNotFoundError(f"Candidate with ID '{clean_id}' does not exist.")
        return candidate

    def search_candidates(self, query: str) -> List[Candidate]:
        """Search candidates by name or technology."""
        clean_query = validate_non_empty(query, "Search query")
        return self.candidate_dao.search(clean_query)

    def get_all_candidates(self, active_only: bool = True) -> List[Candidate]:
        """Return list of candidates."""
        return self.candidate_dao.get_all(active_only=active_only)

    def deactivate_candidate(self, candidate_id: str) -> bool:
        """Deactivate candidate record and log the event."""
        clean_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        candidate = self.candidate_dao.find_by_id(clean_id)
        if not candidate:
            raise CandidateNotFoundError(f"Candidate with ID '{clean_id}' does not exist.")

        success = self.candidate_dao.deactivate(clean_id)
        if success:
            log_activity(f"Candidate Deactivated: {clean_id}")
        return success

