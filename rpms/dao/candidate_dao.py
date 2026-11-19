"""Candidate Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.candidate import Candidate
from rpms.util.db_connection import get_connection


class CandidateDAO:
    """Performs database operations for candidates using parameterized queries."""

    @staticmethod
    def _map_row_to_candidate(row) -> Optional[Candidate]:
        if not row:
            return None
        return Candidate(
            candidate_id=row[0],
            name=row[1],
            email=row[2],
            mobile=row[3],
            technology=row[4],
            percentage=float(row[5]),
            passing_year=int(row[6]),
            backlog_count=int(row[7]),
            is_active=int(row[8]),
            created_at=row[9],
        )

    def add(self, candidate: Candidate) -> Candidate:
        """Insert a new candidate into the database."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO candidates ("
                "candidate_id, name, email, mobile, technology, "
                "percentage, passing_year, backlog_count, is_active"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            params = (
                candidate.candidate_id,
                candidate.name,
                candidate.email,
                candidate.mobile,
                candidate.technology,
                candidate.percentage,
                candidate.passing_year,
                candidate.backlog_count,
                candidate.is_active,
            )
            cursor.execute(query, params)
            conn.commit()
            return candidate
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update(self, candidate: Candidate) -> bool:
        """Update an existing candidate's details."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "UPDATE candidates SET "
                "name = %s, email = %s, mobile = %s, technology = %s, "
                "percentage = %s, passing_year = %s, backlog_count = %s, is_active = %s "
                "WHERE candidate_id = %s"
            )
            params = (
                candidate.name,
                candidate.email,
                candidate.mobile,
                candidate.technology,
                candidate.percentage,
                candidate.passing_year,
                candidate.backlog_count,
                candidate.is_active,
                candidate.candidate_id,
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_id(self, candidate_id: str) -> Optional[Candidate]:
        """Retrieve a candidate by primary key identifier."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT candidate_id, name, email, mobile, technology, "
                "percentage, passing_year, backlog_count, is_active, created_at "
                "FROM candidates WHERE candidate_id = %s"
            )
            cursor.execute(query, (candidate_id,))
            row = cursor.fetchone()
            return self._map_row_to_candidate(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_email(self, email: str) -> Optional[Candidate]:
        """Retrieve a candidate by email address."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT candidate_id, name, email, mobile, technology, "
                "percentage, passing_year, backlog_count, is_active, created_at "
                "FROM candidates WHERE email = %s"
            )
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            return self._map_row_to_candidate(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_mobile(self, mobile: str) -> Optional[Candidate]:
        """Retrieve a candidate by mobile number."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT candidate_id, name, email, mobile, technology, "
                "percentage, passing_year, backlog_count, is_active, created_at "
                "FROM candidates WHERE mobile = %s"
            )
            cursor.execute(query, (mobile,))
            row = cursor.fetchone()
            return self._map_row_to_candidate(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def search(self, query: str) -> List[Candidate]:
        """Search candidates by name or technology."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = (
                "SELECT candidate_id, name, email, mobile, technology, "
                "percentage, passing_year, backlog_count, is_active, created_at "
                "FROM candidates "
                "WHERE name LIKE %s OR technology LIKE %s "
                "ORDER BY candidate_id ASC"
            )
            pattern = f"%{query.strip()}%"
            cursor.execute(sql, (pattern, pattern))
            rows = cursor.fetchall()
            return [self._map_row_to_candidate(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_all(self, active_only: bool = True) -> List[Candidate]:
        """Retrieve all candidates, optionally filtering by active status."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            if active_only:
                sql = (
                    "SELECT candidate_id, name, email, mobile, technology, "
                    "percentage, passing_year, backlog_count, is_active, created_at "
                    "FROM candidates WHERE is_active = 1 "
                    "ORDER BY candidate_id ASC"
                )
            else:
                sql = (
                    "SELECT candidate_id, name, email, mobile, technology, "
                    "percentage, passing_year, backlog_count, is_active, created_at "
                    "FROM candidates ORDER BY candidate_id ASC"
                )
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._map_row_to_candidate(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def deactivate(self, candidate_id: str) -> bool:
        """Deactivate candidate by setting is_active to 0."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE candidates SET is_active = 0 WHERE candidate_id = %s"
            cursor.execute(query, (candidate_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

