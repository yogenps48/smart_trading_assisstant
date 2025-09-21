from datetime import datetime, timezone

def to_rfc3339(dt: datetime) -> str:
    """
    Convert datetime to RFC3339 format with UTC offset.
    Example: 2025-09-20T15:30:00Z
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")
