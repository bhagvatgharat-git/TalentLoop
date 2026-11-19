"""Console submenu for application workflow and status management."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.application import Application
from rpms.model.status import ALL_APPLICATION_STATUSES, ALLOWED_TRANSITIONS
from rpms.service.application_service import ApplicationService
from rpms.util.branding import APP_NAME
from rpms.util.table_printer import print_table

APPLICATION_HEADERS = [
    "App ID",
    "Cand ID",
    "Candidate Name",
    "Job ID",
    "Job Title",
    "Applied Date",
    "Status",
]


def _format_application_rows(applications: List[Application]) -> List[List[Any]]:
    return [
        [
            a.application_id,
            a.candidate_id,
            a.candidate_name or "N/A",
            a.job_id,
            a.job_title or "N/A",
            str(a.applied_date),
            a.status,
        ]
        for a in applications
    ]


class ApplicationMenu:
    """Console user interface for application processing."""

    def __init__(self, service: Optional[ApplicationService] = None):
        self.service = service or ApplicationService()

    def show(self) -> None:
        """Display application menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Application Management ---")
            print("1. Check Candidate Eligibility")
            print("2. Apply for Job")
            print("3. Shortlist Application")
            print("4. Update Application Status")
            print("5. Reject Application")
            print("6. View Applications by Job")
            print("7. View Applications by Candidate")
            print("8. View Applications by Status")
            print("9. View All Applications")
            print("10. Back to Main Menu")

            choice = input("Enter choice (1-10): ").strip()
            if choice == "1":
                self._handle_check_eligibility()
            elif choice == "2":
                self._handle_apply()
            elif choice == "3":
                self._handle_shortlist()
            elif choice == "4":
                self._handle_update_status()
            elif choice == "5":
                self._handle_reject()
            elif choice == "6":
                self._handle_view_by_job()
            elif choice == "7":
                self._handle_view_by_candidate()
            elif choice == "8":
                self._handle_view_by_status()
            elif choice == "9":
                self._handle_view_all()
            elif choice == "10":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 10.")

    def _handle_check_eligibility(self) -> None:
        print("\n--- Check Candidate Eligibility ---")
        cand_id = input("Enter Candidate ID (e.g. CAN1001): ").strip().upper()
        job_id = input("Enter Job ID (e.g. JOB101): ").strip().upper()

        if not cand_id or not job_id:
            print("Both Candidate ID and Job ID are required.")
            return

        try:
            result = self.service.check_eligibility(cand_id, job_id)
            print("\nEligibility Result:")
            print(f"Status: {result.status}")
            print(f"Reason: {result.reason}")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_apply(self) -> None:
        print("\n--- Apply for Job ---")
        cand_id = input("Enter Candidate ID (e.g. CAN1001): ").strip().upper()
        job_id = input("Enter Job ID (e.g. JOB101): ").strip().upper()

        if not cand_id or not job_id:
            print("Both Candidate ID and Job ID are required.")
            return

        try:
            saved = self.service.apply(cand_id, job_id)
            print(
                f"\nSuccess: Application created successfully with ID: {saved.application_id} "
                f"({saved.candidate_name} -> {saved.job_title})"
            )
        except RPMSException as exc:
            print(f"\nApplication Failed: {exc}")

    def _handle_shortlist(self) -> None:
        print("\n--- Shortlist Application ---")
        app_id = input("Enter Application ID (e.g. APP501): ").strip().upper()
        if not app_id:
            print("Application ID is required.")
            return

        try:
            updated = self.service.shortlist(app_id)
            print(f"\nSuccess: Application '{updated.application_id}' transitioned to SHORTLISTED.")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_update_status(self) -> None:
        print("\n--- Update Application Status ---")
        app_id = input("Enter Application ID (e.g. APP501): ").strip().upper()
        if not app_id:
            print("Application ID is required.")
            return

        try:
            current = self.service.get_application_by_id(app_id)
            print(f"Current Status of {current.application_id}: {current.status}")
            allowed = ALLOWED_TRANSITIONS.get(current.status, [])
            if not allowed:
                print(f"Status '{current.status}' is terminal. No further transitions allowed.")
                return

            print(f"Allowed next transitions: {', '.join(allowed)}")
            new_status = input(f"Enter New Status ({'/'.join(allowed)}): ").strip().upper()

            updated = self.service.update_status(app_id, new_status)
            print(f"\nSuccess: Application '{updated.application_id}' status updated to {updated.status}.")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_reject(self) -> None:
        print("\n--- Reject Application ---")
        app_id = input("Enter Application ID (e.g. APP501): ").strip().upper()
        if not app_id:
            print("Application ID is required.")
            return

        confirm = input(f"Are you sure you want to reject application '{app_id}'? (y/N): ").strip().lower()
        if confirm != "y":
            print("Action cancelled.")
            return

        try:
            updated = self.service.reject(app_id)
            print(f"\nSuccess: Application '{updated.application_id}' has been marked as REJECTED.")
        except RPMSException as exc:
            print(f"\nError: {exc}")

    def _handle_view_by_job(self) -> None:
        print("\n--- View Applications by Job ---")
        job_id = input("Enter Job ID: ").strip().upper()
        if not job_id:
            print("Job ID is required.")
            return

        try:
            apps = self.service.get_applications_by_job(job_id)
            print_table(APPLICATION_HEADERS, _format_application_rows(apps))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_by_candidate(self) -> None:
        print("\n--- View Applications by Candidate ---")
        cand_id = input("Enter Candidate ID: ").strip().upper()
        if not cand_id:
            print("Candidate ID is required.")
            return

        try:
            apps = self.service.get_applications_by_candidate(cand_id)
            print_table(APPLICATION_HEADERS, _format_application_rows(apps))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_by_status(self) -> None:
        print("\n--- View Applications by Status ---")
        print(f"Available statuses: {', '.join(ALL_APPLICATION_STATUSES)}")
        status = input("Enter Status to filter by: ").strip().upper()
        if not status:
            print("Status cannot be empty.")
            return

        try:
            apps = self.service.get_applications_by_status(status)
            print_table(APPLICATION_HEADERS, _format_application_rows(apps))
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_view_all(self) -> None:
        print("\n--- View All Applications ---")
        try:
            apps = self.service.get_all_applications()
            print_table(APPLICATION_HEADERS, _format_application_rows(apps))
        except RPMSException as exc:
            print(f"Error: {exc}")

