from datetime import datetime, time
from zoneinfo import ZoneInfo

NAIROBI_TZ = ZoneInfo("Africa/Nairobi")


def now_nairobi() -> datetime:
    return datetime.now(NAIROBI_TZ)


def get_day_type(dt: datetime, public_holidays: list) -> int:
    """0=weekday, 1=weekend, 2=public holiday"""
    date_only = dt.date()
    if date_only in public_holidays:
        return 2
    if dt.weekday() >= 5:
        return 1
    return 0


def is_time_in_window(dt: datetime, valid_from, valid_until) -> bool:
    """Check if current time falls within a fare window."""
    current = dt.time().replace(tzinfo=None)
    if isinstance(valid_from, str):
        start = datetime.strptime(valid_from, "%H:%M:%S").time()
        end = datetime.strptime(valid_until, "%H:%M:%S").time()
    else:
        start = valid_from
        end = valid_until
    return start <= current <= end


def format_iso(dt: datetime) -> str:
    return dt.isoformat()