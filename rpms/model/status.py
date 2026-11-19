"""Application status constants and transition lifecycle rules."""

STATUS_APPLIED = "APPLIED"
STATUS_SHORTLISTED = "SHORTLISTED"
STATUS_INTERVIEW = "INTERVIEW"
STATUS_SELECTED = "SELECTED"
STATUS_OFFERED = "OFFERED"
STATUS_JOINED = "JOINED"
STATUS_REJECTED = "REJECTED"

ALL_APPLICATION_STATUSES = (
    STATUS_APPLIED,
    STATUS_SHORTLISTED,
    STATUS_INTERVIEW,
    STATUS_SELECTED,
    STATUS_OFFERED,
    STATUS_JOINED,
    STATUS_REJECTED,
)

ALLOWED_TRANSITIONS = {
    STATUS_APPLIED: [STATUS_SHORTLISTED, STATUS_REJECTED],
    STATUS_SHORTLISTED: [STATUS_INTERVIEW, STATUS_REJECTED],
    STATUS_INTERVIEW: [STATUS_SELECTED, STATUS_REJECTED],
    STATUS_SELECTED: [STATUS_OFFERED, STATUS_REJECTED],
    STATUS_OFFERED: [STATUS_JOINED, STATUS_REJECTED],
    STATUS_JOINED: [],
    STATUS_REJECTED: [],
}


def is_valid_transition(current: str, new: str) -> bool:
    """Check if transitioning from current status to new status is permitted."""
    if not current or not new:
        return False
    curr_upper = current.strip().upper()
    new_upper = new.strip().upper()
    allowed = ALLOWED_TRANSITIONS.get(curr_upper, [])
    return new_upper in allowed

