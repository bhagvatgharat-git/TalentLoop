"""Placement Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.placement import Placement
from rpms.util.db_connection import get_connection


class PlacementDAO:
    """Performs database operations for confirmed placements using parameterized queries."""

    @staticmethod
    def _map_row_to_placement(row) -> Optional[Placement]:
        if not row:
            return None
        candidate_name = row[8] if len(row) > 8 else None
        company_name = row[9] if len(row) > 9 else None
        job_title = row[10] if len(row) > 10 else None
        return Placement(
            placement_id=row[0],
            application_id=row[1],
            company_id=row[2],
            designation=row[3],
            final_package_lpa=float(row[4]),
            actual_joining_date=row[5],
            joining_status=row[6],
            created_at=row[7],
            candidate_name=candidate_name,
            company_name=company_name,
            job_title=job_title,
        )

    def add(self, placement: Placement, connection: Optional[object] = None) -> Placement:
        """Insert a new placement record."""
        owns_conn = connection is None
        conn = get_connection() if owns_conn else connection
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO placements ("
                "placement_id, application_id, company_id, designation, "
                "final_package_lpa, actual_joining_date, joining_status"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            params = (
                placement.placement_id,
                placement.application_id,
                placement.company_id,
                placement.designation,
                placement.final_package_lpa,
                placement.actual_joining_date,
                placement.joining_status,
            )
            cursor.execute(query, params)
            if owns_conn:
                conn.commit()
            return placement
        finally:
            if cursor is not None:
                cursor.close()
            if owns_conn and conn is not None:
                conn.close()

    def find_by_id(self, placement_id: str) -> Optional[Placement]:
        """Retrieve a placement by ID with candidate and company details joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT p.placement_id, p.application_id, p.company_id, p.designation, "
                "p.final_package_lpa, p.actual_joining_date, p.joining_status, p.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM placements p "
                "JOIN applications a ON p.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON p.company_id = comp.company_id "
                "WHERE p.placement_id = %s"
            )
            cursor.execute(query, (placement_id,))
            row = cursor.fetchone()
            return self._map_row_to_placement(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_application(self, application_id: str) -> Optional[Placement]:
        """Retrieve placement record for an application."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT p.placement_id, p.application_id, p.company_id, p.designation, "
                "p.final_package_lpa, p.actual_joining_date, p.joining_status, p.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM placements p "
                "JOIN applications a ON p.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON p.company_id = comp.company_id "
                "WHERE p.application_id = %s"
            )
            cursor.execute(query, (application_id,))
            row = cursor.fetchone()
            return self._map_row_to_placement(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_all(self) -> List[Placement]:
        """Retrieve all placement records."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT p.placement_id, p.application_id, p.company_id, p.designation, "
                "p.final_package_lpa, p.actual_joining_date, p.joining_status, p.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM placements p "
                "JOIN applications a ON p.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON p.company_id = comp.company_id "
                "ORDER BY p.placement_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_row_to_placement(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_by_company(self, company_id: str) -> List[Placement]:
        """Retrieve all placements made at a specific company."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT p.placement_id, p.application_id, p.company_id, p.designation, "
                "p.final_package_lpa, p.actual_joining_date, p.joining_status, p.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM placements p "
                "JOIN applications a ON p.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON p.company_id = comp.company_id "
                "WHERE p.company_id = %s "
                "ORDER BY p.placement_id ASC"
            )
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_placement(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

