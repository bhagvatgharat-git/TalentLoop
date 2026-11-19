"""Company Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.company import Company
from rpms.util.db_connection import get_connection


class CompanyDAO:
    """Performs database operations for companies using parameterized queries."""

    @staticmethod
    def _map_row_to_company(row) -> Optional[Company]:
        if not row:
            return None
        return Company(
            company_id=row[0],
            name=row[1],
            industry=row[2],
            location=row[3],
            contact_person=row[4],
            contact_email=row[5],
            created_at=row[6],
        )

    def add(self, company: Company) -> Company:
        """Insert a new company into the database."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO companies ("
                "company_id, name, industry, location, contact_person, contact_email"
                ") VALUES (%s, %s, %s, %s, %s, %s)"
            )
            params = (
                company.company_id,
                company.name,
                company.industry,
                company.location,
                company.contact_person,
                company.contact_email,
            )
            cursor.execute(query, params)
            conn.commit()
            return company
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update(self, company: Company) -> bool:
        """Update an existing company record."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "UPDATE companies SET "
                "name = %s, industry = %s, location = %s, "
                "contact_person = %s, contact_email = %s "
                "WHERE company_id = %s"
            )
            params = (
                company.name,
                company.industry,
                company.location,
                company.contact_person,
                company.contact_email,
                company.company_id,
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_id(self, company_id: str) -> Optional[Company]:
        """Retrieve a company by primary key identifier."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT company_id, name, industry, location, contact_person, contact_email, created_at "
                "FROM companies WHERE company_id = %s"
            )
            cursor.execute(query, (company_id,))
            row = cursor.fetchone()
            return self._map_row_to_company(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_name(self, name: str) -> Optional[Company]:
        """Retrieve a company by exact name."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT company_id, name, industry, location, contact_person, contact_email, created_at "
                "FROM companies WHERE name = %s"
            )
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            return self._map_row_to_company(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def search(self, query: str) -> List[Company]:
        """Search companies by name, industry, or location."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = (
                "SELECT company_id, name, industry, location, contact_person, contact_email, created_at "
                "FROM companies "
                "WHERE name LIKE %s OR industry LIKE %s OR location LIKE %s "
                "ORDER BY company_id ASC"
            )
            pattern = f"%{query.strip()}%"
            cursor.execute(sql, (pattern, pattern, pattern))
            rows = cursor.fetchall()
            return [self._map_row_to_company(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_all(self) -> List[Company]:
        """Retrieve all registered companies."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = (
                "SELECT company_id, name, industry, location, contact_person, contact_email, created_at "
                "FROM companies ORDER BY company_id ASC"
            )
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._map_row_to_company(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

