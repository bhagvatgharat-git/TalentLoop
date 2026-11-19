"""Company service handling business logic and input validation."""

from typing import List, Optional

from rpms.dao.company_dao import CompanyDAO
from rpms.exception import CompanyNotFoundError, ValidationError
from rpms.model.company import Company
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import validate_email, validate_non_empty


class CompanyService:
    """Provides business logic for company registration, updates, and searches."""

    def __init__(self, company_dao: Optional[CompanyDAO] = None):
        self.company_dao = company_dao or CompanyDAO()

    def create_company(
        self,
        name: str,
        industry: str,
        location: str,
        contact_person: str,
        contact_email: str,
    ) -> Company:
        """Validate input, verify name uniqueness, generate ID, and save company."""
        clean_name = validate_non_empty(name, "Company name")
        clean_industry = validate_non_empty(industry, "Industry")
        clean_location = validate_non_empty(location, "Location")
        clean_contact_person = validate_non_empty(contact_person, "Contact person")
        clean_email = validate_email(contact_email)

        if self.company_dao.find_by_name(clean_name):
            raise ValidationError(f"A company named '{clean_name}' already exists.")

        company_id = generate_next_id("companies")
        company = Company(
            company_id=company_id,
            name=clean_name,
            industry=clean_industry,
            location=clean_location,
            contact_person=clean_contact_person,
            contact_email=clean_email,
        )

        saved = self.company_dao.add(company)
        log_activity(f"Company Created: {company_id}")
        return saved

    def update_company(
        self,
        company_id: str,
        name: str,
        industry: str,
        location: str,
        contact_person: str,
        contact_email: str,
    ) -> Company:
        """Validate input, verify existence, check uniqueness, and update company."""
        clean_id = validate_non_empty(company_id, "Company ID").upper()
        existing = self.company_dao.find_by_id(clean_id)
        if not existing:
            raise CompanyNotFoundError(f"Company with ID '{clean_id}' does not exist.")

        clean_name = validate_non_empty(name, "Company name")
        clean_industry = validate_non_empty(industry, "Industry")
        clean_location = validate_non_empty(location, "Location")
        clean_contact_person = validate_non_empty(contact_person, "Contact person")
        clean_email = validate_email(contact_email)

        existing_by_name = self.company_dao.find_by_name(clean_name)
        if existing_by_name and existing_by_name.company_id != clean_id:
            raise ValidationError(f"Company name '{clean_name}' is already in use by another company.")

        updated_company = Company(
            company_id=clean_id,
            name=clean_name,
            industry=clean_industry,
            location=clean_location,
            contact_person=clean_contact_person,
            contact_email=clean_email,
        )

        self.company_dao.update(updated_company)
        log_activity(f"Company Updated: {clean_id}")
        return updated_company

    def get_company_by_id(self, company_id: str) -> Company:
        """Fetch company by ID or raise CompanyNotFoundError."""
        clean_id = validate_non_empty(company_id, "Company ID").upper()
        company = self.company_dao.find_by_id(clean_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID '{clean_id}' does not exist.")
        return company

    def search_companies(self, query: str) -> List[Company]:
        """Search companies by name, industry, or location."""
        clean_query = validate_non_empty(query, "Search query")
        return self.company_dao.search(clean_query)

    def get_all_companies(self) -> List[Company]:
        """Retrieve list of all registered companies."""
        return self.company_dao.get_all()

