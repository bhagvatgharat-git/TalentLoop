"""Unit tests for EligibilityService and ApplicationService with mocked DAOs."""

from datetime import date, timedelta
import unittest
from unittest.mock import MagicMock, patch

from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception import (
    CandidateNotEligibleError,
    DuplicateApplicationError,
    InvalidStatusTransitionError,
)
from rpms.model.application import Application
from rpms.model.candidate import Candidate
from rpms.model.job import Job
from rpms.model.status import (
    STATUS_APPLIED,
    STATUS_INTERVIEW,
    STATUS_JOINED,
    STATUS_OFFERED,
    STATUS_REJECTED,
    STATUS_SELECTED,
    STATUS_SHORTLISTED,
    is_valid_transition,
)
from rpms.service.application_service import ApplicationService
from rpms.service.eligibility_service import EligibilityService


class TestEligibilityAndApplication(unittest.TestCase):
    """Test suite covering 7 eligibility rules, workflow transitions, and application lifecycle."""

    def setUp(self):
        self.mock_app_dao = MagicMock(spec=ApplicationDAO)
        self.mock_cand_dao = MagicMock(spec=CandidateDAO)
        self.mock_job_dao = MagicMock(spec=JobDAO)

        self.eligibility_service = EligibilityService(
            application_dao=self.mock_app_dao,
            candidate_dao=self.mock_cand_dao,
            job_dao=self.mock_job_dao,
        )

        self.app_service = ApplicationService(
            application_dao=self.mock_app_dao,
            eligibility_service=self.eligibility_service,
        )

        self.future_date = date.today() + timedelta(days=30)
        self.past_date = date.today() - timedelta(days=5)

        self.valid_candidate = Candidate(
            candidate_id="CAN1001",
            name="Aarav Sharma",
            email="aarav.sharma@gmail.com",
            mobile="9820011001",
            technology="Java",
            percentage=78.5,
            passing_year=2024,
            backlog_count=0,
            is_active=1,
        )

        self.valid_job = Job(
            job_id="JOB101",
            company_id="COM101",
            job_title="Java Backend Developer",
            technology="Java",
            openings=5,
            location="Pune",
            package_lpa=4.5,
            min_percentage=65.0,
            passing_year=2024,
            max_backlogs=0,
            deadline=self.future_date,
            status="OPEN",
        )

    def test_rule_1_inactive_candidate_fails(self):
        """Rule 1: Inactive candidate fails eligibility."""
        self.valid_candidate.is_active = 0
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 1)
        self.assertIn("inactive", result.reason.lower())

    def test_rule_2_closed_job_fails(self):
        """Rule 2: Closed job vacancy fails eligibility."""
        self.valid_job.status = "CLOSED"
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 2)
        self.assertIn("closed", result.reason.lower())

    def test_rule_3_expired_deadline_fails(self):
        """Rule 3: Past deadline fails eligibility."""
        self.valid_job.deadline = self.past_date
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 3)
        self.assertIn("passed", result.reason.lower())

    def test_rule_4_already_applied_fails(self):
        """Rule 4: Candidate who has already applied fails eligibility."""
        existing_app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=date.today(),
        )
        self.mock_app_dao.find_by_candidate_and_job.return_value = existing_app

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 4)
        self.assertIn("already applied", result.reason.lower())

    def test_rule_5_low_percentage_fails(self):
        """Rule 5: Candidate percentage below job minimum fails eligibility."""
        self.valid_candidate.percentage = 60.0
        self.valid_job.min_percentage = 65.0
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 5)
        self.assertIn("below required minimum", result.reason)

    def test_rule_6_passing_year_mismatch_fails(self):
        """Rule 6: Passing year mismatch fails eligibility."""
        self.valid_candidate.passing_year = 2023
        self.valid_job.passing_year = 2024
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 6)
        self.assertIn("does not match required year", result.reason)

    def test_rule_7_excess_backlogs_fails(self):
        """Rule 7: Candidate backlogs exceeding maximum fails eligibility."""
        self.valid_candidate.backlog_count = 2
        self.valid_job.max_backlogs = 0
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertFalse(result.is_eligible)
        self.assertEqual(result.rule_failed, 7)
        self.assertIn("exceeds allowed maximum", result.reason)

    def test_all_rules_pass_eligible(self):
        """All rules satisfied evaluates to ELIGIBLE."""
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        result = self.eligibility_service.evaluate(self.valid_candidate, self.valid_job)
        self.assertTrue(result.is_eligible)
        self.assertEqual(result.status, "ELIGIBLE")
        self.assertIsNone(result.rule_failed)

    def test_apply_raises_duplicate_application_error(self):
        """Applying when already applied raises DuplicateApplicationError."""
        self.mock_cand_dao.find_by_id.return_value = self.valid_candidate
        self.mock_job_dao.find_by_id.return_value = self.valid_job
        existing_app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=date.today(),
        )
        self.mock_app_dao.find_by_candidate_and_job.return_value = existing_app

        with self.assertRaises(DuplicateApplicationError):
            self.app_service.apply("CAN1001", "JOB101")

    def test_apply_raises_candidate_not_eligible_error(self):
        """Applying with low percentage raises CandidateNotEligibleError."""
        self.valid_candidate.percentage = 55.0
        self.mock_cand_dao.find_by_id.return_value = self.valid_candidate
        self.mock_job_dao.find_by_id.return_value = self.valid_job
        self.mock_app_dao.find_by_candidate_and_job.return_value = None

        with self.assertRaises(CandidateNotEligibleError):
            self.app_service.apply("CAN1001", "JOB101")

    def test_valid_workflow_transitions(self):
        """Verify sequential permitted transitions."""
        self.assertTrue(is_valid_transition(STATUS_APPLIED, STATUS_SHORTLISTED))
        self.assertTrue(is_valid_transition(STATUS_SHORTLISTED, STATUS_INTERVIEW))
        self.assertTrue(is_valid_transition(STATUS_INTERVIEW, STATUS_SELECTED))
        self.assertTrue(is_valid_transition(STATUS_SELECTED, STATUS_OFFERED))
        self.assertTrue(is_valid_transition(STATUS_OFFERED, STATUS_JOINED))
        self.assertTrue(is_valid_transition(STATUS_APPLIED, STATUS_REJECTED))
        self.assertTrue(is_valid_transition(STATUS_INTERVIEW, STATUS_REJECTED))

    def test_invalid_workflow_transition_applied_to_joined_fails(self):
        """Direct transition from APPLIED to JOINED must be rejected."""
        self.assertFalse(is_valid_transition(STATUS_APPLIED, STATUS_JOINED))

        existing = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=date.today(),
            status=STATUS_APPLIED,
        )
        self.mock_app_dao.find_by_id.return_value = existing

        with self.assertRaises(InvalidStatusTransitionError) as ctx:
            self.app_service.update_status("APP501", STATUS_JOINED)
        self.assertIn("Cannot transition", str(ctx.exception))
        self.assertIn("APPLIED", str(ctx.exception))
        self.assertIn("JOINED", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
