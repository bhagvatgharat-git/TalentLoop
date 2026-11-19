"""Console submenu for candidate management."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.candidate import Candidate
from rpms.service.candidate_service import CandidateService
from rpms.util.branding import APP_NAME
from rpms.util.console_input import pause_for_user, prompt_validated_input
from rpms.util.table_printer import print_table
from rpms.util.validators import (
    validate_email,
    validate_mobile,
    validate_non_empty,
    validate_non_negative_int,
    validate_percentage,
    validate_positive_int,
)

CANDIDATE_HEADERS = [
    "ID",
    "Name",
    "Email",
    "Mobile",
    "Technology",
    "Percentage",
    "Year",
    "Backlogs",
    "Status",
]


def _format_candidate_rows(candidates: List[Candidate]) -> List[List[Any]]:
    return [
        [
            c.candidate_id,
            c.name,
            c.email,
            c.mobile,
            c.technology,
            f"{c.percentage:.2f}%",
            c.passing_year,
            c.backlog_count,
            "Active" if c.is_active else "Inactive",
        ]
        for c in candidates
    ]


class CandidateMenu:
    """Console user interface for candidate operations."""

    def __init__(self, service: Optional[CandidateService] = None):
        self.service = service or CandidateService()

    def show(self) -> None:
        """Display candidate menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Candidate Management ---")
            print("1. Add Candidate")
            print("2. Update Candidate")
            print("3. Search Candidates")
            print("4. View All Candidates")
            print("5. Deactivate Candidate")
            print("6. Back to Main Menu")

            choice = input("Enter choice (1-6): ").strip()
            if choice == "1":
                self._handle_add()
            elif choice == "2":
                self._handle_update()
            elif choice == "3":
                self._handle_search()
            elif choice == "4":
                self._handle_view_all()
            elif choice == "5":
                self._handle_deactivate()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 6.")

    def _handle_add(self) -> None:
        print("\n--- Add New Candidate ---")
        try:
            name = prompt_validated_input("Enter full name", lambda v: validate_non_empty(v, "Name"))
            email = prompt_validated_input("Enter email address", validate_email)
            mobile = prompt_validated_input("Enter 10-digit mobile number", validate_mobile)
            technology = prompt_validated_input("Enter primary technology", lambda v: validate_non_empty(v, "Technology"))
            percentage = prompt_validated_input("Enter percentage (0-100)", validate_percentage)
            passing_year = prompt_validated_input("Enter passing year", lambda v: validate_positive_int(v, "Passing year"))
            backlogs = prompt_validated_input("Enter active backlogs", lambda v: validate_non_negative_int(v, "Backlog count"), default=0)

            saved = self.service.create_candidate(
                name=name,
                email=email,
                mobile=mobile,
                technology=technology,
                percentage=percentage,
                passing_year=passing_year,
                backlog_count=backlogs,
            )
            print(f"\nSuccess: Candidate registered with ID: {saved.candidate_id}")
        except RPMSException as exc:
            print(f"\nError: {exc}")
        finally:
            pause_for_user()

    def _handle_update(self) -> None:
        print("\n--- Update Candidate ---")
        candidate_id = input("Enter Candidate ID to update: ").strip()
        if not candidate_id:
            print("Candidate ID is required.")
            pause_for_user()
            return

        try:
            existing = self.service.get_candidate_by_id(candidate_id)
            print(f"Editing Candidate: {existing.candidate_id} ({existing.name})")
            print("Press Enter to keep existing value.")

            name = prompt_validated_input("Full name", lambda v: validate_non_empty(v, "Name"), default=existing.name)
            email = prompt_validated_input("Email address", validate_email, default=existing.email)
            mobile = prompt_validated_input("Mobile number", validate_mobile, default=existing.mobile)
            technology = prompt_validated_input("Primary technology", lambda v: validate_non_empty(v, "Technology"), default=existing.technology)
            percentage = prompt_validated_input("Percentage (0-100)", validate_percentage, default=existing.percentage)
            passing_year = prompt_validated_input("Passing year", lambda v: validate_positive_int(v, "Passing year"), default=existing.passing_year)
            backlogs = prompt_validated_input("Active backlogs", lambda v: validate_non_negative_int(v, "Backlog count"), default=existing.backlog_count)
            is_active = prompt_validated_input("Is Active (1 for Yes, 0 for No)", lambda v: validate_non_negative_int(v, "Status"), default=existing.is_active)

            updated = self.service.update_candidate(
                candidate_id=existing.candidate_id,
                name=name,
                email=email,
                mobile=mobile,
                technology=technology,
                percentage=percentage,
                passing_year=passing_year,
                backlog_count=backlogs,
                is_active=is_active,
            )
            print(f"\nSuccess: Candidate '{updated.candidate_id}' updated successfully.")
        except RPMSException as exc:
            print(f"\nError: {exc}")
        finally:
            pause_for_user()

    def _handle_search(self) -> None:
        print("\n--- Search Candidates ---")
        keyword = input("Enter search term (name or technology): ").strip()
        if not keyword:
            print("Search term cannot be empty.")
            pause_for_user()
            return

        try:
            results = self.service.search_candidates(keyword)
            print_table(CANDIDATE_HEADERS, _format_candidate_rows(results))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()

    def _handle_view_all(self) -> None:
        print("\n--- View All Candidates ---")
        filter_choice = input("Show active only? (Y/n): ").strip().lower()
        active_only = filter_choice != "n"
        try:
            candidates = self.service.get_all_candidates(active_only=active_only)
            print_table(CANDIDATE_HEADERS, _format_candidate_rows(candidates))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()

    def _handle_deactivate(self) -> None:
        print("\n--- Deactivate Candidate ---")
        candidate_id = input("Enter Candidate ID to deactivate: ").strip()
        if not candidate_id:
            print("Candidate ID cannot be empty.")
            pause_for_user()
            return

        confirm = input(f"Are you sure you want to deactivate candidate '{candidate_id}'? (y/N): ").strip().lower()
        if confirm != "y":
            print("Deactivation cancelled.")
            pause_for_user()
            return

        try:
            self.service.deactivate_candidate(candidate_id)
            print(f"Success: Candidate '{candidate_id}' deactivated successfully.")
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()
