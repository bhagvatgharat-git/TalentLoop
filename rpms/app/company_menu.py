"""Console submenu for company management."""

from typing import Any, List, Optional

from rpms.exception import RPMSException
from rpms.model.company import Company
from rpms.service.company_service import CompanyService
from rpms.util.branding import APP_NAME
from rpms.util.console_input import pause_for_user, prompt_validated_input
from rpms.util.table_printer import print_table
from rpms.util.validators import validate_email, validate_non_empty

COMPANY_HEADERS = [
    "ID",
    "Name",
    "Industry",
    "Location",
    "Contact Person",
    "Contact Email",
]


def _format_company_rows(companies: List[Company]) -> List[List[Any]]:
    return [
        [
            c.company_id,
            c.name,
            c.industry,
            c.location,
            c.contact_person,
            c.contact_email,
        ]
        for c in companies
    ]


class CompanyMenu:
    """Console user interface for company operations."""

    def __init__(self, service: Optional[CompanyService] = None):
        self.service = service or CompanyService()

    def show(self) -> None:
        """Display company menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Company Management ---")
            print("1. Add Company")
            print("2. Update Company")
            print("3. Search Companies")
            print("4. View All Companies")
            print("5. Back to Main Menu")

            choice = input("Enter choice (1-5): ").strip()
            if choice == "1":
                self._handle_add()
            elif choice == "2":
                self._handle_update()
            elif choice == "3":
                self._handle_search()
            elif choice == "4":
                self._handle_view_all()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 5.")

    def _handle_add(self) -> None:
        print("\n--- Add New Company ---")
        try:
            name = prompt_validated_input("Enter company name", lambda v: validate_non_empty(v, "Company name"))
            industry = prompt_validated_input("Enter industry sector", lambda v: validate_non_empty(v, "Industry"))
            location = prompt_validated_input("Enter company location/city", lambda v: validate_non_empty(v, "Location"))
            contact_person = prompt_validated_input("Enter contact person name", lambda v: validate_non_empty(v, "Contact person"))
            contact_email = prompt_validated_input("Enter contact email address", validate_email)

            saved = self.service.create_company(
                name=name,
                industry=industry,
                location=location,
                contact_person=contact_person,
                contact_email=contact_email,
            )
            print(f"\nSuccess: Company registered with ID: {saved.company_id}")
        except RPMSException as exc:
            print(f"\nError: {exc}")
        finally:
            pause_for_user()

    def _handle_update(self) -> None:
        print("\n--- Update Company ---")
        company_id = input("Enter Company ID to update: ").strip()
        if not company_id:
            print("Company ID is required.")
            pause_for_user()
            return

        try:
            existing = self.service.get_company_by_id(company_id)
            print(f"Editing Company: {existing.company_id} ({existing.name})")
            print("Press Enter to keep existing value.")

            name = prompt_validated_input("Company name", lambda v: validate_non_empty(v, "Company name"), default=existing.name)
            industry = prompt_validated_input("Industry sector", lambda v: validate_non_empty(v, "Industry"), default=existing.industry)
            location = prompt_validated_input("Location/city", lambda v: validate_non_empty(v, "Location"), default=existing.location)
            contact_person = prompt_validated_input("Contact person", lambda v: validate_non_empty(v, "Contact person"), default=existing.contact_person)
            contact_email = prompt_validated_input("Contact email", validate_email, default=existing.contact_email)

            updated = self.service.update_company(
                company_id=existing.company_id,
                name=name,
                industry=industry,
                location=location,
                contact_person=contact_person,
                contact_email=contact_email,
            )
            print(f"\nSuccess: Company '{updated.company_id}' updated successfully.")
        except RPMSException as exc:
            print(f"\nError: {exc}")
        finally:
            pause_for_user()

    def _handle_search(self) -> None:
        print("\n--- Search Companies ---")
        keyword = input("Enter search term (name, industry, or location): ").strip()
        if not keyword:
            print("Search term cannot be empty.")
            pause_for_user()
            return

        try:
            results = self.service.search_companies(keyword)
            print_table(COMPANY_HEADERS, _format_company_rows(results))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()

    def _handle_view_all(self) -> None:
        print("\n--- View All Companies ---")
        try:
            companies = self.service.get_all_companies()
            print_table(COMPANY_HEADERS, _format_company_rows(companies))
        except RPMSException as exc:
            print(f"Error: {exc}")
        finally:
            pause_for_user()
