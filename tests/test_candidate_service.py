"""Unit tests for CandidateService with mocked DAO."""

import unittest
from unittest.mock import MagicMock, patch

from rpms.dao.candidate_dao import CandidateDAO
from rpms.exception import ValidationError
from rpms.model.candidate import Candidate
from rpms.service.candidate_service import CandidateService


class TestCandidateService(unittest.TestCase):
    """Test suite for candidate validation and registration logic."""

    def setUp(self):
        self.mock_dao = MagicMock(spec=CandidateDAO)
        self.service = CandidateService(candidate_dao=self.mock_dao)

    def test_duplicate_email_rejected(self):
        """Block registration when the candidate email is already in the database."""
        existing = Candidate(
            candidate_id="CAN1001",
            name="Aarav Sharma",
            email="aarav.sharma@gmail.com",
            mobile="9820011001",
            technology="Java",
            percentage=78.5,
            passing_year=2024,
        )
        self.mock_dao.find_by_email.return_value = existing

        with self.assertRaises(ValidationError) as ctx:
            self.service.create_candidate(
                name="Aarav Sharma",
                email="aarav.sharma@gmail.com",
                mobile="9820011002",
                technology="Java",
                percentage=80.0,
                passing_year=2024,
                backlog_count=0,
            )
        self.assertIn("already exists", str(ctx.exception))

    def test_duplicate_mobile_rejected(self):
        """Block registration when the candidate mobile is already in the database."""
        self.mock_dao.find_by_email.return_value = None
        existing = Candidate(
            candidate_id="CAN1001",
            name="Aarav Sharma",
            email="aarav.sharma@gmail.com",
            mobile="9820011001",
            technology="Java",
            percentage=78.5,
            passing_year=2024,
        )
        self.mock_dao.find_by_mobile.return_value = existing

        with self.assertRaises(ValidationError) as ctx:
            self.service.create_candidate(
                name="Priya Patel",
                email="priya.patel@gmail.com",
                mobile="9820011001",
                technology="Python",
                percentage=82.0,
                passing_year=2024,
                backlog_count=0,
            )
        self.assertIn("already exists", str(ctx.exception))

    def test_percentage_below_zero_rejected(self):
        """Reject percentage values less than 0."""
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_candidate(
                name="Rohan Deshmukh",
                email="rohan.deshmukh@gmail.com",
                mobile="9820011003",
                technology="Java",
                percentage=-5.0,
                passing_year=2024,
                backlog_count=0,
            )
        self.assertIn("between 0.0 and 100.0", str(ctx.exception))

    def test_percentage_above_hundred_rejected(self):
        """Reject percentage values greater than 100."""
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_candidate(
                name="Sneha Kulkarni",
                email="sneha.kulkarni@gmail.com",
                mobile="9820011004",
                technology="React",
                percentage=105.0,
                passing_year=2024,
                backlog_count=0,
            )
        self.assertIn("between 0.0 and 100.0", str(ctx.exception))

    def test_negative_backlog_rejected(self):
        """Reject backlog counts less than 0."""
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_candidate(
                name="Aditya Verma",
                email="aditya.verma@gmail.com",
                mobile="9820011005",
                technology="Python",
                percentage=75.0,
                passing_year=2024,
                backlog_count=-1,
            )
        self.assertIn("non-negative integer", str(ctx.exception))

    @patch("rpms.service.candidate_service.generate_next_id", return_value="CAN1015")
    @patch("rpms.service.candidate_service.log_activity")
    def test_create_candidate_success(self, mock_log, mock_gen_id):
        """Register candidate successfully with valid input."""
        self.mock_dao.find_by_email.return_value = None
        self.mock_dao.find_by_mobile.return_value = None
        self.mock_dao.add.side_effect = lambda cand: cand

        candidate = self.service.create_candidate(
            name="Neha Joshi",
            email="neha.joshi@gmail.com",
            mobile="9820011006",
            technology="Data Science",
            percentage=88.5,
            passing_year=2024,
            backlog_count=0,
        )

        self.assertEqual(candidate.candidate_id, "CAN1015")
        self.assertEqual(candidate.name, "Neha Joshi")
        self.assertEqual(candidate.percentage, 88.5)
        self.mock_dao.add.assert_called_once()
        mock_log.assert_called_with("Candidate Created: CAN1015")


if __name__ == "__main__":
    unittest.main()

