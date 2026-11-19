"""Console submenu for job vacancy management."""

from typing import Any, Callable, List, Optional

from rpms.exception import RPMSException
from rpms.model.job import Job
from rpms.service.job_service import JobService
from rpms.util.branding import APP_NAME
from rpms.util.table_printer import print_table
from rpms.util.validators import (
    validate_future_date,
    validate_non_empty,
    validate_non_negative_int,
    validate_percentage,
    validate_positive_int,
)

JOB_HEADERS = [
    "Job ID",
    "Company",
    "Title",
    "Tech",
    "Openings",
    "Location",
    "LPA",
    "Min %",
    "Year",
    "Max Backlogs",
    "Deadline",
    "Status",
]


def _format_job_rows(jobs: List[Job]) -> List[List[Any]]:
    return [
        [
            j.job_id,
            j.company_name or j.company_id,
            j.job_title,
            j.technology,
            j.openings,
            j.location,
            f"{j.package_lpa:.2f}",
            f"{j.min_percentage:.2f}%",
            j.passing_year,
            j.max_backlogs,
            str(j.deadline),
            j.status,
        ]
        for j in jobs
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


class JobMenu:
    """Console user interface for job vacancy operations."""

    def __init__(self, service: Optional[JobService] = None):
        self.service = service or JobService()

    def show(self) -> None:
        """Display job menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Job Management ---")
            print("1. Create Job")
            print("2. Update Job")
            print("3. View Open Jobs")
            print("4. Close Job")
            print("5. Search Jobs")
            print("6. Back to Main Menu")

            choice = input("Enter choice (1-6): ").strip()
            if choice == "1":
                self._handle_create()
            elif choice == "2":
                self._handle_update()
            elif choice == "3":
                self._handle_view_open()
            elif choice == "4":
                self._handle_close()
            elif choice == "5":
                self._handle_search()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 6.")

    def _handle_create(self) -> None:
        print("\n--- Create New Job Opening ---")
        try:
            company_id = _prompt_validated_input("Enter Company ID", lambda v: validate_non_empty(v, "Company ID")).upper()
            title = _prompt_validated_input("Enter Job Title", lambda v: validate_non_empty(v, "Job title"))
            technology = _prompt_validated_input("Enter Technology", lambda v: validate_non_empty(v, "Technology"))
            openings = _prompt_validated_input("Enter Number of Openings", lambda v: validate_positive_int(v, "Openings"))
            location = _prompt_validated_input("Enter Location", lambda v: validate_non_empty(v, "Location"))
            package_lpa = _prompt_validated_input("Enter Package in LPA", float)
            min_percentage = _prompt_validated_input("Enter Minimum Percentage (0-100)", validate_percentage, default=0.0)
            passing_year = _prompt_validated_input("Enter Target Passing Year", lambda v: validate_positive_int(v, "Passing year"), default=2024)
            max_backlogs = _prompt_validated_input("Enter Maximum Allowed Backlogs", lambda v: validate_non_negative_int(v, "Max backlogs"), default=0)
            deadline = _prompt_validated_input("Enter Application Deadline (YYYY-MM-DD)", lambda v: validate_future_date(v, "Deadline"))

            saved = self.service.create_job(
                company_id=company_id,
                job_title=title,
                technology=technology,
                openings=openings,
                location=location,
                package_lpa=package_lpa,
                min_percentage=min_percentage,
                passing_year=passing_year,
                max_backlogs=max_backlogs,
                deadline=deadline,
            )
            print(f"\nSuccess: Job posted with ID: {saved.job_id} for {saved.company_name}")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_update(self) -> None:
        print("\n--- Update Job Opening ---")
        job_id = input("Enter Job ID to update: ").strip()
        if not job_id:
            print("Job ID is required.")
            return

        try:
            existing = self.service.get_job_by_id(job_id)
            print(f"Editing Job: {existing.job_id} ({existing.job_title} at {existing.company_name or existing.company_id})")
            print("Press Enter to keep existing value.")

            company_id = _prompt_validated_input("Company ID", lambda v: validate_non_empty(v, "Company ID"), default=existing.company_id).upper()
            title = _prompt_validated_input("Job Title", lambda v: validate_non_empty(v, "Job title"), default=existing.job_title)
            technology = _prompt_validated_input("Technology", lambda v: validate_non_empty(v, "Technology"), default=existing.technology)
            openings = _prompt_validated_input("Openings count", lambda v: validate_positive_int(v, "Openings"), default=existing.openings)
            location = _prompt_validated_input("Location", lambda v: validate_non_empty(v, "Location"), default=existing.location)
            package_lpa = _prompt_validated_input("Package in LPA", float, default=existing.package_lpa)
            min_percentage = _prompt_validated_input("Minimum Percentage (0-100)", validate_percentage, default=existing.min_percentage)
            passing_year = _prompt_validated_input("Target Passing Year", lambda v: validate_positive_int(v, "Passing year"), default=existing.passing_year)
            max_backlogs = _prompt_validated_input("Maximum Allowed Backlogs", lambda v: validate_non_negative_int(v, "Max backlogs"), default=existing.max_backlogs)
            deadline = _prompt_validated_input("Application Deadline (YYYY-MM-DD)", lambda v: validate_future_date(v, "Deadline"), default=str(existing.deadline))
            status = _prompt_validated_input("Status (OPEN / CLOSED)", lambda v: validate_non_empty(v, "Status"), default=existing.status).upper()

            updated = self.service.update_job(
                job_id=existing.job_id,
                company_id=company_id,
                job_title=title,
                technology=technology,
                openings=openings,
                location=location,
                package_lpa=package_lpa,
                min_percentage=min_percentage,
                passing_year=passing_year,
                max_backlogs=max_backlogs,
                deadline=deadline,
                status=status,
            )
            print(f"\nSuccess: Job '{updated.job_id}' updated successfully.")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_view_open(self) -> None:
        print("\n--- View Open Jobs ---")
        try:
            jobs = self.service.get_open_jobs()
            print_table(JOB_HEADERS, _format_job_rows(jobs))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_close(self) -> None:
        print("\n--- Close Job Opening ---")
        job_id = input("Enter Job ID to close: ").strip()
        if not job_id:
            print("Job ID cannot be empty.")
            return

        confirm = input(f"Are you sure you want to close job '{job_id}'? (y/N): ").strip().lower()
        if confirm != "y":
            print("Action cancelled.")
            return

        try:
            self.service.close_job(job_id)
            print(f"Success: Job '{job_id}' has been marked as CLOSED.")
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_search(self) -> None:
        print("\n--- Search Jobs ---")
        keyword = input("Enter search keyword (title, technology, or location): ").strip()
        if not keyword:
            print("Search keyword cannot be empty.")
            return

        try:
            results = self.service.search_jobs(keyword)
            print_table(JOB_HEADERS, _format_job_rows(results))
        except RPMSException as exc:
            print(f"Error: {exc}")
