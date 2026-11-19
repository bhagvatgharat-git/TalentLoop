"""Eligibility verification service for job applications."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception import CandidateNotFoundError, JobNotFoundError
from rpms.model.candidate import Candidate
from rpms.model.job import Job
from rpms.util.validators import validate_non_empty


@dataclass
class EligibilityResult:
    """Represents the outcome of a candidate job eligibility evaluation."""

    is_eligible: bool
    status: str
    reason: str
    rule_failed: Optional[int] = None


class EligibilityService:
    """Evaluates whether a candidate qualifies for a job posting."""

    def __init__(
        self,
        application_dao: Optional[ApplicationDAO] = None,
        candidate_dao: Optional[CandidateDAO] = None,
        job_dao: Optional[JobDAO] = None,
    ):
        self.application_dao = application_dao or ApplicationDAO()
        self.candidate_dao = candidate_dao or CandidateDAO()
        self.job_dao = job_dao or JobDAO()

    def evaluate(self, candidate: Candidate, job: Job) -> EligibilityResult:
        """Evaluate candidate eligibility rules in strict sequential order."""
        # 1. Candidate is active
        if not candidate.is_active:
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=f"Candidate '{candidate.candidate_id}' is inactive.",
                rule_failed=1,
            )

        # 2. Job is open
        if job.status.upper() != "OPEN":
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=f"Job opening '{job.job_id}' is closed.",
                rule_failed=2,
            )

        # 3. Deadline has not passed
        deadline_date = (
            datetime.strptime(str(job.deadline), "%Y-%m-%d").date()
            if isinstance(job.deadline, str)
            else job.deadline
        )
        if deadline_date and deadline_date < date.today():
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=f"Job application deadline ({deadline_date}) has passed.",
                rule_failed=3,
            )

        # 4. Candidate has not already applied to this job
        existing = self.application_dao.find_by_candidate_and_job(
            candidate.candidate_id, job.job_id
        )
        if existing:
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=f"Candidate '{candidate.candidate_id}' has already applied for job '{job.job_id}'.",
                rule_failed=4,
            )

        # 5. Candidate percentage >= job minimum percentage
        if candidate.percentage < job.min_percentage:
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=(
                    f"Candidate percentage ({candidate.percentage:.2f}%) is below "
                    f"required minimum ({job.min_percentage:.2f}%)."
                ),
                rule_failed=5,
            )

        # 6. Candidate passing year matches the job's passing year
        if int(candidate.passing_year) != int(job.passing_year):
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=(
                    f"Candidate passing year ({candidate.passing_year}) does not "
                    f"match required year ({job.passing_year})."
                ),
                rule_failed=6,
            )

        # 7. Candidate backlogs <= job maximum backlogs
        if int(candidate.backlog_count) > int(job.max_backlogs):
            return EligibilityResult(
                is_eligible=False,
                status="NOT ELIGIBLE",
                reason=(
                    f"Candidate backlog count ({candidate.backlog_count}) exceeds "
                    f"allowed maximum ({job.max_backlogs})."
                ),
                rule_failed=7,
            )

        return EligibilityResult(
            is_eligible=True,
            status="ELIGIBLE",
            reason="Candidate meets all eligibility criteria.",
            rule_failed=None,
        )

    def check_by_ids(self, candidate_id: str, job_id: str) -> EligibilityResult:
        """Fetch candidate and job entities by ID, then run eligibility rules."""
        clean_cand_id = validate_non_empty(candidate_id, "Candidate ID").upper()
        clean_job_id = validate_non_empty(job_id, "Job ID").upper()

        candidate = self.candidate_dao.find_by_id(clean_cand_id)
        if not candidate:
            raise CandidateNotFoundError(f"Candidate with ID '{clean_cand_id}' does not exist.")

        job = self.job_dao.find_by_id(clean_job_id)
        if not job:
            raise JobNotFoundError(f"Job opening with ID '{clean_job_id}' does not exist.")

        return self.evaluate(candidate, job)
