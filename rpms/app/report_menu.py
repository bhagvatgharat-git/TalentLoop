"""Console submenu for analytical reports and recruitment metrics."""

from typing import Optional

from rpms.exception import RPMSException
from rpms.service.report_service import ReportService
from rpms.util.branding import APP_NAME
from rpms.util.table_printer import print_table


class ReportMenu:
    """Console user interface for management analytics and reports."""

    def __init__(self, service: Optional[ReportService] = None):
        self.service = service or ReportService()

    def show(self) -> None:
        """Display report menu loop."""
        while True:
            print(f"\n--- {APP_NAME} :: Analytics & Reports ---")
            print("1. Candidates by Technology")
            print("2. Open Jobs Report")
            print("3. Applications by Status")
            print("4. Company-wise Placements")
            print("5. Placed Candidates Report")
            print("6. Unplaced Candidates Report")
            print("7. Back to Main Menu")

            choice = input("Enter choice (1-7): ").strip()
            if choice == "1":
                self._handle_candidates_by_tech()
            elif choice == "2":
                self._handle_open_jobs()
            elif choice == "3":
                self._handle_apps_by_status()
            elif choice == "4":
                self._handle_company_placements()
            elif choice == "5":
                self._handle_placed_candidates()
            elif choice == "6":
                self._handle_unplaced_candidates()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please select an option from 1 to 7.")

    def _handle_candidates_by_tech(self) -> None:
        print("\n--- Report: Candidates by Technology ---")
        try:
            data = self.service.get_candidates_by_technology()
            headers = ["Technology", "Candidate Count"]
            rows = [[tech, count] for tech, count in data.items()]
            total_count = sum(data.values())
            total_row = ["TOTAL", total_count]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_open_jobs(self) -> None:
        print("\n--- Report: Open Jobs & Vacancies ---")
        try:
            jobs = self.service.get_open_jobs()
            headers = [
                "Job ID",
                "Company",
                "Job Title",
                "Technology",
                "Openings",
                "Package (LPA)",
                "Location",
                "Deadline",
            ]
            rows = [
                [
                    j["job_id"],
                    j["company_name"],
                    j["job_title"],
                    j["technology"],
                    j["openings"],
                    f"{j['package_lpa']:.2f}",
                    j["location"],
                    j["deadline"],
                ]
                for j in jobs
            ]
            total_openings = sum(j["openings"] for j in jobs)
            total_row = ["TOTAL OPENINGS", "", "", "", total_openings, "", "", ""]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_apps_by_status(self) -> None:
        print("\n--- Report: Applications by Workflow Status ---")
        try:
            data = self.service.get_applications_by_status()
            headers = ["Application Status", "Count"]
            rows = [[status, count] for status, count in data.items()]
            total_count = sum(data.values())
            total_row = ["TOTAL APPLICATIONS", total_count]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_company_placements(self) -> None:
        print("\n--- Report: Company-wise Placement Performance ---")
        try:
            companies = self.service.get_company_wise_placements()
            headers = [
                "Company ID",
                "Company Name",
                "Placements",
                "Avg Package (LPA)",
                "Highest Package (LPA)",
            ]
            rows = [
                [
                    c["company_id"],
                    c["company_name"],
                    c["placement_count"],
                    f"{c['avg_package']:.2f}",
                    f"{c['max_package']:.2f}",
                ]
                for c in companies
            ]
            total_placements = sum(c["placement_count"] for c in companies)
            active_companies = [c for c in companies if c["placement_count"] > 0]
            overall_avg = (
                sum(c["avg_package"] * c["placement_count"] for c in active_companies) / total_placements
                if total_placements > 0
                else 0.0
            )
            peak_pkg = max([c["max_package"] for c in companies], default=0.0)
            total_row = [
                "TOTAL",
                f"{len(companies)} Companies",
                total_placements,
                f"{overall_avg:.2f}",
                f"{peak_pkg:.2f}",
            ]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_placed_candidates(self) -> None:
        print("\n--- Report: Confirmed Placed Candidates ---")
        try:
            placed = self.service.get_placed_candidates()
            headers = [
                "Candidate ID",
                "Name",
                "Email",
                "Technology",
                "Company",
                "Designation",
                "Package (LPA)",
                "Joining Date",
            ]
            rows = [
                [
                    p["candidate_id"],
                    p["candidate_name"],
                    p["email"],
                    p["technology"],
                    p["company_name"],
                    p["designation"],
                    f"{p['package_lpa']:.2f}",
                    p["joining_date"],
                ]
                for p in placed
            ]
            avg_pkg = sum(p["package_lpa"] for p in placed) / len(placed) if placed else 0.0
            total_row = [
                "TOTAL PLACED",
                f"{len(placed)} Candidates",
                "",
                "",
                "",
                "",
                f"Avg: {avg_pkg:.2f}",
                "",
            ]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

    def _handle_unplaced_candidates(self) -> None:
        print("\n--- Report: Unplaced Active Candidates ---")
        try:
            unplaced = self.service.get_unplaced_candidates()
            headers = [
                "Candidate ID",
                "Name",
                "Email",
                "Mobile",
                "Technology",
                "Percentage",
                "Passing Year",
                "Backlogs",
            ]
            rows = [
                [
                    u["candidate_id"],
                    u["candidate_name"],
                    u["email"],
                    u["mobile"],
                    u["technology"],
                    f"{u['percentage']:.2f}%",
                    u["passing_year"],
                    u["backlog_count"],
                ]
                for u in unplaced
            ]
            total_row = [
                "TOTAL UNPLACED",
                f"{len(unplaced)} Candidates",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
            print_table(headers, rows + [total_row] if rows else [])
        except RPMSException as exc:
            print(f"Error: {exc}")

