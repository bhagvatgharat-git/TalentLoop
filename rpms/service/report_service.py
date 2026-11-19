"""Report service aggregating analytics and placement performance data."""

from typing import Any, Dict, List, Optional

from rpms.dao.report_dao import ReportDAO


class ReportService:
    """Provides analytical reports and key recruitment metrics."""

    def __init__(self, report_dao: Optional[ReportDAO] = None):
        self.report_dao = report_dao or ReportDAO()

    def get_candidates_by_technology(self) -> Dict[str, int]:
        """Aggregate active candidates grouped by technology stack."""
        raw_tuples = self.report_dao.get_candidate_count_by_technology()
        return {tech: count for tech, count in raw_tuples}

    def get_open_jobs(self) -> List[Dict[str, Any]]:
        """Retrieve all currently active job postings with vacancies."""
        return self.report_dao.get_open_jobs_report()

    def get_applications_by_status(self) -> Dict[str, int]:
        """Aggregate candidate applications grouped by workflow status."""
        raw_tuples = self.report_dao.get_application_count_by_status()
        return {status: count for status, count in raw_tuples}

    def get_company_wise_placements(self) -> List[Dict[str, Any]]:
        """Retrieve placement totals, average, and peak package metrics by company."""
        return self.report_dao.get_company_wise_placements()

    def get_placed_candidates(self) -> List[Dict[str, Any]]:
        """Retrieve comprehensive list of students who secured placements."""
        return self.report_dao.get_placed_candidates_report()

    def get_unplaced_candidates(self) -> List[Dict[str, Any]]:
        """Retrieve active candidates who have not yet secured a placement."""
        return self.report_dao.get_unplaced_candidates_report()
