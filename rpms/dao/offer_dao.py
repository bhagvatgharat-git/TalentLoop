"""Offer Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.offer import Offer
from rpms.util.db_connection import get_connection


class OfferDAO:
    """Performs database operations for candidate offers using parameterized queries."""

    @staticmethod
    def _map_row_to_offer(row) -> Optional[Offer]:
        if not row:
            return None
        candidate_name = row[8] if len(row) > 8 else None
        company_name = row[9] if len(row) > 9 else None
        job_title = row[10] if len(row) > 10 else None
        return Offer(
            offer_id=row[0],
            application_id=row[1],
            designation=row[2],
            package_lpa=float(row[3]),
            offer_date=row[4],
            joining_date=row[5],
            offer_status=row[6],
            created_at=row[7],
            candidate_name=candidate_name,
            company_name=company_name,
            job_title=job_title,
        )

    def add(self, offer: Offer, connection: Optional[object] = None) -> Offer:
        """Insert a new job offer."""
        owns_conn = connection is None
        conn = get_connection() if owns_conn else connection
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO offers ("
                "offer_id, application_id, designation, package_lpa, "
                "offer_date, joining_date, offer_status"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            params = (
                offer.offer_id,
                offer.application_id,
                offer.designation,
                offer.package_lpa,
                offer.offer_date,
                offer.joining_date,
                offer.offer_status,
            )
            cursor.execute(query, params)
            if owns_conn:
                conn.commit()
            return offer
        finally:
            if cursor is not None:
                cursor.close()
            if owns_conn and conn is not None:
                conn.close()

    def update_status(self, offer_id: str, status: str, connection: Optional[object] = None) -> bool:
        """Update offer status (OFFERED/ACCEPTED/DECLINED)."""
        owns_conn = connection is None
        conn = get_connection() if owns_conn else connection
        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE offers SET offer_status = %s WHERE offer_id = %s"
            cursor.execute(query, (status, offer_id))
            if owns_conn:
                conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if owns_conn and conn is not None:
                conn.close()

    def find_by_id(self, offer_id: str) -> Optional[Offer]:
        """Retrieve an offer by ID with candidate and company details joined."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT o.offer_id, o.application_id, o.designation, o.package_lpa, "
                "o.offer_date, o.joining_date, o.offer_status, o.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM offers o "
                "JOIN applications a ON o.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "WHERE o.offer_id = %s"
            )
            cursor.execute(query, (offer_id,))
            row = cursor.fetchone()
            return self._map_row_to_offer(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_application(self, application_id: str) -> Optional[Offer]:
        """Retrieve the offer issued for an application."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT o.offer_id, o.application_id, o.designation, o.package_lpa, "
                "o.offer_date, o.joining_date, o.offer_status, o.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM offers o "
                "JOIN applications a ON o.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "WHERE o.application_id = %s"
            )
            cursor.execute(query, (application_id,))
            row = cursor.fetchone()
            return self._map_row_to_offer(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_all(self) -> List[Offer]:
        """Retrieve all issued offers."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT o.offer_id, o.application_id, o.designation, o.package_lpa, "
                "o.offer_date, o.joining_date, o.offer_status, o.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, j.job_title "
                "FROM offers o "
                "JOIN applications a ON o.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "ORDER BY o.offer_id ASC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_row_to_offer(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

