"""Main application menu and navigation loop."""

from rpms.app.application_menu import ApplicationMenu
from rpms.app.candidate_menu import CandidateMenu
from rpms.app.company_menu import CompanyMenu
from rpms.app.interview_menu import InterviewMenu
from rpms.app.job_menu import JobMenu
from rpms.app.offer_menu import OfferMenu
from rpms.app.placement_menu import PlacementMenu
from rpms.app.report_menu import ReportMenu
from rpms.exception import DatabaseConnectionError, RPMSException
from rpms.util.branding import APP_NAME, APP_SUBTITLE
from rpms.util.db_connection import get_connection
from rpms.util.logger import log_activity


def _check_db_connection() -> bool:
    """Verify database accessibility before starting the application."""
    try:
        conn = get_connection()
        conn.close()
        return True
    except DatabaseConnectionError as exc:
        print("\nDatabase Connection Error:")
        print(str(exc))
        print("Please verify MySQL service is running and configuration in .env or config.py is correct.")
        return False
    except Exception as exc:
        print("\nUnexpected Database Connection Failure:")
        print(f"Details: {exc}")
        return False


def _print_main_menu() -> None:
    """Print the formatted main banner and menu options."""
    print("==================================")
    print(APP_NAME.upper())
    print(APP_SUBTITLE)
    print("==================================")
    print("1. Candidates")
    print("2. Companies")
    print("3. Jobs")
    print("4. Applications")
    print("5. Interviews")
    print("6. Offers")
    print("7. Placements")
    print("8. Reports")
    print("9. Exit")


def run() -> None:
    """Main execution loop of the console application."""
    if not _check_db_connection():
        return

    log_activity(f"{APP_NAME} started")

    candidate_menu = CandidateMenu()
    company_menu = CompanyMenu()
    job_menu = JobMenu()
    application_menu = ApplicationMenu()
    interview_menu = InterviewMenu()
    offer_menu = OfferMenu()
    placement_menu = PlacementMenu()
    report_menu = ReportMenu()

    try:
        while True:
            _print_main_menu()
            choice = input("\nEnter choice (1-9): ").strip()

            if choice == "1":
                try:
                    candidate_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Candidates Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "2":
                try:
                    company_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Companies Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "3":
                try:
                    job_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Jobs Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "4":
                try:
                    application_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Applications Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "5":
                try:
                    interview_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Interviews Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "6":
                try:
                    offer_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Offers Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "7":
                try:
                    placement_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Placements Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "8":
                try:
                    report_menu.show()
                except RPMSException as exc:
                    print(f"\nError: {exc}")
                    input("\nPress Enter to continue...")
                except Exception as exc:
                    print("\nAn unexpected error occurred. Details have been logged.")
                    log_activity(f"Unexpected Error in Reports Menu: {type(exc).__name__} - {str(exc)}")
                    input("\nPress Enter to continue...")
            elif choice == "9":
                print(f"\nThank you for using {APP_NAME}. Goodbye!\n")
                log_activity(f"{APP_NAME} closed")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 9.")
                input("Press Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        print(f"\n\nExiting {APP_NAME}.")
        log_activity(f"{APP_NAME} closed")
