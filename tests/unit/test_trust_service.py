import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone, timedelta


@pytest.mark.asyncio
async def test_confidence_low_when_no_verified_at():
    from app.services.trust_service import get_data_confidence

    mock_route = MagicMock()
    mock_route.id = "test-id"
    mock_route.fare_last_verified_at = None

    mock_db = AsyncMock()
    result = await get_data_confidence(mock_route, mock_db)
    assert result == "low"


@pytest.mark.asyncio
async def test_confidence_high_when_recent():
    from app.services.trust_service import get_data_confidence

    mock_route = MagicMock()
    mock_route.id = "test-id"
    mock_route.fare_last_verified_at = datetime.now(
        timezone.utc) - timedelta(days=2)

    def make_setting_result(value=None):
        r = MagicMock()
        if value:
            setting = MagicMock()
            setting.value = value
            r.scalar_one_or_none.return_value = setting
        else:
            r.scalar_one_or_none.return_value = None
        return r

    corrections_result = MagicMock()
    corrections_result.scalars.return_value.all.return_value = []

    mock_db = AsyncMock()
    mock_db.execute.side_effect = [
        make_setting_result(),
        make_setting_result(),
        corrections_result,
    ]

    result = await get_data_confidence(mock_route, mock_db)
    assert result == "high"
