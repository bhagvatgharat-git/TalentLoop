"""Job service handling business logic and vacancy validation."""

from datetime import date
from typing import List, Optional, Union

from rpms.dao.company_dao import CompanyDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception import CompanyNotFoundError, JobNotFoundError, ValidationError
from rpms.model.job import Job
from rpms.util.id_generator import generate_next_id
from rpms.util.logger import log_activity
from rpms.util.validators import (
    validate_future_date,
    validate_non_empty,
    validate_non_negative_int,
    validate_percentage,
    validate_positive_int,
)


class JobService:
    """Provides business logic for job vacancies and recruitment drives."""

    def __init__(
        self,
        job_dao: Optional[JobDAO] = None,
        company_dao: Optional[CompanyDAO] = None,
    ):
        self.job_dao = job_dao or JobDAO()
        self.company_dao = company_dao or CompanyDAO()

    def _validate_package_lpa(self, value: Union[float, int, str]) -> float:
        try:
            val = float(value)
        except (TypeError, ValueError) as exc:
            raise ValidationError("Package (LPA) must be a numeric value.") from exc
        if val < 0.0:
            raise ValidationError("Package (LPA) cannot be negative.")
        return round(val, 2)

    def create_job(
        self,
        company_id: str,
        job_title: str,
        technology: str,
        openings: int,
        location: str,
        package_lpa: float,
        min_percentage: float = 0.0,
        passing_year: int = 2024,
        max_backlogs: int = 0,
        deadline: Optional[Union[date, str]] = None,
    ) -> Job:
        """Validate criteria, verify company existence, generate ID, and post job."""
        clean_company_id = validate_non_empty(company_id, "Company ID").upper()
        company = self.company_dao.find_by_id(clean_company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID '{clean_company_id}' does not exist.")

        clean_title = validate_non_empty(job_title, "Job title")
        clean_tech = validate_non_empty(technology, "Technology")
        clean_openings = validate_positive_int(openings, "Openings count")
        clean_loc = validate_non_empty(location, "Location")
        clean_package = self._validate_package_lpa(package_lpa)
        clean_min_pct = validate_percentage(min_percentage)
        clean_year = validate_positive_int(passing_year, "Passing year")
        clean_backlogs = validate_non_negative_int(max_backlogs, "Maximum backlogs")
        clean_deadline = validate_future_date(deadline, "Deadline")

        job_id = generate_next_id("jobs")
        job = Job(
            job_id=job_id,
            company_id=clean_company_id,
            job_title=clean_title,
            technology=clean_tech,
            openings=clean_openings,
            location=clean_loc,
            package_lpa=clean_package,
            min_percentage=clean_min_pct,
            passing_year=clean_year,
            max_backlogs=clean_backlogs,
            deadline=clean_deadline,
            status="OPEN",
            company_name=company.name,
        )

        saved = self.job_dao.add(job)
        log_activity(f"Job Created: {job_id}")
        return saved

    def update_job(
        self,
        job_id: str,
        company_id: str,
        job_title: str,
        technology: str,
        openings: int,
        location: str,
        package_lpa: float,
        min_percentage: float,
        passing_year: int,
        max_backlogs: int,
        deadline: Union[date, str],
        status: str,
    ) -> Job:
        """Validate parameters, verify job and company existence, and update job."""
        clean_job_id = validate_non_empty(job_id, "Job ID").upper()
        existing = self.job_dao.find_by_id(clean_job_id)
        if not existing:
            raise JobNotFoundError(f"Job opening with ID '{clean_job_id}' does not exist.")

        clean_company_id = validate_non_empty(company_id, "Company ID").upper()
        company = self.company_dao.find_by_id(clean_company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID '{clean_company_id}' does not exist.")

        clean_title = validate_non_empty(job_title, "Job title")
        clean_tech = validate_non_empty(technology, "Technology")
        clean_openings = validate_positive_int(openings, "Openings count")
        clean_loc = validate_non_empty(location, "Location")
        clean_package = self._validate_package_lpa(package_lpa)
        clean_min_pct = validate_percentage(min_percentage)
        clean_year = validate_positive_int(passing_year, "Passing year")
        clean_backlogs = validate_non_negative_int(max_backlogs, "Maximum backlogs")
        clean_deadline = validate_future_date(deadline, "Deadline")
        clean_status = validate_non_empty(status, "Status").upper()
        if clean_status not in ("OPEN", "CLOSED"):
            raise ValidationError("Job status must be either 'OPEN' or 'CLOSED'.")

        updated_job = Job(
            job_id=clean_job_id,
            company_id=clean_company_id,
            job_title=clean_title,
            technology=clean_tech,
            openings=clean_openings,
            location=clean_loc,
            package_lpa=clean_package,
            min_percentage=clean_min_pct,
            passing_year=clean_year,
            max_backlogs=clean_backlogs,
            deadline=clean_deadline,
            status=clean_status,
            company_name=company.name,
        )

        self.job_dao.update(updated_job)
        log_activity(f"Job Updated: {clean_job_id}")
        return updated_job

    def get_job_by_id(self, job_id: str) -> Job:
        """Retrieve a job by ID or raise JobNotFoundError."""
        clean_id = validate_non_empty(job_id, "Job ID").upper()
        job = self.job_dao.find_by_id(clean_id)
        if not job:
            raise JobNotFoundError(f"Job opening with ID '{clean_id}' does not exist.")
        return job

    def get_open_jobs(self) -> List[Job]:
        """Fetch all currently open job postings with company name joined."""
        return self.job_dao.find_open_jobs()

    def close_job(self, job_id: str) -> bool:
        """Close an active job vacancy."""
        clean_id = validate_non_empty(job_id, "Job ID").upper()
        existing = self.job_dao.find_by_id(clean_id)
        if not existing:
            raise JobNotFoundError(f"Job opening with ID '{clean_id}' does not exist.")

        success = self.job_dao.close_job(clean_id)
        if success:
            log_activity(f"Job Closed: {clean_id}")
        return success

    def search_jobs(self, query: str) -> List[Job]:
        """Search job vacancies by title, technology, or location."""
        clean_query = validate_non_empty(query, "Search query")
        return self.job_dao.search(clean_query)

    def get_all_jobs(self) -> List[Job]:
        """Retrieve all job postings."""
        return self.job_dao.get_all()
