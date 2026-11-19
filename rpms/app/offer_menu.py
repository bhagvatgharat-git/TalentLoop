"""Console submenu for job offer management."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.offer import Offer
from rpms.service.offer_service import OfferService
from rpms.util.branding import APP_NAME
from rpms.util.table_printer import print_table

OFFER_HEADERS = [
    "Offer ID",
    "App ID",
    "Candidate",
    "Company",
    "Designation",
    "LPA",
    "Offer Date",
    "Joining Date",
    "Status",
]


def _format_offer_rows(offers: List[Offer]) -> List[List[Any]]:
    return [
        [
            o.offer_id,
            o.application_id,
            o.candidate_name or "N/A",
            o.company_name or "N/A",
            o.designation,
            f"{o.package_lpa:.2f}",
            str(o.offer_date),
            str(o.joining_date),
            o.offer_status,
        ]
        for o in offers
    ]


class OfferMenu:
    """Console user interface for offer letter management."""

    def __init__(self, service: Optional[OfferService] = None):
        self.service = service or OfferService()

    def show(self) -> None:
        """Display offer menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Offer Management ---")
            print("1. Create Offer")
            print("2. Update Offer Status (Accept / Decline)")
            print("3. View Offer by Application")
            print("4. View All Offers")
            print("5. Back to Main Menu")

            choice = input("Enter choice (1-5): ").strip()
            if choice == "1":
                self._handle_create()
            elif choice == "2":
                self._handle_update_status()
            elif choice == "3":
                self._handle_view_by_app()
            elif choice == "4":
                self._handle_view_all()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 5.")

    def _handle_create(self) -> None:
        print("\n--- Create New Offer Letter ---")
        try:
            app_id = input("Enter Application ID (status must be SELECTED): ").strip().upper()
            if not app_id:
                print("Application ID is required.")
                return

            designation = input("Enter Job Designation: ").strip()
            package_lpa = float(input("Enter Offered Package in LPA: ").strip())
            offer_date = input("Enter Offer Date (YYYY-MM-DD): ").strip()
            joining_date = input("Enter Expected Joining Date (YYYY-MM-DD): ").strip()

            saved = self.service.create_offer(
                application_id=app_id,
                designation=designation,
                package_lpa=package_lpa,
                offer_date=offer_date,
                joining_date=joining_date,
            )
            print(
                f"\nSuccess: Offer created with ID: {saved.offer_id} for Application '{saved.application_id}'. "
                f"Application transitioned to OFFERED."
            )
        except RPMSException as exc:
            print(f"\nOffer Creation Failed: {exc}")
        except ValueError:
            print("\nError: Invalid numeric or date format entered.")

    def _handle_update_status(self) -> None:
        print("\n--- Update Offer Status ---")
        offer_id = input("Enter Offer ID (e.g. OFF101): ").strip().upper()
        if not offer_id:
            print("Offer ID is required.")
            return

        print("Options: ACCEPTED, DECLINED")
        status = input("Enter New Status: ").strip().upper()

        try:
            updated = self.service.update_offer_status(offer_id, status)
            print(f"\nSuccess: Offer '{updated.offer_id}' updated to {updated.offer_status}.")
            if status == "DECLINED":
                print("Application transitioned to REJECTED.")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_view_by_app(self) -> None:
        print("\n--- View Offer by Application ---")
        app_id = input("Enter Application ID: ").strip().upper()
        if not app_id:
            print("Application ID is required.")
            return

        try:
            offer = self.service.get_offer_by_application(app_id)
            print_table(OFFER_HEADERS, _format_offer_rows([offer]))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_all(self) -> None:
        print("\n--- View All Offers ---")
        try:
            offers = self.service.get_all_offers()
            print_table(OFFER_HEADERS, _format_offer_rows(offers))
        except RPMSException as exc:
            print(f"Error: {exc}")

