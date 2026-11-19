"""Job Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.job import Job
from rpms.util.db_connection import get_connection


class JobDAO:
    """Performs database operations for jobs using parameterized queries."""

    @staticmethod
    def _map_row_to_job(row) -> Optional[Job]:
        if not row:
            return None
        company_name = row[13] if len(row) > 13 else None
        return Job(
            job_id=row[0],
            company_id=row[1],
            job_title=row[2],
            technology=row[3],
            openings=int(row[4]),
            location=row[5],
            package_lpa=float(row[6]),
            min_percentage=float(row[7]),
            passing_year=int(row[8]),
            max_backlogs=int(row[9]),
            deadline=row[10],
            status=row[11],
            created_at=row[12],
            company_name=company_name,
        )

    def add(self, job: Job) -> Job:
        """Insert a new job opening into the database."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO jobs ("
                "job_id, company_id, job_title, technology, openings, "
                "location, package_lpa, min_percentage, passing_year, "
                "max_backlogs, deadline, status"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            params = (
                job.job_id,
                job.company_id,
                job.job_title,
                job.technology,
                job.openings,
                job.location,
                job.package_lpa,
                job.min_percentage,
                job.passing_year,
                job.max_backlogs,
                job.deadline,
                job.status,
            )
            cursor.execute(query, params)
            conn.commit()
            return job
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update(self, job: Job) -> bool:
        """Update an existing job opening."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "UPDATE jobs SET "
                "company_id = %s, job_title = %s, technology = %s, openings = %s, "
                "location = %s, package_lpa = %s, min_percentage = %s, "
                "passing_year = %s, max_backlogs = %s, deadline = %s, status = %s "
                "WHERE job_id = %s"
            )
            params = (
                job.company_id,
                job.job_title,
                job.technology,
                job.openings,
                job.location,
                job.package_lpa,
                job.min_percentage,
                job.passing_year,
                job.max_backlogs,
                job.deadline,
                job.status,
                job.job_id,
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_id(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by primary key with company name joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT j.job_id, j.company_id, j.job_title, j.technology, j.openings, "
                "j.location, j.package_lpa, j.min_percentage, j.passing_year, "
                "j.max_backlogs, j.deadline, j.status, j.created_at, c.name AS company_name "
                "FROM jobs j "
                "JOIN companies c ON j.company_id = c.company_id "
                "WHERE j.job_id = %s"
            )
            cursor.execute(query, (job_id,))
            row = cursor.fetchone()
            return self._map_row_to_job(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_open_jobs(self) -> List[Job]:
        """Retrieve all open jobs with company name joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT j.job_id, j.company_id, j.job_title, j.technology, j.openings, "
                "j.location, j.package_lpa, j.min_percentage, j.passing_year, "
                "j.max_backlogs, j.deadline, j.status, j.created_at, c.name AS company_name "
                "FROM jobs j "
                "JOIN companies c ON j.company_id = c.company_id "
                "WHERE j.status = 'OPEN' "
                "ORDER BY j.job_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_row_to_job(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def search(self, query: str) -> List[Job]:
        """Search jobs by title, technology, or location with company name joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = (
                "SELECT j.job_id, j.company_id, j.job_title, j.technology, j.openings, "
                "j.location, j.package_lpa, j.min_percentage, j.passing_year, "
                "j.max_backlogs, j.deadline, j.status, j.created_at, c.name AS company_name "
                "FROM jobs j "
                "JOIN companies c ON j.company_id = c.company_id "
                "WHERE j.job_title LIKE %s OR j.technology LIKE %s OR j.location LIKE %s "
                "ORDER BY j.job_id ASC"
            )
            pattern = f"%{query.strip()}%"
            cursor.execute(sql, (pattern, pattern, pattern))
            rows = cursor.fetchall()
            return [self._map_row_to_job(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def close_job(self, job_id: str) -> bool:
        """Mark a job opening as CLOSED."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE jobs SET status = 'CLOSED' WHERE job_id = %s"
            cursor.execute(query, (job_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def decrement_openings(self, job_id: str, connection: Optional[object] = None) -> int:
        """Reduce job openings count by 1 and auto-close when reaching zero."""
        owns_conn = connection is None
        conn = get_connection() if owns_conn else connection
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE jobs SET openings = openings - 1 WHERE job_id = %s", (job_id,))
            cursor.execute("UPDATE jobs SET status = 'CLOSED' WHERE job_id = %s AND openings <= 0", (job_id,))
            cursor.execute("SELECT openings FROM jobs WHERE job_id = %s", (job_id,))
            row = cursor.fetchone()
            remaining = int(row[0]) if row else 0
            if owns_conn:
                conn.commit()
            return remaining
        finally:
            if cursor is not None:
                cursor.close()
            if owns_conn and conn is not None:
                conn.close()

    def get_all(self) -> List[Job]:
        """Retrieve all jobs with company name joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT j.job_id, j.company_id, j.job_title, j.technology, j.openings, "
                "j.location, j.package_lpa, j.min_percentage, j.passing_year, "
                "j.max_backlogs, j.deadline, j.status, j.created_at, c.name AS company_name "
                "FROM jobs j "
                "JOIN companies c ON j.company_id = c.company_id "
                "ORDER BY j.job_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_row_to_job(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

