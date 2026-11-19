"""Application Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.application import Application
from rpms.util.db_connection import get_connection


class ApplicationDAO:
    """Performs database operations for applications using parameterized queries."""

    @staticmethod
    def _map_row_to_application(row) -> Optional[Application]:
        if not row:
            return None
        candidate_name = row[6] if len(row) > 6 else None
        job_title = row[7] if len(row) > 7 else None
        return Application(
            application_id=row[0],
            candidate_id=row[1],
            job_id=row[2],
            applied_date=row[3],
            status=row[4],
            created_at=row[5],
            candidate_name=candidate_name,
            job_title=job_title,
        )

    def add(self, application: Application) -> Application:
        """Insert a new application into the database."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO applications ("
                "application_id, candidate_id, job_id, applied_date, status"
                ") VALUES (%s, %s, %s, %s, %s)"
            )
            params = (
                application.application_id,
                application.candidate_id,
                application.job_id,
                application.applied_date,
                application.status,
            )
            cursor.execute(query, params)
            conn.commit()
            return application
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update_status(self, application_id: str, new_status: str) -> bool:
        """Update status of an existing application."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE applications SET status = %s WHERE application_id = %s"
            cursor.execute(query, (new_status, application_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_id(self, application_id: str) -> Optional[Application]:
        """Retrieve an application by ID with candidate and job details joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "WHERE a.application_id = %s"
            )
            cursor.execute(query, (application_id,))
            row = cursor.fetchone()
            return self._map_row_to_application(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_candidate_and_job(self, candidate_id: str, job_id: str) -> Optional[Application]:
        """Find an application by candidate ID and job ID combination."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "WHERE a.candidate_id = %s AND a.job_id = %s"
            )
            cursor.execute(query, (candidate_id, job_id))
            row = cursor.fetchone()
            return self._map_row_to_application(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_job(self, job_id: str) -> List[Application]:
        """Retrieve all applications for a specific job."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "WHERE a.job_id = %s "
                "ORDER BY a.application_id ASC"
            )
            cursor.execute(query, (job_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_application(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_candidate(self, candidate_id: str) -> List[Application]:
        """Retrieve all applications submitted by a specific candidate."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "WHERE a.candidate_id = %s "
                "ORDER BY a.application_id ASC"
            )
            cursor.execute(query, (candidate_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_application(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_status(self, status: str) -> List[Application]:
        """Retrieve all applications currently in a specific status."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "WHERE a.status = %s "
                "ORDER BY a.application_id ASC"
            )
            cursor.execute(query, (status,))
            rows = cursor.fetchall()
            return [self._map_row_to_application(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_all(self) -> List[Application]:
        """Retrieve all applications."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT a.application_id, a.candidate_id, a.job_id, a.applied_date, "
                "a.status, a.created_at, c.name AS candidate_name, j.job_title "
                "FROM applications a "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "ORDER BY a.application_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_row_to_application(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
