"""Console submenu for placement confirmation and tracking."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.placement import Placement
from rpms.service.placement_service import PlacementService
from rpms.util.branding import APP_NAME
from rpms.util.table_printer import print_table

PLACEMENT_HEADERS = [
    "Placement ID",
    "App ID",
    "Candidate",
    "Company",
    "Designation",
    "Final LPA",
    "Joining Date",
    "Status",
]


def _format_placement_rows(placements: List[Placement]) -> List[List[Any]]:
    return [
        [
            p.placement_id,
            p.application_id,
            p.candidate_name or "N/A",
            p.company_name or "N/A",
            p.designation,
            f"{p.final_package_lpa:.2f}",
            str(p.actual_joining_date),
            p.joining_status,
        ]
        for p in placements
    ]


class PlacementMenu:
    """Console user interface for confirmed student placements."""

    def __init__(self, service: Optional[PlacementService] = None):
        self.service = service or PlacementService()

    def show(self) -> None:
        """Display placement menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Placement Management ---")
            print("1. Record Placement")
            print("2. View Placement by ID")
            print("3. View Placements by Company")
            print("4. View All Placements")
            print("5. Back to Main Menu")

            choice = input("Enter choice (1-5): ").strip()
            if choice == "1":
                self._handle_record()
            elif choice == "2":
                self._handle_view_by_id()
            elif choice == "3":
                self._handle_view_by_company()
            elif choice == "4":
                self._handle_view_all()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 5.")

    def _handle_record(self) -> None:
        print("\n--- Record Confirmed Placement ---")
        try:
            app_id = input("Enter Application ID (must have ACCEPTED offer): ").strip().upper()
            if not app_id:
                print("Application ID is required.")
                return

            print("Press Enter on any field to accept values from the accepted offer.")
            designation = input("Designation override: ").strip() or None
            pkg_str = input("Final Package LPA override: ").strip()
            pkg_val = float(pkg_str) if pkg_str else None
            date_str = input("Actual Joining Date override (YYYY-MM-DD): ").strip() or None

            saved = self.service.record_placement(
                application_id=app_id,
                designation=designation,
                final_package_lpa=pkg_val,
                actual_joining_date=date_str,
            )
            print(
                f"\nSuccess: Placement recorded with ID: {saved.placement_id} "
                f"for Application '{saved.application_id}'. Application moved to JOINED and vacancy updated."
            )
        except RPMSException as exc:
            print(f"\nPlacement Error: {exc}")
        except ValueError:
            print("\nError: Invalid numeric package entered.")

    def _handle_view_by_id(self) -> None:
        print("\n--- View Placement by ID ---")
        plc_id = input("Enter Placement ID (e.g. PLC101): ").strip().upper()
        if not plc_id:
            print("Placement ID is required.")
            return

        try:
            placement = self.service.get_placement_by_id(plc_id)
            print_table(PLACEMENT_HEADERS, _format_placement_rows([placement]))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_by_company(self) -> None:
        print("\n--- View Placements by Company ---")
        comp_id = input("Enter Company ID (e.g. COM101): ").strip().upper()
        if not comp_id:
            print("Company ID is required.")
            return

        try:
            placements = self.service.get_placements_by_company(comp_id)
            print_table(PLACEMENT_HEADERS, _format_placement_rows(placements))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_all(self) -> None:
        print("\n--- View All Placements ---")
        try:
            placements = self.service.get_all_placements()
            print_table(PLACEMENT_HEADERS, _format_placement_rows(placements))
        except RPMSException as exc:
            print(f"Error: {exc}")

