import pytest
from datetime import datetime, date
from zoneinfo import ZoneInfo
from app.services.fare_service import apply_surge, get_current_fare
from app.utils.time_utils import get_day_type, is_time_in_window

NAIROBI = ZoneInfo("Africa/Nairobi")


def test_get_day_type_weekday():
    dt = datetime(2025, 3, 17, 8, 0, tzinfo=NAIROBI)  # Monday
    assert get_day_type(dt, []) == 0


def test_get_day_type_weekend():
    dt = datetime(2025, 3, 15, 8, 0, tzinfo=NAIROBI)  # Saturday
    assert get_day_type(dt, []) == 1


def test_get_day_type_holiday():
    dt = datetime(2025, 6, 1, 8, 0, tzinfo=NAIROBI)  # Madaraka Day
    holidays = [date(2025, 6, 1)]
    assert get_day_type(dt, holidays) == 2


def test_is_time_in_window_inside():
    from datetime import time
    dt = datetime(2025, 3, 17, 7, 30, tzinfo=NAIROBI)
    assert is_time_in_window(dt, time(6, 0), time(9, 0)) is True


def test_is_time_in_window_outside():
    from datetime import time
    dt = datetime(2025, 3, 17, 10, 0, tzinfo=NAIROBI)
    assert is_time_in_window(dt, time(6, 0), time(9, 0)) is False


@pytest.mark.asyncio
async def test_apply_surge_no_surge():
    amount, active, reason = await apply_surge(100, None)
    assert amount == 100
    assert active is False
    assert reason is None


@pytest.mark.asyncio
async def test_apply_surge_with_surge():
    from unittest.mock import MagicMock
    surge = MagicMock()
    surge.multiplier = 1.5
    surge.reason = "Heavy rain"
    amount, active, reason = await apply_surge(100, surge)
    assert amount == 150
    assert active is True
    assert reason == "Heavy rain"
