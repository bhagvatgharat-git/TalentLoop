"""Activity logging utility."""

from datetime import datetime
import os

LOG_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "activity_log.txt")
)


def log_activity(message: str) -> None:
    """Append a timestamped log entry to activity_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {message.strip()}\n"
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(log_entry)
