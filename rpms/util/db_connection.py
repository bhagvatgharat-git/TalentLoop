"""Database connection provider."""

import mysql.connector
from mysql.connector import Error as MySQLError

from rpms.exception import DatabaseConnectionError
from rpms.util.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def get_connection():
    """Establish and return a connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except MySQLError as exc:
        raise DatabaseConnectionError(
            f"Could not connect to database '{DB_NAME}' on host '{DB_HOST}' as user '{DB_USER}'. "
            f"Reason: {exc.msg}"
        ) from exc
    except Exception as exc:
        raise DatabaseConnectionError(
            f"Unexpected error while connecting to database '{DB_NAME}' on host '{DB_HOST}'."
        ) from exc
