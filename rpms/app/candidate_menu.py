"""Console submenu for candidate management."""

from typing import Any, Callable, List, Optional

from rpms.exception import RPMSException
from rpms.model.candidate import Candidate
from rpms.service.candidate_service import CandidateService
from rpms.util.branding import APP_NAME
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


def _prompt_validated_input(
    prompt_text: str,
    validator: Optional[Callable[[str], Any]] = None,
    default: Optional[Any] = None,
) -> Any:
    """Prompt user until a valid input is provided or default accepted."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw_val = input(f"{prompt_text}{suffix}: ").strip()
        if not raw_val and default is not None:
            return default
        if not raw_val:
            print("Error: Input cannot be empty. Please enter a value.")
            continue
        if validator:
            try:
                return validator(raw_val)
            except Exception as exc:
                print(f"Validation error: {exc}")
                continue
        return raw_val


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
            name = _prompt_validated_input("Enter full name", lambda v: validate_non_empty(v, "Name"))
            email = _prompt_validated_input("Enter email address", validate_email)
            mobile = _prompt_validated_input("Enter 10-digit mobile number", validate_mobile)
            technology = _prompt_validated_input("Enter primary technology", lambda v: validate_non_empty(v, "Technology"))
            percentage = _prompt_validated_input("Enter percentage (0-100)", validate_percentage)
            passing_year = _prompt_validated_input("Enter passing year", lambda v: validate_positive_int(v, "Passing year"))
            backlogs = _prompt_validated_input("Enter active backlogs", lambda v: validate_non_negative_int(v, "Backlog count"), default=0)

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

    def _handle_update(self) -> None:
        print("\n--- Update Candidate ---")
        candidate_id = input("Enter Candidate ID to update: ").strip()
        if not candidate_id:
            print("Candidate ID is required.")
            return

        try:
            existing = self.service.get_candidate_by_id(candidate_id)
            print(f"Editing Candidate: {existing.candidate_id} ({existing.name})")
            print("Press Enter to keep existing value.")

            name = _prompt_validated_input("Full name", lambda v: validate_non_empty(v, "Name"), default=existing.name)
            email = _prompt_validated_input("Email address", validate_email, default=existing.email)
            mobile = _prompt_validated_input("Mobile number", validate_mobile, default=existing.mobile)
            technology = _prompt_validated_input("Primary technology", lambda v: validate_non_empty(v, "Technology"), default=existing.technology)
            percentage = _prompt_validated_input("Percentage (0-100)", validate_percentage, default=existing.percentage)
            passing_year = _prompt_validated_input("Passing year", lambda v: validate_positive_int(v, "Passing year"), default=existing.passing_year)
            backlogs = _prompt_validated_input("Active backlogs", lambda v: validate_non_negative_int(v, "Backlog count"), default=existing.backlog_count)
            is_active = _prompt_validated_input("Is Active (1 for Yes, 0 for No)", lambda v: validate_non_negative_int(v, "Status"), default=existing.is_active)

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

    def _handle_search(self) -> None:
        print("\n--- Search Candidates ---")
        keyword = input("Enter search term (name or technology): ").strip()
        if not keyword:
            print("Search term cannot be empty.")
            return

        try:
            results = self.service.search_candidates(keyword)
            print_table(CANDIDATE_HEADERS, _format_candidate_rows(results))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_all(self) -> None:
        print("\n--- View All Candidates ---")
        filter_choice = input("Show active only? (Y/n): ").strip().lower()
        active_only = filter_choice != "n"
        try:
            candidates = self.service.get_all_candidates(active_only=active_only)
            print_table(CANDIDATE_HEADERS, _format_candidate_rows(candidates))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_deactivate(self) -> None:
        print("\n--- Deactivate Candidate ---")
        candidate_id = input("Enter Candidate ID to deactivate: ").strip()
        if not candidate_id:
            print("Candidate ID cannot be empty.")
            return

        confirm = input(f"Are you sure you want to deactivate candidate '{candidate_id}'? (y/N): ").strip().lower()
        if confirm != "y":
            print("Deactivation cancelled.")
            return

        try:
            self.service.deactivate_candidate(candidate_id)
            print(f"Success: Candidate '{candidate_id}' deactivated successfully.")
        except RPMSException as exc:
            print(f"Error: {exc}")

