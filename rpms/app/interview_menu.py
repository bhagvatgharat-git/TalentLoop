"""Console submenu for interview scheduling, tracking, and evaluation."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.interview import Interview
from rpms.service.interview_service import InterviewService
from rpms.util.branding import APP_NAME
from rpms.util.console_input import pause_for_user
from rpms.util.table_printer import print_table
from rpms.util.validators import (
    validate_future_date,
    validate_non_empty,
    validate_positive_int,
)

INTERVIEW_HEADERS = [
    "Interview ID",
    "App ID",
    "Candidate",
    "Company",
    "Job Title",
    "Round",
    "Date",
    "Mode",
    "Interviewer",
    "Status",
    "Result",
]


def _format_interview_rows(interviews: List[Interview]) -> List[List[Any]]:
    return [
        [
            i.interview_id,
            i.application_id,
            i.candidate_name or "N/A",
            i.company_name or "N/A",
            i.job_title or "N/A",
            i.round_no,
            str(i.interview_date),
            i.mode,
            i.interviewer,
            i.status,
            i.feedback_result or "Pending",
        ]
        for c, i in enumerate(interviews)
    ]


class InterviewMenu:
    """Console user interface for interview rounds and feedback entry."""

    def __init__(self, service: Optional[InterviewService] = None):
        self.service = service or InterviewService()

    def show(self) -> None:
        """Display interview menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Interview Management ---")
            print("1. Schedule Interview")
            print("2. Update Interview Status")
            print("3. Add Interview Feedback")
            print("4. View Interviews by Candidate")
            print("5. View Interviews by Company")
            print("6. Back to Main Menu")

            choice = input("Enter choice (1-6): ").strip()
            if choice == "1":
                self._handle_schedule()
            elif choice == "2":
                self._handle_update_status()
            elif choice == "3":
                self._handle_add_feedback()
            elif choice == "4":
                self._handle_view_by_candidate()
            elif choice == "5":
                self._handle_view_by_company()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 6.")

    def _handle_schedule(self) -> None:
        print("\n--- Schedule Interview Round ---")
        try:
            app_id = input("Enter Application ID (e.g. APP501): ").strip().upper()
            if not app_id:
                print("Application ID is required.")
                pause_for_user()
                return

            date_str = input("Enter Interview Date (YYYY-MM-DD): ").strip()
            interview_date = validate_future_date(date_str, "Interview date")

            mode = input("Enter Interview Mode (Online / Offline) [Online]: ").strip() or "Online"
            interviewer = input("Enter Interviewer Name: ").strip()
            validate_non_empty(interviewer, "Interviewer name")

            round_input = input("Enter Round Number (Press Enter for auto-increment): ").strip()
            round_no = validate_positive_int(round_input, "Round number") if round_input else None

            saved = self.service.schedule_interview(
                application_id=app_id,
                interview_date=interview_date,
                mode=mode,
                interviewer=interviewer,
                round_no=round_no,
            )
            print(
                f"\nSuccess: Interview round {saved.round_no} scheduled with ID: {saved.interview_id} "
                f"for Application '{saved.application_id}'."
            )
        except RPMSException as exc:
            print(f"\nScheduling Error: {exc}")
        finally:
            pause_for_user()

    def _handle_update_status(self) -> None:
        print("\n--- Update Interview Status ---")
        interview_id = input("Enter Interview ID (e.g. INT101): ").strip().upper()
        if not interview_id:
            print("Interview ID is required.")
            pause_for_user()
            return

        print("Available statuses: SCHEDULED, COMPLETED, CANCELLED")
        status = input("Enter New Status: ").strip().upper()

        try:
            updated = self.service.update_interview_status(interview_id, status)
            print(f"\nSuccess: Interview '{updated.interview_id}' status updated to {updated.status}.")
        except RPMSException as exc:
            print(f"\nError: {exc}")
        finally:
            pause_for_user()

    def _handle_add_feedback(self) -> None:
        print("\n--- Add Interview Feedback ---")
        try:
            interview_id = input("Enter Interview ID (e.g. INT101): ").strip().upper()
            if not interview_id:
                print("Interview ID is required.")
                pause_for_user()
                return

            tech_str = input("Enter Technical Rating (1-10): ").strip()
            comm_str = input("Enter Communication Rating (1-10): ").strip()
            remarks = input("Enter Evaluation Remarks: ").strip()
            result = input("Enter Result (PASS / FAIL): ").strip().upper()

            is_final = False
            if result == "PASS":
                final_input = input("Is this the final round for selection? (y/N): ").strip().lower()
                is_final = final_input == "y"

            saved = self.service.add_feedback(
                interview_id=interview_id,
                technical_rating=int(tech_str),
                communication_rating=int(comm_str),
                remarks=remarks,
                result=result,
                is_final_round=is_final,
            )
            print(f"\nSuccess: Feedback recorded with ID: {saved.feedback_id}. Result: {saved.result}.")
            if result == "FAIL":
                print("Application has been moved to REJECTED status.")
            elif result == "PASS" and is_final:
                print("Application has been moved to SELECTED status.")
        except RPMSException as exc:
            print(f"\nFeedback Error: {exc}")
        finally:
            pause_for_user()

    def _handle_view_by_candidate(self) -> None:
        print("\n--- View Interviews by Candidate ---")
        cand_id = input("Enter Candidate ID (e.g. CAN1001): ").strip().upper()
        if not cand_id:
            print("Candidate ID is required.")
            pause_for_user()
            return

        try:
            interviews = self.service.get_interviews_by_candidate(cand_id)
            print_table(INTERVIEW_HEADERS, _format_interview_rows(interviews))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()

    def _handle_view_by_company(self) -> None:
        print("\n--- View Interviews by Company ---")
        comp_id = input("Enter Company ID (e.g. COM101): ").strip().upper()
        if not comp_id:
            print("Company ID is required.")
            pause_for_user()
            return

        try:
            interviews = self.service.get_interviews_by_company(comp_id)
            print_table(INTERVIEW_HEADERS, _format_interview_rows(interviews))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()
