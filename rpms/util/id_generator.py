"""Database ID generator utility."""

from typing import Optional

from rpms.exception import ValidationError
from rpms.util.db_connection import get_connection

TABLE_CONFIG = {
    "candidates": {"id_col": "candidate_id", "prefix": "CAN", "start": 1001},
    "companies": {"id_col": "company_id", "prefix": "COM", "start": 101},
    "jobs": {"id_col": "job_id", "prefix": "JOB", "start": 101},
    "applications": {"id_col": "application_id", "prefix": "APP", "start": 501},
    "interviews": {"id_col": "interview_id", "prefix": "INT", "start": 101},
    "interview_feedback": {"id_col": "feedback_id", "prefix": "FB", "start": 101},
    "offers": {"id_col": "offer_id", "prefix": "OFF", "start": 101},
    "placements": {"id_col": "placement_id", "prefix": "PLC", "start": 101},
}


def generate_next_id(table_name: str, connection: Optional[object] = None) -> str:
    """Generate the next formatted primary key identifier for a specified table."""
    config = TABLE_CONFIG.get(table_name.lower())
    if not config:
        raise ValidationError(f"No ID generation rules configured for table '{table_name}'.")

    id_col = config["id_col"]
    prefix = config["prefix"]
    start_num = config["start"]

    owns_connection = connection is None
    conn = get_connection() if owns_connection else connection
    cursor = None

    try:
        cursor = conn.cursor()
        query = (
            f"SELECT {id_col} FROM {table_name} "
            f"WHERE {id_col} LIKE %s "
            f"ORDER BY LENGTH({id_col}) DESC, {id_col} DESC LIMIT 1"
        )
        cursor.execute(query, (f"{prefix}%",))
        row = cursor.fetchone()

        if row and row[0]:
            raw_id = str(row[0])
            numeric_part = raw_id[len(prefix):]
            current_num = int(numeric_part) if numeric_part.isdigit() else start_num
            next_num = current_num + 1
        else:
            next_num = start_num

        return f"{prefix}{next_num}"
    finally:
        if cursor is not None:
            cursor.close()
        if owns_connection and conn is not None:
            conn.close()

