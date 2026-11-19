"""Placement service handling confirmation, joining records, and vacancy adjustments."""

from datetime import date
from typing import List, Optional, Union

from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.job_dao import JobDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.dao.placement_dao import PlacementDAO
from rpms.exception import RPMSException, ValidationError
from rpms.model.placement import Placement
from rpms.model.status import STATUS_JOINED, STATUS_OFFERED
from rpms.util.db_connection import get_connection
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import validate_date, validate_non_empty


class PlacementService:
    """Manages finalized placements, joins, and automated vacancy decrementing."""

    def __init__(
        self,
        placement_dao: Optional[PlacementDAO] = None,
        application_dao: Optional[ApplicationDAO] = None,
        offer_dao: Optional[OfferDAO] = None,
        job_dao: Optional[JobDAO] = None,
    ):
        self.placement_dao = placement_dao or PlacementDAO()
        self.application_dao = application_dao or ApplicationDAO()
        self.offer_dao = offer_dao or OfferDAO()
        self.job_dao = job_dao or JobDAO()

    def record_placement(
        self,
        application_id: str,
        designation: Optional[str] = None,
        final_package_lpa: Optional[Union[float, int, str]] = None,
        actual_joining_date: Optional[Union[date, str]] = None,
        joining_status: str = "JOINED",
    ) -> Placement:
        """Confirm placement, update application to JOINED, and decrement openings in a transaction."""
        clean_app_id = validate_non_empty(application_id, "Application ID").upper()
        application = self.application_dao.find_by_id(clean_app_id)
        if not application:
            raise RPMSException(f"Application with ID '{clean_app_id}' does not exist.")

        if application.status != STATUS_OFFERED:
            raise ValidationError(
                f"Placement can only be recorded for applications in OFFERED status. "
                f"Current status is '{application.status}'."
            )

        offer = self.offer_dao.find_by_application(clean_app_id)
        if not offer or offer.offer_status != "ACCEPTED":
            raise ValidationError("Placement requires an accepted offer (status 'ACCEPTED').")

        if self.placement_dao.find_by_application(clean_app_id):
            raise ValidationError(f"A placement record already exists for application '{clean_app_id}'.")

        job = self.job_dao.find_by_id(application.job_id)
        if not job:
            raise RPMSException(f"Associated job '{application.job_id}' does not exist.")

        resolved_designation = validate_non_empty(
            designation if designation else offer.designation, "Designation"
        )

        raw_package = final_package_lpa if final_package_lpa is not None else offer.package_lpa
        try:
            pkg_val = float(raw_package)
            if pkg_val < 0.0:
                raise ValueError
        except (TypeError, ValueError) as exc:
            raise ValidationError("Final package (LPA) must be a non-negative numeric value.") from exc

        raw_date = actual_joining_date if actual_joining_date else offer.joining_date
        parsed_joining_date = validate_date(raw_date, "Actual joining date")

        clean_joining_status = validate_non_empty(joining_status, "Joining status").upper()
        if clean_joining_status not in ("JOINED", "NOT_JOINED"):
            raise ValidationError("Joining status must be either 'JOINED' or 'NOT_JOINED'.")

        conn = get_connection()
        conn.autocommit = False
        try:
            placement_id = generate_next_id("placements", connection=conn)
            placement = Placement(
                placement_id=placement_id,
                application_id=clean_app_id,
                company_id=job.company_id,
                designation=resolved_designation,
                final_package_lpa=round(pkg_val, 2),
                actual_joining_date=parsed_joining_date,
                joining_status=clean_joining_status,
            )
            self.placement_dao.add(placement, connection=conn)
            self.application_dao.update_status(clean_app_id, STATUS_JOINED, connection=conn)
            remaining_openings = self.job_dao.decrement_openings(job.job_id, connection=conn)
            conn.commit()

            log_activity(f"Placement Recorded: {placement_id}")
            log_activity(f"Candidate Joined: {clean_app_id}")
            if remaining_openings <= 0:
                log_activity(f"Job Closed Automatically: {job.job_id}")

            return self.placement_dao.find_by_id(placement_id) or placement
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_placement_by_id(self, placement_id: str) -> Placement:
        """Fetch placement details by ID."""
        clean_id = validate_non_empty(placement_id, "Placement ID").upper()
        placement = self.placement_dao.find_by_id(clean_id)
        if not placement:
            raise ValidationError(f"Placement with ID '{clean_id}' does not exist.")
        return placement

    def get_all_placements(self) -> List[Placement]:
        """Fetch all confirmed placements."""
        return self.placement_dao.get_all()

    def get_placements_by_company(self, company_id: str) -> List[Placement]:
        """Fetch placements for a company."""
        clean_id = validate_non_empty(company_id, "Company ID").upper()
        return self.placement_dao.get_by_company(clean_id)

