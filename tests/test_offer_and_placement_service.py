"""Unit tests for OfferService and PlacementService with mocked DAOs and transactions."""

from datetime import date, timedelta
import unittest
from unittest.mock import MagicMock, patch

from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.job_dao import JobDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.dao.placement_dao import PlacementDAO
from rpms.exception import ValidationError
from rpms.model.application import Application
from rpms.model.job import Job
from rpms.model.offer import Offer
from rpms.model.placement import Placement
from rpms.model.status import STATUS_APPLIED, STATUS_OFFERED, STATUS_SELECTED
from rpms.service.offer_service import OfferService
from rpms.service.placement_service import PlacementService


class TestOfferAndPlacementService(unittest.TestCase):
    """Test suite verifying business rules for offer generation and confirmed placements."""

    def setUp(self):
        self.mock_offer_dao = MagicMock(spec=OfferDAO)
        self.mock_placement_dao = MagicMock(spec=PlacementDAO)
        self.mock_app_dao = MagicMock(spec=ApplicationDAO)
        self.mock_job_dao = MagicMock(spec=JobDAO)

        self.offer_service = OfferService(
            offer_dao=self.mock_offer_dao,
            application_dao=self.mock_app_dao,
        )

        self.placement_service = PlacementService(
            placement_dao=self.mock_placement_dao,
            application_dao=self.mock_app_dao,
            offer_dao=self.mock_offer_dao,
            job_dao=self.mock_job_dao,
        )

        self.today = date.today()
        self.joining_date = self.today + timedelta(days=15)

    def test_offer_allowed_only_for_selected_applications(self):
        """Reject offer creation if application is not in SELECTED status."""
        non_selected_app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_APPLIED,
        )
        self.mock_app_dao.find_by_id.return_value = non_selected_app

        with self.assertRaises(ValidationError) as ctx:
            self.offer_service.create_offer(
                application_id="APP501",
                designation="Software Engineer",
                package_lpa=5.5,
                offer_date=self.today,
                joining_date=self.joining_date,
            )
        self.assertIn("SELECTED", str(ctx.exception))

    def test_offer_joining_date_must_be_after_offer_date(self):
        """Reject offer if joining date is on or before offer date."""
        selected_app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_SELECTED,
        )
        self.mock_app_dao.find_by_id.return_value = selected_app
        self.mock_offer_dao.find_by_application.return_value = None
        self.mock_offer_dao.find_by_id.return_value = None

        with self.assertRaises(ValidationError) as ctx:
            self.offer_service.create_offer(
                application_id="APP501",
                designation="Software Engineer",
                package_lpa=5.5,
                offer_date=self.today,
                joining_date=self.today - timedelta(days=1),
            )
        self.assertIn("strictly after", str(ctx.exception))

    @patch("rpms.service.offer_service.get_connection")
    @patch("rpms.service.offer_service.generate_next_id", return_value="OFF105")
    @patch("rpms.service.offer_service.log_activity")
    def test_create_offer_success(self, mock_log, mock_gen_id, mock_get_conn):
        """Issue offer successfully for a SELECTED candidate inside a transaction."""
        selected_app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_SELECTED,
        )
        self.mock_app_dao.find_by_id.return_value = selected_app
        self.mock_offer_dao.find_by_application.return_value = None
        self.mock_offer_dao.find_by_id.return_value = None

        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn

        offer = self.offer_service.create_offer(
            application_id="APP501",
            designation="Software Engineer",
            package_lpa=5.5,
            offer_date=self.today,
            joining_date=self.joining_date,
        )

        self.assertEqual(offer.offer_id, "OFF105")
        self.assertEqual(offer.offer_status, "OFFERED")
        mock_conn.commit.assert_called_once()
        self.mock_app_dao.update_status.assert_called_with(
            "APP501", STATUS_OFFERED, connection=mock_conn
        )

    def test_placement_fails_if_application_not_offered(self):
        """Reject placement if application status is not OFFERED."""
        app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_SELECTED,
        )
        self.mock_app_dao.find_by_id.return_value = app

        with self.assertRaises(ValidationError) as ctx:
            self.placement_service.record_placement("APP501")
        self.assertIn("OFFERED", str(ctx.exception))

    def test_placement_fails_if_offer_not_accepted(self):
        """Reject placement if offer status is not ACCEPTED."""
        app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_OFFERED,
        )
        unaccepted_offer = Offer(
            offer_id="OFF101",
            application_id="APP501",
            designation="Software Engineer",
            package_lpa=5.5,
            offer_date=self.today,
            joining_date=self.joining_date,
            offer_status="OFFERED",
        )
        self.mock_app_dao.find_by_id.return_value = app
        self.mock_offer_dao.find_by_application.return_value = unaccepted_offer

        with self.assertRaises(ValidationError) as ctx:
            self.placement_service.record_placement("APP501")
        self.assertIn("ACCEPTED", str(ctx.exception))

    def test_placement_blocks_duplicate_placement(self):
        """Block duplicate placement for the same application."""
        app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_OFFERED,
        )
        accepted_offer = Offer(
            offer_id="OFF101",
            application_id="APP501",
            designation="Software Engineer",
            package_lpa=5.5,
            offer_date=self.today,
            joining_date=self.joining_date,
            offer_status="ACCEPTED",
        )
        existing_placement = Placement(
            placement_id="PLC101",
            application_id="APP501",
            company_id="COM101",
            designation="Software Engineer",
            final_package_lpa=5.5,
            actual_joining_date=self.joining_date,
        )
        self.mock_app_dao.find_by_id.return_value = app
        self.mock_offer_dao.find_by_application.return_value = accepted_offer
        self.mock_placement_dao.find_by_application.return_value = existing_placement

        with self.assertRaises(ValidationError) as ctx:
            self.placement_service.record_placement("APP501")
        self.assertIn("already exists", str(ctx.exception))

    @patch("rpms.service.placement_service.get_connection")
    @patch("rpms.service.placement_service.generate_next_id", return_value="PLC105")
    @patch("rpms.service.placement_service.log_activity")
    def test_record_placement_success_and_decrements_openings(
        self, mock_log, mock_gen_id, mock_get_conn
    ):
        """Record placement, transition app to JOINED, and decrement vacancies."""
        app = Application(
            application_id="APP501",
            candidate_id="CAN1001",
            job_id="JOB101",
            applied_date=self.today,
            status=STATUS_OFFERED,
        )
        accepted_offer = Offer(
            offer_id="OFF101",
            application_id="APP501",
            designation="Software Engineer",
            package_lpa=5.5,
            offer_date=self.today,
            joining_date=self.joining_date,
            offer_status="ACCEPTED",
        )
        job = Job(
            job_id="JOB101",
            company_id="COM101",
            job_title="Software Engineer",
            technology="Java",
            openings=2,
            location="Pune",
            package_lpa=5.5,
            deadline=self.today + timedelta(days=30),
        )

        self.mock_app_dao.find_by_id.return_value = app
        self.mock_offer_dao.find_by_application.return_value = accepted_offer
        self.mock_placement_dao.find_by_application.return_value = None
        self.mock_placement_dao.find_by_id.return_value = None
        self.mock_job_dao.find_by_id.return_value = job
        self.mock_job_dao.decrement_openings.return_value = 1

        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn

        placement = self.placement_service.record_placement("APP501")

        self.assertEqual(placement.placement_id, "PLC105")
        mock_conn.commit.assert_called_once()
        self.mock_job_dao.decrement_openings.assert_called_with("JOB101", connection=mock_conn)
        self.mock_app_dao.update_status.assert_called_with(
            "APP501", "JOINED", connection=mock_conn
        )


if __name__ == "__main__":
    unittest.main()
