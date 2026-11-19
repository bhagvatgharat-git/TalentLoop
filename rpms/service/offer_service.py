"""Offer service handling offer letter issuance, updates, and status sync."""

from datetime import date
from typing import List, Optional, Union

from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.exception import RPMSException, ValidationError
from rpms.model.offer import Offer
from rpms.model.status import STATUS_OFFERED, STATUS_REJECTED, STATUS_SELECTED
from rpms.util.db_connection import get_connection
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import validate_date, validate_non_empty


class OfferService:
    """Provides business logic for creating and managing formal job offers."""

    def __init__(
        self,
        offer_dao: Optional[OfferDAO] = None,
        application_dao: Optional[ApplicationDAO] = None,
    ):
        self.offer_dao = offer_dao or OfferDAO()
        self.application_dao = application_dao or ApplicationDAO()

    def create_offer(
        self,
        application_id: str,
        designation: str,
        package_lpa: Union[float, int, str],
        offer_date: Union[date, str],
        joining_date: Union[date, str],
    ) -> Offer:
        """Issue an offer letter for a SELECTED candidate inside a single transaction."""
        clean_app_id = validate_non_empty(application_id, "Application ID").upper()
        application = self.application_dao.find_by_id(clean_app_id)
        if not application:
            raise RPMSException(f"Application with ID '{clean_app_id}' does not exist.")

        if application.status != STATUS_SELECTED:
            raise ValidationError(
                f"Offer can only be created for applications in SELECTED status. "
                f"Current status is '{application.status}'."
            )

        if self.offer_dao.find_by_application(clean_app_id):
            raise ValidationError(f"An offer has already been issued for application '{clean_app_id}'.")

        clean_desig = validate_non_empty(designation, "Designation")

        try:
            pkg_val = float(package_lpa)
            if pkg_val < 0.0:
                raise ValueError
        except (TypeError, ValueError) as exc:
            raise ValidationError("Package (LPA) must be a non-negative numeric value.") from exc

        parsed_offer_date = validate_date(offer_date, "Offer date")
        parsed_joining_date = validate_date(joining_date, "Joining date")

        if parsed_joining_date <= parsed_offer_date:
            raise ValidationError("Joining date must be strictly after the offer date.")

        conn = get_connection()
        conn.autocommit = False
        try:
            offer_id = generate_next_id("offers", connection=conn)
            offer = Offer(
                offer_id=offer_id,
                application_id=clean_app_id,
                designation=clean_desig,
                package_lpa=round(pkg_val, 2),
                offer_date=parsed_offer_date,
                joining_date=parsed_joining_date,
                offer_status="OFFERED",
            )
            self.offer_dao.add(offer, connection=conn)
            self.application_dao.update_status(clean_app_id, STATUS_OFFERED, connection=conn)
            conn.commit()

            log_activity(f"Offer Issued: {offer_id}")
            log_activity(f"Candidate Offered: {clean_app_id}")
            return self.offer_dao.find_by_id(offer_id) or offer
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update_offer_status(self, offer_id: str, new_status: str) -> Offer:
        """Update offer response (ACCEPTED / DECLINED) and sync application status."""
        clean_offer_id = validate_non_empty(offer_id, "Offer ID").upper()
        clean_status = validate_non_empty(new_status, "Offer status").upper()

        if clean_status not in ("OFFERED", "ACCEPTED", "DECLINED"):
            raise ValidationError("Offer status must be 'OFFERED', 'ACCEPTED', or 'DECLINED'.")

        existing_offer = self.offer_dao.find_by_id(clean_offer_id)
        if not existing_offer:
            raise ValidationError(f"Offer with ID '{clean_offer_id}' does not exist.")

        if clean_status == "DECLINED":
            conn = get_connection()
            conn.autocommit = False
            try:
                self.offer_dao.update_status(clean_offer_id, "DECLINED", connection=conn)
                self.application_dao.update_status(
                    existing_offer.application_id, STATUS_REJECTED, connection=conn
                )
                conn.commit()
                log_activity(f"Offer Declined: {clean_offer_id}")
                log_activity(f"Candidate Rejected: {existing_offer.application_id}")
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
        else:
            self.offer_dao.update_status(clean_offer_id, clean_status)
            log_activity(f"Offer Status Updated: {clean_offer_id} to {clean_status}")

        updated = self.offer_dao.find_by_id(clean_offer_id)
        if not updated:
            raise RPMSException(f"Failed to retrieve updated offer '{clean_offer_id}'.")
        return updated

    def get_offer_by_id(self, offer_id: str) -> Offer:
        """Fetch offer details by primary key."""
        clean_id = validate_non_empty(offer_id, "Offer ID").upper()
        offer = self.offer_dao.find_by_id(clean_id)
        if not offer:
            raise ValidationError(f"Offer with ID '{clean_id}' does not exist.")
        return offer

    def get_offer_by_application(self, application_id: str) -> Offer:
        """Fetch offer details for a given application."""
        clean_id = validate_non_empty(application_id, "Application ID").upper()
        offer = self.offer_dao.find_by_application(clean_id)
        if not offer:
            raise ValidationError(f"No offer found for application '{clean_id}'.")
        return offer

    def get_all_offers(self) -> List[Offer]:
        """Fetch all issued job offers."""
        return self.offer_dao.get_all()

