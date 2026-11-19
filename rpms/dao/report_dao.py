"""Report Data Access Object executing analytical and aggregation queries."""

from typing import Any, Dict, List, Tuple

from rpms.util.db_connection import get_connection


class ReportDAO:
    """Executes aggregation and relational join queries for analytics and reports."""

    def get_candidate_count_by_technology(self) -> List[Tuple[str, int]]:
        """Return candidate counts grouped by primary technology."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT technology, COUNT(*) AS count "
                "FROM candidates "
                "WHERE is_active = 1 "
                "GROUP BY technology "
                "ORDER BY count DESC, technology ASC"
            )
            cursor.execute(query)
            return [(str(row[0]), int(row[1])) for row in cursor.fetchall()]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_open_jobs_report(self) -> List[Dict[str, Any]]:
        """Retrieve all currently active job postings with joined company names."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT j.job_id, c.name AS company_name, j.job_title, "
                "j.technology, j.openings, j.package_lpa, j.location, j.deadline "
                "FROM jobs j "
                "JOIN companies c ON j.company_id = c.company_id "
                "WHERE j.status = 'OPEN' "
                "ORDER BY j.job_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                {
                    "job_id": row[0],
                    "company_name": row[1],
                    "job_title": row[2],
                    "technology": row[3],
                    "openings": int(row[4]),
                    "package_lpa": float(row[5]),
                    "location": row[6],
                    "deadline": str(row[7]),
                }
                for row in rows
            ]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_application_count_by_status(self) -> List[Tuple[str, int]]:
        """Return application counts grouped by status."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT status, COUNT(*) AS count "
                "FROM applications "
                "GROUP BY status "
                "ORDER BY count DESC, status ASC"
            )
            cursor.execute(query)
            return [(str(row[0]), int(row[1])) for row in cursor.fetchall()]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_company_wise_placements(self) -> List[Dict[str, Any]]:
        """Return placement statistics grouped by company."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT c.company_id, c.name, COUNT(p.placement_id) AS placement_count, "
                "COALESCE(AVG(p.final_package_lpa), 0.0) AS avg_package, "
                "COALESCE(MAX(p.final_package_lpa), 0.0) AS max_package "
                "FROM companies c "
                "LEFT JOIN placements p ON c.company_id = p.company_id "
                "GROUP BY c.company_id, c.name "
                "ORDER BY placement_count DESC, c.name ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                {
                    "company_id": row[0],
                    "company_name": row[1],
                    "placement_count": int(row[2]),
                    "avg_package": round(float(row[3]), 2),
                    "max_package": round(float(row[4]), 2),
                }
                for row in rows
            ]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_placed_candidates_report(self) -> List[Dict[str, Any]]:
        """Return details of all placed candidates who joined partner companies."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT c.candidate_id, c.name, c.email, c.technology, "
                "comp.name AS company_name, p.designation, p.final_package_lpa, p.actual_joining_date "
                "FROM placements p "
                "JOIN applications a ON p.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN companies comp ON p.company_id = comp.company_id "
                "ORDER BY p.actual_joining_date DESC, c.candidate_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                {
                    "candidate_id": row[0],
                    "candidate_name": row[1],
                    "email": row[2],
                    "technology": row[3],
                    "company_name": row[4],
                    "designation": row[5],
                    "package_lpa": float(row[6]),
                    "joining_date": str(row[7]),
                }
                for row in rows
            ]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_unplaced_candidates_report(self) -> List[Dict[str, Any]]:
        """Return active candidates with no JOINED application."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT c.candidate_id, c.name, c.email, c.mobile, "
                "c.technology, c.percentage, c.passing_year, c.backlog_count "
                "FROM candidates c "
                "WHERE c.is_active = 1 "
                "AND c.candidate_id NOT IN ("
                "    SELECT a.candidate_id FROM applications a WHERE a.status = 'JOINED'"
                ") "
                "ORDER BY c.candidate_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                {
                    "candidate_id": row[0],
                    "candidate_name": row[1],
                    "email": row[2],
                    "mobile": row[3],
                    "technology": row[4],
                    "percentage": float(row[5]),
                    "passing_year": int(row[6]),
                    "backlog_count": int(row[7]),
                }
                for row in rows
            ]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
