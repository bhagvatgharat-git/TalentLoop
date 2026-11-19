"""Interview Data Access Object handling SQL operations."""

from typing import List, Optional

from rpms.model.interview import Interview
from rpms.model.interview_feedback import InterviewFeedback
from rpms.util.db_connection import get_connection


class InterviewDAO:
    """Performs database operations for interview rounds and feedback using parameterized queries."""

    @staticmethod
    def _map_row_to_interview(row) -> Optional[Interview]:
        if not row:
            return None
        candidate_name = row[8] if len(row) > 8 else None
        company_name = row[9] if len(row) > 9 else None
        job_title = row[10] if len(row) > 10 else None
        feedback_result = row[11] if len(row) > 11 else None
        return Interview(
            interview_id=row[0],
            application_id=row[1],
            round_no=int(row[2]),
            interview_date=row[3],
            mode=row[4],
            interviewer=row[5],
            status=row[6],
            created_at=row[7],
            candidate_name=candidate_name,
            company_name=company_name,
            job_title=job_title,
            feedback_result=feedback_result,
        )

    @staticmethod
    def _map_row_to_feedback(row) -> Optional[InterviewFeedback]:
        if not row:
            return None
        return InterviewFeedback(
            feedback_id=row[0],
            interview_id=row[1],
            technical_rating=int(row[2]),
            communication_rating=int(row[3]),
            remarks=row[4],
            result=row[5],
            created_at=row[6],
        )

    def add_interview(self, interview: Interview) -> Interview:
        """Insert a new interview round."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO interviews ("
                "interview_id, application_id, round_no, interview_date, mode, interviewer, status"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            params = (
                interview.interview_id,
                interview.application_id,
                interview.round_no,
                interview.interview_date,
                interview.mode,
                interview.interviewer,
                interview.status,
            )
            cursor.execute(query, params)
            conn.commit()
            return interview
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update_status(self, interview_id: str, new_status: str) -> bool:
        """Update interview session status."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE interviews SET status = %s WHERE interview_id = %s"
            cursor.execute(query, (new_status, interview_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_id(self, interview_id: str) -> Optional[Interview]:
        """Retrieve interview by ID with joined candidate, company, and feedback details."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT i.interview_id, i.application_id, i.round_no, i.interview_date, "
                "i.mode, i.interviewer, i.status, i.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, "
                "j.job_title, fb.result AS feedback_result "
                "FROM interviews i "
                "JOIN applications a ON i.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "LEFT JOIN interview_feedback fb ON i.interview_id = fb.interview_id "
                "WHERE i.interview_id = %s"
            )
            cursor.execute(query, (interview_id,))
            row = cursor.fetchone()
            return self._map_row_to_interview(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_application(self, application_id: str) -> List[Interview]:
        """Retrieve all interview rounds for a specific application."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT i.interview_id, i.application_id, i.round_no, i.interview_date, "
                "i.mode, i.interviewer, i.status, i.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, "
                "j.job_title, fb.result AS feedback_result "
                "FROM interviews i "
                "JOIN applications a ON i.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "LEFT JOIN interview_feedback fb ON i.interview_id = fb.interview_id "
                "WHERE i.application_id = %s "
                "ORDER BY i.round_no ASC"
            )
            cursor.execute(query, (application_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_interview(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_candidate(self, candidate_id: str) -> List[Interview]:
        """Retrieve all interviews associated with a candidate."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT i.interview_id, i.application_id, i.round_no, i.interview_date, "
                "i.mode, i.interviewer, i.status, i.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, "
                "j.job_title, fb.result AS feedback_result "
                "FROM interviews i "
                "JOIN applications a ON i.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "LEFT JOIN interview_feedback fb ON i.interview_id = fb.interview_id "
                "WHERE a.candidate_id = %s "
                "ORDER BY i.interview_date DESC, i.round_no ASC"
            )
            cursor.execute(query, (candidate_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_interview(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def find_by_company(self, company_id: str) -> List[Interview]:
        """Retrieve all interviews associated with a company."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT i.interview_id, i.application_id, i.round_no, i.interview_date, "
                "i.mode, i.interviewer, i.status, i.created_at, "
                "c.name AS candidate_name, comp.name AS company_name, "
                "j.job_title, fb.result AS feedback_result "
                "FROM interviews i "
                "JOIN applications a ON i.application_id = a.application_id "
                "JOIN candidates c ON a.candidate_id = c.candidate_id "
                "JOIN jobs j ON a.job_id = j.job_id "
                "JOIN companies comp ON j.company_id = comp.company_id "
                "LEFT JOIN interview_feedback fb ON i.interview_id = fb.interview_id "
                "WHERE comp.company_id = %s "
                "ORDER BY i.interview_date DESC, i.round_no ASC"
            )
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            return [self._map_row_to_interview(row) for row in rows if row]
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def add_feedback(self, feedback: InterviewFeedback) -> InterviewFeedback:
        """Insert feedback evaluation for an interview round."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "INSERT INTO interview_feedback ("
                "feedback_id, interview_id, technical_rating, communication_rating, remarks, result"
                ") VALUES (%s, %s, %s, %s, %s, %s)"
            )
            params = (
                feedback.feedback_id,
                feedback.interview_id,
                feedback.technical_rating,
                feedback.communication_rating,
                feedback.remarks,
                feedback.result,
            )
            cursor.execute(query, params)
            conn.commit()
            return feedback
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_feedback_by_interview_id(self, interview_id: str) -> Optional[InterviewFeedback]:
        """Retrieve feedback recorded for an interview round."""
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = (
                "SELECT feedback_id, interview_id, technical_rating, "
                "communication_rating, remarks, result, created_at "
                "FROM interview_feedback WHERE interview_id = %s"
            )
            cursor.execute(query, (interview_id,))
            row = cursor.fetchone()
            return self._map_row_to_feedback(row)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
